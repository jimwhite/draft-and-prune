#!/usr/bin/env python3
import time
import random
import os
import requests
from typing import Optional, Tuple, Dict, Any, Union
from abc import ABC, abstractmethod
import openai

# Provider-specific imports are deferred so that only the SDK you
# actually use needs to be installed.
try:
    from google import genai
except ImportError:
    genai = None

try:
    from openai import AzureOpenAI
except ImportError:
    AzureOpenAI = None

try:
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
except ImportError:
    DefaultAzureCredential = None
    get_bearer_token_provider = None

class APIConfig:
    """Configuration class for API calls"""
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        gemini_thinking_budget: Optional[int] = None,
        gemini_thinking_level: Optional[str] = None,
        openai_compatible_extra_body: Optional[Dict[str, Any]] = None,
        max_retries: int = 10,
        inter_test_case_delay: float = 2.0
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.gemini_thinking_budget = gemini_thinking_budget
        self.gemini_thinking_level = gemini_thinking_level
        self.openai_compatible_extra_body = openai_compatible_extra_body
        self.max_retries = max_retries
        self.inter_test_case_delay = inter_test_case_delay

class APIClient(ABC):
    """Base class for API clients"""
    def __init__(self, config: APIConfig):
        self.config = config
        self.last_call_metadata: Dict[str, Any] = {}
    
    @property
    def temperature(self) -> float:
        """Get the current temperature setting"""
        return self.config.temperature
    
    @temperature.setter
    def temperature(self, value: float):
        """Set the temperature setting"""
        self.config.temperature = value

    def _clear_last_call_metadata(self) -> None:
        """Clear metadata from the previous API call."""
        self.last_call_metadata = {}

    def _set_last_call_usage(self, usage_obj: Any) -> None:
        """Store token usage metadata from provider response objects."""
        existing_timing = self.last_call_metadata.get("timing")
        if usage_obj is None:
            self.last_call_metadata = {"usage": None}
            if existing_timing is not None:
                self.last_call_metadata["timing"] = existing_timing
            return

        self.last_call_metadata = {
            "usage": {
                "prompt_tokens": getattr(usage_obj, "prompt_tokens", None),
                "completion_tokens": getattr(usage_obj, "completion_tokens", None),
                "total_tokens": getattr(usage_obj, "total_tokens", None),
            }
        }
        if existing_timing is not None:
            self.last_call_metadata["timing"] = existing_timing

    def _set_last_call_timing(self, api_time_only_sec: float, attempt_count: int) -> None:
        """Store API-only timing for the latest call."""
        existing_usage = self.last_call_metadata.get("usage")
        self.last_call_metadata = {
            "timing": {
                "api_time_only_sec": float(api_time_only_sec),
                "attempt_count": int(attempt_count),
            }
        }
        if existing_usage is not None:
            self.last_call_metadata["usage"] = existing_usage

    def get_last_call_metadata(self) -> Dict[str, Any]:
        """Return a shallow copy of metadata for the latest API call."""
        return dict(self.last_call_metadata)
    
    @abstractmethod
    def call(self, prompt: str) -> str:
        """Make an API call with the given prompt and return the response"""
        pass

class GeminiClient(APIClient):
    """Client for Gemini API using the official google-genai SDK."""
    def __init__(self, config: APIConfig, api_key: str = None, api_keys: list = None):
        if genai is None:
            raise ImportError("The 'google-generativeai' package is required for the Gemini provider. "
                              "Install it with: pip install google-generativeai")
        super().__init__(config)
        if api_keys and isinstance(api_keys, list):
            self.api_keys = [k for k in api_keys if k]
        else:
            self.api_keys = [api_key] if api_key else []
        self.current_key_index = 0
        self.api_key = self.api_keys[0] if self.api_keys else api_key
        self.client = None
        self.set_api_key(self.api_key)

    def set_api_key(self, api_key: Optional[str]) -> None:
        """Update API key and reconfigure SDK client."""
        self.api_key = api_key
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = genai.Client()

    def rotate_api_key(self):
        """Rotate to the next API key if multiple keys are available"""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            self.set_api_key(self.api_keys[self.current_key_index])
            print(f"Rotated to API key #{self.current_key_index + 1}")
            return True
        return False

    @staticmethod
    def _build_usage_obj(usage_metadata: Any) -> Any:
        """Normalize provider usage objects to a common schema."""
        return type("UsageObj", (), {
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", None),
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", None),
            "total_tokens": getattr(usage_metadata, "total_token_count", None),
        })()

    @staticmethod
    def _extract_text_from_new_response(response: Any) -> Optional[str]:
        """Extract only text parts from google-genai response objects.

        Avoids accessing `response.text`, which can emit warnings when the
        response includes non-text parts such as `thought_signature`.
        """
        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            parts = getattr(content, "parts", None) or []
            extracted = []
            for part in parts:
                part_text = getattr(part, "text", None)
                if part_text:
                    extracted.append(part_text)
            if extracted:
                return "".join(extracted)
        return None
    
    def call(self, prompt: str) -> str:
        """Call the Gemini API with error handling and retries"""
        self._clear_last_call_metadata()
        api_time_only_sec = 0.0
        attempt_count = 0

        # Try multiple times in case of errors
        for attempt in range(self.config.max_retries):
            try:
                attempt_count += 1
                api_call_start = time.time()
                generation_config: Dict[str, Any] = {
                    "temperature": self.config.temperature,
                }
                if self.config.gemini_thinking_level is not None:
                    generation_config["thinking_config"] = {
                        "thinking_level": self.config.gemini_thinking_level,
                        "include_thoughts": False,
                    }
                elif self.config.gemini_thinking_budget is not None:
                    generation_config["thinking_config"] = {
                        "thinking_budget": self.config.gemini_thinking_budget,
                        "include_thoughts": False,
                    }
                response = self.client.models.generate_content(
                    model=self.config.model_name,
                    contents=prompt,
                    config=generation_config,
                )
                api_time_only_sec += time.time() - api_call_start

                response_text = self._extract_text_from_new_response(response)

                if response_text:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    usage_metadata = getattr(response, "usage_metadata", None)
                    if usage_metadata is None:
                        self._set_last_call_usage(None)
                    else:
                        self._set_last_call_usage(self._build_usage_obj(usage_metadata))
                    return response_text

                block_reason = "Unknown"
                prompt_feedback = getattr(response, "prompt_feedback", None)
                block_reason = getattr(prompt_feedback, "block_reason", "Unknown") if prompt_feedback else "Unknown"
                print(f"Warning: Model response was empty or blocked (Attempt {attempt+1}/{self.config.max_retries}). Reason: {block_reason}")
                if block_reason != 'Unknown' and attempt < self.config.max_retries - 1:
                    print(f"Retrying due to block reason: {block_reason}")
                    time.sleep(self.config.inter_test_case_delay**(attempt+1))  # Exponential backoff
                    continue
                self._set_last_call_timing(api_time_only_sec, attempt_count)
                self._set_last_call_usage(None)
                return f"Generation failed. Reason: {block_reason}"

            except Exception as e:
                if 'api_call_start' in locals():
                    api_time_only_sec += time.time() - api_call_start
                error_str = str(e)
                print(f"Error in API call (attempt {attempt+1}/{self.config.max_retries}): {error_str}")
                
                # Check if it's a rate limit error and try rotating API keys
                if ("quota" in error_str.lower() or "rate" in error_str.lower() or "limit" in error_str.lower()):
                    if self.rotate_api_key():
                        print("Retrying with rotated API key...")
                        time.sleep(2)  # Short delay after key rotation
                        continue
                
                if attempt == self.config.max_retries - 1:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(None)
                    return f"API call failed after {self.config.max_retries} attempts: {error_str}"
                print(f"Waiting {self.config.inter_test_case_delay**(attempt+1)} seconds before retry...")
                time.sleep(self.config.inter_test_case_delay**(attempt+1))
            finally:
                # Basic rate limiting delay
                time.sleep(1.1)

        self._set_last_call_timing(api_time_only_sec, attempt_count)
        self._set_last_call_usage(None)
        return "Max retries reached for API call."

class GPTClient(APIClient):
    """Client for OpenAI's GPT API"""
    def call(self, prompt: str) -> str:
        """Call the GPT API with error handling and retries"""
        self._clear_last_call_metadata()
        api_time_only_sec = 0.0
        attempt_count = 0
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                attempt_count += 1
                api_call_start = time.time()
                response = openai.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    n=1,
                )
                api_time_only_sec += time.time() - api_call_start
                # Extract the content from the choices
                if response.choices and len(response.choices) > 0:
                    if response.choices[0].message:
                        self._set_last_call_timing(api_time_only_sec, attempt_count)
                        self._set_last_call_usage(getattr(response, "usage", None))
                        return response.choices[0].message.content
                    else:
                        error_message = "GPT response was empty."
                        print(f"Warning: {error_message}")
                        last_error = error_message
                        continue # Retry
                else:
                    error_message = "GPT response was empty."
                    print(f"Warning: {error_message}")
                    last_error = error_message
                    continue # Retry
            except Exception as e:
                if 'api_call_start' in locals():
                    api_time_only_sec += time.time() - api_call_start
                error_message = f"Error in API call (attempt {attempt+1}/{self.config.max_retries}): {str(e)}"
                print(error_message)
                last_error = error_message
                if attempt == self.config.max_retries - 1:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(None)
                    return f"API call failed after {self.config.max_retries} attempts. Last error: {last_error}"
                random_sleep = random.uniform(2 ** attempt, 2 ** (attempt + 1))
                print(f"Waiting {random_sleep} seconds before retry...")
                time.sleep(random_sleep) # Exponential backoff
            finally:
                time.sleep(1.1) # Rate limiting delay
        self._set_last_call_timing(api_time_only_sec, attempt_count)
        self._set_last_call_usage(None)
        return f"API call failed after {self.config.max_retries} attempts. Last error: {last_error}"

class AzureOpenAIClient(APIClient):
    """Client for Azure OpenAI API with Entra ID authentication"""
    def __init__(self, config: APIConfig, endpoint: str = None, deployment: str = None, managed_identity_client_id: str = None):
        if AzureOpenAI is None or DefaultAzureCredential is None:
            raise ImportError("The 'azure-identity' and 'openai' packages are required for the Azure OpenAI provider. "
                              "Install them with: pip install azure-identity openai")
        super().__init__(config)
        self.endpoint = endpoint
        self.deployment = deployment
        self.managed_identity_client_id = managed_identity_client_id
        
        # Initialize Azure OpenAI client with Entra ID authentication
        if self.managed_identity_client_id:
            credential = DefaultAzureCredential(managed_identity_client_id=self.managed_identity_client_id)
        else:
            credential = DefaultAzureCredential()
        
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        
        # Map models to appropriate API versions
        if self.config.model_name == "gpt-4":
            api_version="2024-02-01"  # Updated from 2023-05-15
        else:
            # Default to a recent stable version for unknown models
            api_version="2024-02-01"
        
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version,
        )

    def _use_max_completion_tokens(self) -> bool:
        """GPT-5.* deployments require max_completion_tokens instead of max_tokens."""
        name = (self.deployment or self.config.model_name or "").lower()
        return name.startswith("gpt-5") or name.startswith("gpt5")
    
    def call(self, prompt: str) -> str:
        """Call the Azure OpenAI API with error handling and retries"""
        self._clear_last_call_metadata()
        api_time_only_sec = 0.0
        attempt_count = 0
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                request_args = {
                    "model": self.deployment,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.config.temperature,
                    "n": 1,
                    "stop": None,
                    "stream": False,
                }
                if self._use_max_completion_tokens():
                    request_args["max_completion_tokens"] = 2048
                else:
                    request_args["max_tokens"] = 2048

                attempt_count += 1
                api_call_start = time.time()
                response = self.client.chat.completions.create(**request_args)
                api_time_only_sec += time.time() - api_call_start
                
                # Extract the content from the choices
                if response.choices and len(response.choices) > 0:
                    if response.choices[0].message:
                        self._set_last_call_timing(api_time_only_sec, attempt_count)
                        self._set_last_call_usage(getattr(response, "usage", None))
                        return response.choices[0].message.content
                    else:
                        error_message = "Azure OpenAI response was empty."
                        print(f"Warning: {error_message}")
                        last_error = error_message
                        continue # Retry
                else:
                    error_message = "Azure OpenAI response was empty."
                    print(f"Warning: {error_message}")
                    last_error = error_message
                    continue # Retry
            except Exception as e:
                if 'api_call_start' in locals():
                    api_time_only_sec += time.time() - api_call_start
                error_message = f"Error in Azure OpenAI API call (attempt {attempt+1}/{self.config.max_retries}): {str(e)}"
                print(error_message)
                last_error = error_message
                if attempt == self.config.max_retries - 1:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(None)
                    return f"Azure OpenAI API call failed after {self.config.max_retries} attempts. Last error: {last_error}"
                random_sleep = random.uniform(2 ** attempt, 2 ** (attempt + 1))
                print(f"Waiting {random_sleep} seconds before retry...")
                time.sleep(random_sleep) # Exponential backoff
            finally:
                time.sleep(1.1) # Rate limiting delay
        self._set_last_call_timing(api_time_only_sec, attempt_count)
        self._set_last_call_usage(None)
        return f"Azure OpenAI API call failed after {self.config.max_retries} attempts. Last error: {last_error}"

class OpenAICompatibleClient(APIClient):
    """Client for OpenAI-compatible chat completion endpoints."""
    def __init__(self, config: APIConfig, api_key: str = None, base_url: str = None):
        super().__init__(config)
        if base_url:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = openai.OpenAI(api_key=api_key)

    def call(self, prompt: str) -> str:
        """Call an OpenAI-compatible chat endpoint with retries."""
        self._clear_last_call_metadata()
        api_time_only_sec = 0.0
        attempt_count = 0
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                attempt_count += 1
                request_args: Dict[str, Any] = {
                    "model": self.config.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.config.temperature,
                    "n": 1,
                }
                if isinstance(self.config.openai_compatible_extra_body, dict) and self.config.openai_compatible_extra_body:
                    request_args["extra_body"] = self.config.openai_compatible_extra_body

                api_call_start = time.time()
                response = self.client.chat.completions.create(**request_args)
                api_time_only_sec += time.time() - api_call_start

                if response.choices and len(response.choices) > 0 and response.choices[0].message:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(getattr(response, "usage", None))
                    return response.choices[0].message.content

                last_error = "OpenAI-compatible response was empty."
                print(f"Warning: {last_error}")

            except Exception as e:
                if 'api_call_start' in locals():
                    api_time_only_sec += time.time() - api_call_start
                last_error = f"Error in OpenAI-compatible API call (attempt {attempt+1}/{self.config.max_retries}): {str(e)}"
                print(last_error)
                if attempt == self.config.max_retries - 1:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(None)
                    return f"OpenAI-compatible API call failed after {self.config.max_retries} attempts. Last error: {last_error}"
                random_sleep = random.uniform(2 ** attempt, 2 ** (attempt + 1))
                print(f"Waiting {random_sleep} seconds before retry...")
                time.sleep(random_sleep)
            finally:
                time.sleep(1.1)

        self._set_last_call_timing(api_time_only_sec, attempt_count)
        self._set_last_call_usage(None)
        return f"OpenAI-compatible API call failed after {self.config.max_retries} attempts. Last error: {last_error}"

class AnthropicClient(APIClient):
    """Client for Anthropic Messages API."""
    def __init__(self, config: APIConfig, api_key: str = None, base_url: str = None):
        super().__init__(config)
        self.api_key = api_key
        self.base_url = (base_url or "https://api.anthropic.com/v1").rstrip("/")

    def _build_usage_obj(self, usage: Dict[str, Any]):
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        total_tokens = None
        if isinstance(input_tokens, int) and isinstance(output_tokens, int):
            total_tokens = input_tokens + output_tokens
        return type("UsageObj", (), {
            "prompt_tokens": input_tokens,
            "completion_tokens": output_tokens,
            "total_tokens": total_tokens,
        })()

    def call(self, prompt: str) -> str:
        """Call Anthropic Messages API with retries."""
        self._clear_last_call_metadata()
        api_time_only_sec = 0.0
        attempt_count = 0
        last_error = None

        if not self.api_key:
            self._set_last_call_timing(api_time_only_sec, attempt_count)
            self._set_last_call_usage(None)
            return "Anthropic API key is missing."

        for attempt in range(self.config.max_retries):
            try:
                attempt_count += 1
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                payload = {
                    "model": self.config.model_name,
                    "max_tokens": 2048,
                    "temperature": self.config.temperature,
                    "messages": [{"role": "user", "content": prompt}],
                }

                api_call_start = time.time()
                response = requests.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload,
                    timeout=180,
                )
                api_time_only_sec += time.time() - api_call_start

                if response.status_code >= 400:
                    raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

                body = response.json()
                content = body.get("content", [])
                text_parts = [
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                ]
                text = "".join(text_parts).strip()
                if text:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    usage = body.get("usage") or {}
                    self._set_last_call_usage(self._build_usage_obj(usage))
                    return text

                last_error = "Anthropic response was empty."
                print(f"Warning: {last_error}")

            except Exception as e:
                if 'api_call_start' in locals():
                    api_time_only_sec += time.time() - api_call_start
                last_error = f"Error in Anthropic API call (attempt {attempt+1}/{self.config.max_retries}): {str(e)}"
                print(last_error)
                if attempt == self.config.max_retries - 1:
                    self._set_last_call_timing(api_time_only_sec, attempt_count)
                    self._set_last_call_usage(None)
                    return f"Anthropic API call failed after {self.config.max_retries} attempts. Last error: {last_error}"
                random_sleep = random.uniform(2 ** attempt, 2 ** (attempt + 1))
                print(f"Waiting {random_sleep} seconds before retry...")
                time.sleep(random_sleep)
            finally:
                time.sleep(1.1)

        self._set_last_call_timing(api_time_only_sec, attempt_count)
        self._set_last_call_usage(None)
        return f"Anthropic API call failed after {self.config.max_retries} attempts. Last error: {last_error}"

def get_api_client(provider: str, config: APIConfig, **kwargs) -> APIClient:
    """Factory function to get the appropriate API client based on provider"""
    if provider.lower() == "gemini":
        api_key = kwargs.get('api_key')
        api_keys = kwargs.get('api_keys')  # Support multiple keys
        return GeminiClient(config, api_key, api_keys)
    # elif provider.lower() == "gpt":
    #     return GPTClient(config)
    elif provider.lower() == "azure-openai" or provider.lower() == "azure":
        # Extract Azure-specific parameters from kwargs
        endpoint = kwargs.get('endpoint')
        deployment = kwargs.get('deployment')
        managed_identity_client_id = kwargs.get('managed_identity_client_id')
        return AzureOpenAIClient(config, endpoint, deployment, managed_identity_client_id)
    elif provider.lower() in ("openai-compatible", "openai_compatible"):
        api_key = kwargs.get('api_key')
        base_url = kwargs.get('base_url')
        return OpenAICompatibleClient(config, api_key=api_key, base_url=base_url)
    elif provider.lower() in ("anthropic", "claude"):
        api_key = kwargs.get('api_key')
        base_url = kwargs.get('base_url')
        return AnthropicClient(config, api_key=api_key, base_url=base_url)
    else:
        raise ValueError(f"Unsupported API provider: {provider}") 
