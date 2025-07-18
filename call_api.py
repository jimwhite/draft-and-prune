#!/usr/bin/env python3
import time
import os
from typing import Optional, Tuple, Dict, Any, Union
from abc import ABC, abstractmethod
import openai
import google.generativeai as genai
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class APIConfig:
    """Configuration class for API calls"""
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.0,
        max_repairs: int = 3,
        inter_test_case_delay: float = 2.0
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_repairs = max_repairs
        self.inter_test_case_delay = inter_test_case_delay

class APIClient(ABC):
    """Base class for API clients"""
    def __init__(self, config: APIConfig):
        self.config = config
    
    @property
    def temperature(self) -> float:
        """Get the current temperature setting"""
        return self.config.temperature
    
    @temperature.setter
    def temperature(self, value: float):
        """Set the temperature setting"""
        self.config.temperature = value
    
    @abstractmethod
    def call(self, prompt: str) -> str:
        """Make an API call with the given prompt and return the response"""
        pass

class GeminiClient(APIClient):
    """Client for Google's Gemini API"""
    def call(self, prompt: str) -> str:
        """Call the Gemini API with error handling and retries"""
        # Initialize the model
        client = genai
        model = client.GenerativeModel(self.config.model_name)
    
        # Configure the generation parameters
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            candidate_count=1  # Single generation only
        )
        
        # Using less restrictive safety settings
        safety_settings = {
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"
        }

        # Try multiple times in case of errors
        for attempt in range(self.config.max_repairs):
            try:
                response = model.generate_content(
                    contents=prompt,
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )

                if response.parts:
                    return response.text
                else:
                    block_reason = response.prompt_feedback.block_reason if response.prompt_feedback else 'Unknown'
                    print(f"Warning: Model response was empty or blocked (Attempt {attempt+1}/{self.config.max_repairs}). Reason: {block_reason}")
                    if block_reason != 'Unknown' and attempt < self.config.max_repairs - 1:
                        print(f"Retrying due to block reason: {block_reason}")
                        time.sleep(self.config.inter_test_case_delay**(attempt+1))  # Exponential backoff
                        continue
                    return f"Generation failed. Reason: {block_reason}"

            except Exception as e:
                print(f"Error in API call (attempt {attempt+1}/{self.config.max_repairs}): {str(e)}")
                if attempt == self.config.max_repairs - 1:
                    return f"API call failed after {self.config.max_repairs} attempts: {str(e)}"
                print(f"Waiting {self.config.inter_test_case_delay**(attempt+1)} seconds before retry...")
                time.sleep(self.config.inter_test_case_delay**(attempt+1))
            finally:
                # Basic rate limiting delay
                time.sleep(1.1)

        return "Max retries reached for API call."

class GPTClient(APIClient):
    """Client for OpenAI's GPT API"""
    def call(self, prompt: str) -> str:
        """Call the GPT API with error handling and retries"""
        last_error = None
        for attempt in range(self.config.max_repairs):
            try:
                response = openai.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    n=1,
                )
                # Extract the content from the choices
                if response.choices and len(response.choices) > 0:
                    if response.choices[0].message:
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
                error_message = f"Error in API call (attempt {attempt+1}/{self.config.max_repairs}): {str(e)}"
                print(error_message)
                last_error = error_message
                if attempt == self.config.max_repairs - 1:
                    return f"API call failed after {self.config.max_repairs} attempts. Last error: {last_error}"
                print(f"Waiting {2**(attempt+1)} seconds before retry...")
                time.sleep(2**(attempt+1)) # Exponential backoff
            finally:
                time.sleep(1.1) # Rate limiting delay
        return f"API call failed after {self.config.max_repairs} attempts. Last error: {last_error}"

class AzureOpenAIClient(APIClient):
    """Client for Azure OpenAI API with Entra ID authentication"""
    def __init__(self, config: APIConfig, endpoint: str = None, deployment: str = None, managed_identity_client_id: str = None):
        super().__init__(config)
        self.endpoint = endpoint or os.getenv("ENDPOINT_URL", "https://ai4mtest1.openai.azure.com/")
        self.deployment = deployment or os.getenv("DEPLOYMENT_NAME", self.config.model_name)
        self.managed_identity_client_id = managed_identity_client_id or os.getenv("MANAGED_IDENTITY_CLIENT_ID")
        
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
    
    def call(self, prompt: str) -> str:
        """Call the Azure OpenAI API with error handling and retries"""
        last_error = None
        for attempt in range(self.config.max_repairs):
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    stream=False
                )
                
                # Extract the content from the choices
                if response.choices and len(response.choices) > 0:
                    if response.choices[0].message:
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
                error_message = f"Error in Azure OpenAI API call (attempt {attempt+1}/{self.config.max_repairs}): {str(e)}"
                print(error_message)
                last_error = error_message
                if attempt == self.config.max_repairs - 1:
                    return f"Azure OpenAI API call failed after {self.config.max_repairs} attempts. Last error: {last_error}"
                print(f"Waiting {2**(attempt+1)} seconds before retry...")
                time.sleep(2**(attempt+1)) # Exponential backoff
            finally:
                time.sleep(1.1) # Rate limiting delay
        return f"Azure OpenAI API call failed after {self.config.max_repairs} attempts. Last error: {last_error}"

def get_api_client(provider: str, config: APIConfig, **kwargs) -> APIClient:
    """Factory function to get the appropriate API client based on provider"""
    if provider.lower() == "gemini":
        return GeminiClient(config)
    elif provider.lower() == "gpt":
        return GPTClient(config)
    elif provider.lower() == "azure-openai" or provider.lower() == "azure":
        # Extract Azure-specific parameters from kwargs
        endpoint = kwargs.get('endpoint')
        deployment = kwargs.get('deployment')
        managed_identity_client_id = kwargs.get('managed_identity_client_id')
        return AzureOpenAIClient(config, endpoint, deployment, managed_identity_client_id)
    else:
        raise ValueError(f"Unsupported API provider: {provider}") 