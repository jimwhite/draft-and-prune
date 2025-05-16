#!/usr/bin/env python3
import time
from typing import Optional, Tuple, Dict, Any
from abc import ABC, abstractmethod
import openai
import google.generativeai as genai

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
    
    @abstractmethod
    def call(self, prompt: str) -> str:
        """Make an API call with the given prompt"""
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
            temperature=self.config.temperature
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
                )
                # Extract the content from the first choice
                if response.choices and len(response.choices) > 0 and response.choices[0].message:
                    return response.choices[0].message.content
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

def get_api_client(provider: str, config: APIConfig) -> APIClient:
    """Factory function to get the appropriate API client based on provider"""
    if provider.lower() == "gemini":
        return GeminiClient(config)
    elif provider.lower() == "gpt":
        return GPTClient(config)
    else:
        raise ValueError(f"Unsupported API provider: {provider}") 