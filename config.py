#!/usr/bin/env python3

class ReasonerConfig:
    """Configuration for the reasoning system"""
    
    def __init__(self, 
                 reasoning_method: str,
                 api_key: str,
                 dataset: str,
                 model_name: str = "gemini-2.5-flash-preview-04-17", 
                 data_path: str = None,
                 temperature: float = 0.6, 
                 max_repairs: int = 3,
                 limit: int = None,
                 result_filename_template: str = "{dataset}_{reasoning_method}_results_{model_name}_{shots}_shot_COT.json",
                 inter_test_case_delay: int = 5,
                 shots: int = 0):
        self.reasoning_method = reasoning_method
        self.api_key = api_key
        self.dataset = dataset
        self.model_name = model_name
        self.data_path = data_path
        self.temperature = temperature
        self.max_repairs = max_repairs
        self.result_filename_template = result_filename_template
        self.inter_test_case_delay = inter_test_case_delay
        self.limit = limit
        self.shots = shots

    def get_results_filename(self) -> str:
        """Generate results filename based on model name"""
        return self.result_filename_template.format(dataset=self.dataset, reasoning_method=self.reasoning_method, model_name=self.model_name, shots=self.shots) 