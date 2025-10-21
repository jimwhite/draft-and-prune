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
                 model: str = "gemini-2.5-flash-preview-04-17",  # Backward compatibility
                 plan_model: str = None,  # New: Model for plan generation
                 code_model: str = None,  # New: Model for code generation
                 code_temp: float = 0.6, 
                 max_repairs: int = 3,
                 max_retries: int = 10,
                 num_processes: int = 1,
                 test_delay: int = 5,
                 prompt_path: str = None,
                 shots: str = 'zero',
                 desired_indices: list = None,
                 # Azure OpenAI specific parameters
                 azure_endpoint: str = None,
                 azure_deployment: str = None,
                 azure_managed_identity_client_id: str = None,
                 # Gemini multiple API keys
                 gemini_api_keys: list = None,
                 # Plan generation parameters
                 num_paths: int = 3,
                 plan_temp: float = 1.0):
        """
        Initialize configuration either from parameters or will be loaded from YAML
        
        Args:
            reasoning_method: The reasoning method to use
            api_key: API key for the model service
            dataset: Dataset name to use
            test_file: Test file to use
            model: Primary model name
            code_temp: code_temp for model generation
            max_repairs: Maximum number of repair attempts
            max_retries: Maximum number of LLM requests
            num_processes: Number of parallel processes to use
            test_delay: Delay between test cases in seconds
            prompt_path: Path to the prompt file
            shots: Number of shots for few-shot learning
            desired_indices: Desired indices to use
            azure_endpoint: Azure OpenAI endpoint
            azure_deployment: Azure OpenAI deployment
            azure_managed_identity_client_id: Azure managed identity client ID
            num_paths: Number of different plans to generate
            plan_temp: code_temp for plan generation
        """
        self.dataset = dataset
        self.test_file = test_file
        self.reasoning_method = reasoning_method
        self.api_key = api_key
        self.model = model  # Backward compatibility
        self.plan_model = plan_model
        self.code_model = code_model
        self.code_temp = code_temp
        self.max_repairs = max_repairs
        self.max_retries = max_retries
        self.num_processes = num_processes
        self.test_delay = test_delay
        self.prompt_path = prompt_path
        self.shots = shots
        self.desired_indices = desired_indices
        self.azure_endpoint = azure_endpoint
        self.azure_deployment = azure_deployment
        self.azure_managed_identity_client_id = azure_managed_identity_client_id
        self.gemini_api_keys = gemini_api_keys
        self.num_paths = num_paths
        self.plan_temp = plan_temp
    
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
        
        # Handle new model field names with backward compatibility
        if 'plan_model' in config_data:
            instance.plan_model = config_data['plan_model']
            instance.model = config_data['plan_model']  # For backward compatibility
        else:
            instance.model = config_data.get('model', 'gemini-2.5-flash')
            instance.plan_model = instance.model
            
        if 'code_model' in config_data:
            instance.code_model = config_data['code_model']
        else:
            instance.code_model = instance.plan_model  # Default to same as plan model
        instance.code_temp = config_data['code_temp']
        instance.max_repairs = config_data['max_repairs']
        if config_data.get('max_retries'):
            instance.max_retries = config_data['max_retries']
        else:
            instance.max_retries = 10   # Set Default Value
        instance.num_processes = config_data.get('num_processes', 1)  # Default to 1 if not specified
        instance.test_delay = config_data['test_delay']
        instance.prompt_path = config_data['prompt_path']
        instance.shots = config_data['shots']
        instance.desired_indices = config_data['desired_indices']
        # Azure OpenAI fields are optional for backward compatibility
        instance.azure_endpoint = config_data.get('azure_endpoint')
        instance.azure_deployment = config_data.get('azure_deployment')
        instance.azure_managed_identity_client_id = config_data.get('azure_managed_identity_client_id')
        # Gemini multiple API keys are optional
        instance.gemini_api_keys = config_data.get('gemini_api_keys')
        # Plan generation parameters with defaults
        instance.num_paths = config_data.get('num_paths', 3)
        instance.plan_temp = config_data.get('plan_temp', 1.0)
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
        if not isinstance(self.code_temp, (int, float)) or self.code_temp < 0:
            raise ValueError("code_temp must be a non-negative number")
        if not isinstance(self.max_repairs, int) or self.max_repairs < 0:
            raise ValueError("max_repairs must be a non-negative integer")
        if not isinstance(self.max_retries, int) or self.max_retries <= 0:
            raise ValueError("max_retries must be a positive integer")
        if not isinstance(self.num_processes, int) or self.num_processes <= 0:
            raise ValueError("num_processes must be a positive integer")
        if not isinstance(self.test_delay, int) or self.test_delay < 0:
            raise ValueError("test_delay must be a non-negative integer")
        if not isinstance(self.shots, str) or self.shots not in ['zero', 'one', 'two', 'three', 'six', 'nine']:
            raise ValueError("shots must be a string in ['zero', 'one', 'two', 'three', 'six', 'nine']")
        if self.desired_indices is not None and not isinstance(self.desired_indices, list):
            raise TypeError("desired_indices must be a list or None")
        if self.azure_endpoint is not None and not isinstance(self.azure_endpoint, str):
            raise TypeError("azure_endpoint must be a string or None")
        if self.azure_deployment is not None and not isinstance(self.azure_deployment, str):
            raise TypeError("azure_deployment must be a string or None")
        if self.azure_managed_identity_client_id is not None and not isinstance(self.azure_managed_identity_client_id, str):
            raise TypeError("azure_managed_identity_client_id must be a string or None")
        if not isinstance(self.num_paths, int) or self.num_paths <= 0:
            raise ValueError("num_paths must be a positive integer")
        if not isinstance(self.plan_temp, (int, float)) or self.plan_temp < 0:
            raise ValueError("plan_temp must be a non-negative number")
    
    def save_to_yaml(self, yaml_path: str) -> None:
        """
        Save current configuration to a YAML file
        
        Args:
            yaml_path: Path where to save the YAML configuration file
        """
        # Create ordered dictionary with both new and legacy field names
        ordered_config = {
            'dataset': self.dataset,
            'test_file': self.test_file,
            'reasoning_method': self.reasoning_method,
            'api_key': self.api_key,
            # New model field names (preferred)
            'plan_model': getattr(self, 'plan_model', self.model),
            'code_model': getattr(self, 'code_model', self.model),
            # Legacy field names (for backward compatibility)
            'model': self.model,
            'code_temp': self.code_temp,
            'max_repairs': self.max_repairs,
            'max_retries': self.max_retries,
            'num_processes': self.num_processes,
            'test_delay': self.test_delay,
            'prompt_path': self.prompt_path,
            'shots': self.shots,
            'desired_indices': self.desired_indices,
            'azure_endpoint': self.azure_endpoint,
            'azure_deployment': self.azure_deployment,
            'azure_managed_identity_client_id': self.azure_managed_identity_client_id,
            # Multiple Gemini API keys for batch distribution
            'gemini_api_keys': getattr(self, 'gemini_api_keys', None),
            # Plan generation parameters
            'num_paths': getattr(self, 'num_paths', 3),
            'plan_temp': getattr(self, 'plan_temp', 1.0)
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

