#!/usr/bin/env python3
import json
from abc import ABC, abstractmethod
from typing import List, Dict
import os

class DatasetLoader(ABC):
    """Base class for loading different dataset formats"""
    
    @abstractmethod
    def load_data(self, file_path: str) -> List[Dict]:
        """Load dataset from file"""
        pass
    
    @abstractmethod
    def get_test_case_id(self, test_case: Dict) -> str:
        """Get a unique identifier for the test case"""
        pass


class AR_LSAT_DatasetLoader(DatasetLoader):
    """Loader for the AR-LSAT dataset"""
    
    def load_data(self, file_path: str) -> List[Dict]:
        """Load test cases from JSON file"""
        file_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Ensure all test cases have an id_string
        for i, test_case in enumerate(data):
            if "id_string" not in test_case:
                test_case["id_string"] = f"test_{i}"
                
        return data
    
    def get_test_case_id(self, test_case: Dict) -> str:
        """Get the ID of a test case"""
        return test_case.get("id_string", "unknown_id") 