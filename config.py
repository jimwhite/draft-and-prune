#!/usr/bin/env python3
import os
from datetime import datetime

class ReasonerConfig:
    """Configuration for the reasoning system"""
    
    def __init__(self, 
                 reasoning_method: str,
                 api_key: str,
                 dataset: str,
                 model_name: str = "gemini-2.5-flash-preview-04-17", 
                 fix_model_name: str = "gemini-2.5-flash-preview-04-17",
                 data_path: str = None,
                 temperature: float = 0.6, 
                 max_repairs: int = 3,
                 limit: int = None,
                 inter_test_case_delay: int = 5,
                 shots: int = 0,
                 results_folder: str = None):
        self.reasoning_method = reasoning_method
        self.api_key = api_key
        self.dataset = dataset
        self.model_name = model_name
        self.fix_model_name = fix_model_name
        self.data_path = data_path
        self.temperature = temperature
        self.max_repairs = max_repairs
        self.inter_test_case_delay = inter_test_case_delay
        self.limit = limit
        self.shots = shots
        self.results_folder = results_folder

