#!/usr/bin/env python3
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Iterator, Optional, Union
import os
import random

# PyTorch-style Dataset, DataLoader, and Sampler classes
class Dataset(ABC):
    """Abstract base class for all datasets"""
    
    @abstractmethod
    def __len__(self) -> int:
        """Return the size of the dataset"""
        pass
    
    @abstractmethod
    def __getitem__(self, idx: int):
        """Get a data sample by index"""
        pass


class JSON_Dataset(Dataset):
    """PyTorch-style Dataset for json data"""
    
    def __init__(self, data: List[Dict]):
        """
        Initialize dataset with loaded data
        
        Args:
            data: List of test case dictionaries
        """
        self.data = data
    
    def __len__(self) -> int:
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict:
        """Get a test case by index"""
        if idx >= len(self.data) or idx < 0:
            raise IndexError(f"Index {idx} out of range for dataset of size {len(self.data)}")
        return self.data[idx]
    
    @classmethod
    def from_file(cls, file_path: str) -> 'JSON_Dataset':
        """Create dataset from file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return cls(data)


class Sampler:
    """
    Unified sampler class that supports multiple sampling strategies:
    """
    def __init__(self, 
                 dataset_size: int,
                 desired_indices: Optional[List[int]] = None,
                 generator=None):
        """
        Args:
            desired_indices: List of specific indices
            generator: Random number generator for reproducibility (optional)
        """
        self.generator = generator
        
        if desired_indices is not None:
            # check if desired_indices are valid
            if not all(isinstance(i, int) for i in desired_indices):
                raise ValueError("desired_indices must be a list of integers")
            if not all(i >= 0 and i < dataset_size for i in desired_indices):
                raise ValueError("desired_indices must be within the range of the dataset")
            self.indices = desired_indices
            
        else:
            self.indices = list(range(dataset_size))
        
    def __iter__(self) -> Iterator[int]:
        """Return an iterator over desired indices"""
        return iter(self.indices)
    
    def __len__(self) -> int:
        """Return the number of samples"""
        return len(self.indices)


class DataLoader:
    """
    PyTorch-style DataLoader for iterating over datasets with batching and sampling
    """
    
    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = 1,
        sampler: Optional[Sampler] = None,
        drop_last: bool = False
    ):
        """
        Args:
            dataset: Dataset to load from
            batch_size: Number of samples per batch
            sampler: Custom sampler
            drop_last: Whether to drop the last incomplete batch
        """
        self.dataset = dataset
        self.batch_size = batch_size
        self.drop_last = drop_last

        if sampler is not None:
            self.sampler = sampler
        else:
            raise ValueError("sampler is required")
        
    
    def __iter__(self):
        """Iterate over batches"""
        batch = []
        for idx in self.sampler:
            batch.append(self.dataset[idx])
            
            if len(batch) == self.batch_size:
                yield batch
                batch = []
        
        # Handle remaining items
        if batch and not self.drop_last:
            yield batch
    
    def __len__(self) -> int:
        """Return number of batches"""
        sampler_len = len(self.sampler)
        if self.drop_last:
            return sampler_len // self.batch_size
        else:
            return (sampler_len + self.batch_size - 1) // self.batch_size