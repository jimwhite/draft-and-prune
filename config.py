#!/usr/bin/env python3
import os
import yaml
from datetime import datetime
from typing import Optional, Dict, Any

class ReasonerConfig:
    """Configuration for the reasoning system"""
    
    def __init__(self, 
                 dataset: str = None,
                 test_file: str = None,
                 reasoning_method: str = None,
                 api_key: str = None,
                 model: str = "gemini-2.5-flash-preview-04-17", 
                 fix_model: str = None,
                 fix_api_key: str = None,
                 temperature: float = 0.6, 
                 max_repairs: int = 3,
                 test_delay: int = 5,
                 prompt_path: str = None,
                 shots: str = 'zero',
                 desired_indices: list = None,
                 # Azure OpenAI specific parameters
                 azure_endpoint: str = None,
                 azure_deployment: str = None,
                 azure_managed_identity_client_id: str = None):
        """
        Initialize configuration either from parameters or will be loaded from YAML
        
        Args:
            reasoning_method: The reasoning method to use
            api_key: API key for the model service
            dataset: Dataset name to use
            test_file: Test file to use
            model: Primary model name
            fix_model: Model name for fixing/repair operations
            temperature: Temperature for model generation
            max_repairs: Maximum number of repair attempts
            test_delay: Delay between test cases in seconds
            prompt_path: Path to the prompt file
            shots: Number of shots for few-shot learning
            desired_indices: Desired indices to use
            azure_endpoint: Azure OpenAI endpoint
            azure_deployment: Azure OpenAI deployment
            azure_managed_identity_client_id: Azure managed identity client ID
        """
        self.dataset = dataset
        self.test_file = test_file
        self.reasoning_method = reasoning_method
        self.api_key = api_key
        self.model = model
        self.fix_model = fix_model
        self.fix_api_key = fix_api_key
        self.temperature = temperature
        self.max_repairs = max_repairs
        self.test_delay = test_delay
        self.prompt_path = prompt_path
        self.shots = shots
        self.desired_indices = desired_indices
        self.azure_endpoint = azure_endpoint
        self.azure_deployment = azure_deployment
        self.azure_managed_identity_client_id = azure_managed_identity_client_id
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ReasonerConfig':
        """
        Load configuration from a YAML file
        
        Args:
            yaml_path: Path to the YAML configuration file
            
        Returns:
            ReasonerConfig instance with loaded configuration
            
        Raises:
            FileNotFoundError: If the YAML file doesn't exist
            yaml.YAMLError: If the YAML file is malformed
            KeyError: If required configuration keys are missing
        """
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")
        
        try:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {yaml_path}: {e}")
        
        if config_data is None:
            raise ValueError(f"Empty or invalid YAML file: {yaml_path}")
        
        # Create instance with loaded data
        instance = cls()
        instance.dataset = config_data['dataset']
        instance.test_file = config_data['test_file']
        instance.reasoning_method = config_data['reasoning_method']
        instance.api_key = config_data['api_key']
        instance.model = config_data['model']
        if config_data.get('fix_model'):
            instance.fix_model = config_data['fix_model']
        if config_data.get('fix_api_key'):
            instance.fix_api_key = config_data['fix_api_key']
        instance.temperature = config_data['temperature']
        instance.max_repairs = config_data['max_repairs']
        instance.test_delay = config_data['test_delay']
        instance.prompt_path = config_data['prompt_path']
        instance.shots = config_data['shots']
        instance.desired_indices = config_data['desired_indices']
        # Azure OpenAI fields are optional for backward compatibility
        instance.azure_endpoint = config_data.get('azure_endpoint')
        instance.azure_deployment = config_data.get('azure_deployment')
        instance.azure_managed_identity_client_id = config_data.get('azure_managed_identity_client_id')
        instance._validate_config()
        return instance
    
    def _validate_config(self) -> None:
        """Validate configuration values and types"""
        if not isinstance(self.reasoning_method, str):
            raise TypeError("reasoning_method must be a string")
        if not isinstance(self.api_key, str):
            raise TypeError("api_key must be a string")
        if not isinstance(self.dataset, str):
            raise TypeError("dataset must be a string")
        if not isinstance(self.model, str):
            raise TypeError("model must be a string")
        if not isinstance(self.fix_model, str):
            raise TypeError("fix_model must be a string")
        if self.fix_api_key is not None and not isinstance(self.fix_api_key, str):
            raise TypeError("fix_api_key must be a string")
        if not isinstance(self.temperature, (int, float)) or self.temperature < 0:
            raise ValueError("temperature must be a non-negative number")
        if not isinstance(self.max_repairs, int) or self.max_repairs < 0:
            raise ValueError("max_repairs must be a non-negative integer")
        if not isinstance(self.test_delay, int) or self.test_delay < 0:
            raise ValueError("test_delay must be a non-negative integer")
        if not isinstance(self.shots, str) or self.shots not in ['zero', 'one', 'two', 'three']:
            raise ValueError("shots must be a string in ['zero', 'one', 'two', 'three']")
        if self.desired_indices is not None and not isinstance(self.desired_indices, list):
            raise TypeError("desired_indices must be a list or None")
        if self.azure_endpoint is not None and not isinstance(self.azure_endpoint, str):
            raise TypeError("azure_endpoint must be a string or None")
        if self.azure_deployment is not None and not isinstance(self.azure_deployment, str):
            raise TypeError("azure_deployment must be a string or None")
        if self.azure_managed_identity_client_id is not None and not isinstance(self.azure_managed_identity_client_id, str):
            raise TypeError("azure_managed_identity_client_id must be a string or None")
    
    def save_to_yaml(self, yaml_path: str) -> None:
        """
        Save current configuration to a YAML file
        
        Args:
            yaml_path: Path where to save the YAML configuration file
        """
        # Create ordered dictionary matching __init__ parameter order
        ordered_config = {
            'dataset': self.dataset,
            'test_file': self.test_file,
            'reasoning_method': self.reasoning_method,
            'api_key': self.api_key,
            'model': self.model,
            'fix_model': self.fix_model if self.fix_model is not None else None,
            'fix_api_key': self.fix_api_key if self.fix_api_key is not None else None,
            'temperature': self.temperature,
            'max_repairs': self.max_repairs,
            'test_delay': self.test_delay,
            'prompt_path': self.prompt_path,
            'shots': self.shots,
            'desired_indices': self.desired_indices,
            'azure_endpoint': self.azure_endpoint,
            'azure_deployment': self.azure_deployment,
            'azure_managed_identity_client_id': self.azure_managed_identity_client_id
        }
        
        try:
            with open(yaml_path, 'w', encoding='utf-8') as file:
                yaml.dump(ordered_config, file, default_flow_style=False, indent=2, sort_keys=False)
        except Exception as e:
            raise IOError(f"Error saving configuration to {yaml_path}: {e}")
    
    def __str__(self) -> str:
        """String representation of the configuration"""
        return f"ReasonerConfig({self.__dict__})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the configuration"""
        return self.__str__()

