#!/usr/bin/env python3
"""
Generalized ablation analysis script for neural-symbolic reasoning experiments.

This script analyzes experimental results and creates comprehensive CSV/XLSX files with:

TWO-STEP EXPERIMENTS (sketch-based) - 6 methods with --all-methods:
1. SketchFormal (VVV): Sketch Plans + Multi-path + Semantic Pruning [PRIMARY METHOD]
2. Sketch-only (VXX): Sketch Plans + Single path + No pruning
3. SketchFormal with semantic pruning only (VXV): Sketch Plans + Single path + Semantic Pruning
4. SketchFormal with majority vote (VVX): Sketch Plans + Multi-path + No pruning
5. Existence pruning + majority vote: Multi-path + existence pruning only (length >= 1)
6. Uniqueness pruning + majority vote: Multi-path + uniqueness pruning only (length <= 1)

ONE-STEP EXPERIMENTS (direct translation) - 6 methods with --all-methods:
1. Direct translation (XXX): No sketch + Single path + No pruning
2. Direct translation with pruning (XXV): No sketch + Single path + Semantic Pruning
3. Direct translation with multi-path (XVX): No sketch + Multi-path + No pruning
4. Direct translation with multi-path and pruning (XVV): No sketch + Multi-path + Semantic Pruning
5. Existence pruning + majority vote: Multi-path + existence pruning only (length >= 1)
6. Uniqueness pruning + majority vote: Multi-path + uniqueness pruning only (length <= 1)

PRUNING ABLATION STUDY:
- path pruning (existence): Can be satisfied (length >= 1)
- path pruning (uniqueness): Unique solution (length <= 1)

VOTER SENSITIVITY ANALYSIS:
- Analyzes how accuracy changes with different numbers of voters (1, 3, 5, 7, 9, 11, 13, 15)
- Uses special summary files with 15+ outputs per sample (path_15_summary.txt, etc.)
- Simulates majority voting by sampling k voters from all available outputs
- Generates detailed reports, plots, and statistical analysis
- Helps determine optimal voter count for ensemble methods

SUPPORTED DATASETS:
- AR-LSAT: Multiple choice (0-4 indices), pruning criteria: single valid index
- ProofWriter: Boolean logic (True/False/Unknown), pruning criteria: single valid boolean
- FOLIO: Boolean logic (True/False/Unknown), pruning criteria: single valid boolean  
- ProntoQA: Boolean logic (True/False), pruning criteria: single valid boolean
- LogicalDeduction: Multiple choice (A-G letters), pruning criteria: single valid letter

The script automatically detects the dataset from config.yaml and applies appropriate parsing and pruning rules.

KEY FEATURES:
- Enhanced syntax error handling: Missing paths (when samples have <5 outputs) are counted as syntax errors
- Dual format output: Automatically saves both CSV and XLSX formats
- Smart model extraction: Extracts sketch-gen and code-gen models from filename when not in config
- Flexible file detection: Finds summary.txt in main directory or summary/ subdirectory
- Path pruning annotation: SketchFormal method marked with "yes" for all pruning columns

By default, only SketchFormal method is run. Use --all-methods flag to run all three methods.

=== OUTPUT DIRECTORIES ===
- CSV files: ./standard-experiments/
- XLSX files: ./standard-experiments-xlsx/
- Detailed JSON: [original_experiment_directory]/detailed_ablation_results.json

=== PARAMETER MEANINGS ===

Core Experiment Info:
- ID: Unique identifier for the experimental run
- Benchmarks: Dataset name (extracted from config.yaml "dataset" field)
- #shots in ICL: Number of in-context learning examples (0=zero-shot, 3=three-shot, etc.)
- ICL sample source: Source of ICL examples ("logic-lm autoformalization ICL")
- sketch: Whether sketch/planning is used ("yes" for two-step, "no" for one-step/cot)
- #total samples: Total number of samples

Path Generation:
- K (#paths per sample): Expected number of generated paths per sample (default: 5)
- path pruning: "yes" for SketchFormal and Ablation Study 2, "no" for Ablation Study 1
- path pruning (existence): "yes" for SketchFormal and Ablation Study 2, "no" for Ablation Study 1
- path pruning (uniqueness): "yes" for SketchFormal and Ablation Study 2, "no" for Ablation Study 1
- ensemble: "yes" for SketchFormal and Ablation Study 1 (majority vote), "no" for Ablation Study 2

Model Configuration:
- sketch-gen model: Model used for sketch/plan generation (from config or extracted from filename)
- code-gen model: Model used for code generation (from config or extracted from filename)
- sketch temp: Temperature for sketch generation (default: 1)
- code temp: Temperature for code generation (default: 0)

Error Analysis:
- #samples failed by syntax error: Number of samples with at least one syntax error (including missing paths)
- #paths failed by syntax error: Total number of paths with syntax errors (including missing paths)
- syntax error rate: Ratio of syntax error paths to total expected paths

Path Statistics:
- Total #paths before pruning: Total expected paths across all samples (samples × expected_paths_per_sample)
- Total #paths after pruning: Total paths after applying method-specific filtering
- Avg #paths before pruning: Average expected paths per sample
- Avg #paths after pruning: Average paths per sample after filtering

Performance Metrics:
- tied voting rate: Ratio of samples with tied votes (multiple answers with same max votes)
- #samples with auto-formalization failure: Number of samples where no valid answer could be extracted
- backup method: Fallback method used when primary extraction fails (currently "none")
- overall accuracy: Sample-level accuracy (correct samples / total samples)
- accuracy by path: Path-level accuracy (correct paths / syntactically correct paths)

=== USAGE ===

Basic Commands:
    # Run only SketchFormal method (default)
    python custom_ablation_analysis.py <results_directory>
    
    # Run all three methods
    python custom_ablation_analysis.py <results_directory> --all-methods
    
    # Run specific methods
    python custom_ablation_analysis.py <results_directory> --methods sketchformal ablation_study_1
    
    # Specify expected paths per sample (when not all samples have 30 paths due to syntax errors)
    python custom_ablation_analysis.py <results_directory> --path-ablation --expected-paths 5
    
    # Run pruning ablation study
    python custom_ablation_analysis.py <results_directory> --pruning-ablation
    
Examples:
    python custom_ablation_analysis.py results/experiment_folder/
    python custom_ablation_analysis.py results/experiment_folder/ --all-methods
    python custom_ablation_analysis.py results/experiment_folder/ --path-ablation --expected-paths 5
    python custom_ablation_analysis.py results/experiment_folder/ --pruning-ablation

=== MODEL EXTRACTION ===
If sketch-gen model and code-gen model are not found in config.yaml, the script automatically
extracts them from the experiment directory name using patterns like:
- "generate-with-gpt-4-fix-with-gpt-4" → sketch-gen: gpt-4, code-gen: gpt-4

=== SYNTAX ERROR HANDLING ===
The script handles cases where all_solver_outputs has fewer than expected paths:
- Missing paths are automatically counted as syntax errors
- Total paths before pruning uses expected count (default: 5 per sample)
- Provides accurate syntax error rates and statistics

Example: If a sample has only 3 outputs instead of 5, the 2 missing outputs are counted as syntax errors.
"""

import json
import pandas as pd
import yaml
import ast
import argparse
from collections import Counter
import re
import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_results(results_file):
    """Load results from JSON or TXT file containing JSON."""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict) and "results" in data:
                return data["results"]
            elif isinstance(data, list):
                return data
            else:
                return data
    except Exception as e:
        print(f"Error loading results file: {e}")
        return []

def parse_solver_output(output_str, dataset=None):
    """Parse solver output string to extract list of answers based on dataset format."""
    try:
        # Check for syntax error pattern first
        if isinstance(output_str, str) and "error" in output_str.lower():
            return 'syntax error'
        
        # Handle different dataset formats
        if dataset and dataset.lower() in ['proofwriter', 'folio', 'prontoqa']:
            # Boolean-based datasets: True, False, Unknown
            if isinstance(output_str, str):
                output_clean = output_str.strip()
                if output_clean in ['True', 'False', 'Unknown']:
                    return [output_clean]
                elif output_clean == 'multiple answers':
                    return ['multiple answers']
                else:
                    return []
            return []
        
        elif dataset and dataset.lower() == 'logicaldeduction':
            # Letter-based dataset: A, B, C, D, E, F, G
            if isinstance(output_str, str):
                output_clean = output_str.strip()
                valid_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                if output_clean in valid_letters:
                    return [output_clean]
                else:
                    # Try to extract from lines
                    lines = [line.strip() for line in output_clean.split('\n') if line.strip()]
                    unique_lines = list(set(lines))
                    if len(unique_lines) == 1 and unique_lines[0] in valid_letters:
                        return [unique_lines[0]]
                    elif len(unique_lines) > 1:
                        return ['multiple answers']
                    else:
                        return []
            return []
        
        else:
            # AR-LSAT format: Handle string representations of lists like "[2]", "[]", etc.
            if isinstance(output_str, str):
                # Try to parse as Python literal
                parsed = ast.literal_eval(output_str)
                if isinstance(parsed, list):
                    return parsed
                else:
                    return [parsed] if parsed is not None else []
            elif isinstance(output_str, list):
                return output_str
            else:
                return []
    except:
        # Fallback parsing
        if dataset and dataset.lower() == 'logicaldeduction':
            # Try to extract letters
            letters = re.findall(r'\b[A-G]\b', str(output_str))
            return letters if letters else []
        else:
            # Try to extract numbers for AR-LSAT
            try:
                numbers = re.findall(r'\d+', str(output_str))
                return [int(n) for n in numbers]
            except:
                return []

def _flatten(nested_list):
    """Flatten arbitrarily nested lists into a flat list (non-list elements)."""
    for item in nested_list:
        if isinstance(item, list):
            yield from _flatten(item)
        else:
            yield item

def load_config(config_file):
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

def extract_config_info(config, exp_id):
    """Extract information from config and experiment ID."""
    # Extract shots from config
    shots_mapping = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }
    shots_str = config.get('shots', 'zero')
    shots = shots_mapping.get(shots_str, 0)
    
    # Check if sketch is used based on reasoning method
    reasoning_method = config.get('reasoning_method', '').lower()
    if 'two-step' in reasoning_method:
        has_sketch = True
    elif 'one-step' in reasoning_method or 'cot' in reasoning_method:
        has_sketch = False
    else:
        # Fallback: check if plan_model exists
        has_sketch = config.get('plan_model') is not None
    
    # Extract model information from config or filename
    plan_model = config.get('plan_model', '')
    code_model = config.get('code_model', '')
    
    # If models not found in config, extract from experiment ID filename
    if not plan_model or not code_model:
        # Look for pattern like "generate-with-gpt-4-fix-with-gpt-4"
        import re
        pattern = r'generate-with-(gpt-[^-]+)-fix-with-(gpt-[^-]+)'
        match = re.search(pattern, exp_id)
        if match:
            if not plan_model:
                plan_model = match.group(1)
            if not code_model:
                code_model = match.group(2)
    
    return {
        'shots': shots,
        'has_sketch': has_sketch,
        'plan_model': plan_model,
        'code_model': code_model
    }

def create_comprehensive_csv(results_dir, summary_file, config_file, dataset, *results, args):
    """Create comprehensive CSV file with all required columns."""
    
    # Load config
    config = load_config(config_file)
    
    # Extract experiment ID from directory name
    exp_id = os.path.basename(results_dir.rstrip('/'))
    
    # Extract config info
    config_info = extract_config_info(config, exp_id)
    
    # Create rows for all methods
    rows = []
    
    for i, result in enumerate(results):
        # Determine attributes based on method (VVV pattern: Sketch Plans, Multi-path, Semantic Pruning)
        method_name = result['method']
        
        # Method configurations based on VVV pattern
        method_configs = {
            'sketchformal': {'sketch': 'yes', 'multipath': 'yes', 'pruning': 'yes'},  # VVV
            'direct_translation_multipath_pruning': {'sketch': 'no', 'multipath': 'yes', 'pruning': 'yes'},  # XVV
            'sketchformal_pruning_only': {'sketch': 'yes', 'multipath': 'no', 'pruning': 'yes'},  # VXV
            'sketchformal_majority_vote': {'sketch': 'yes', 'multipath': 'yes', 'pruning': 'no'},  # VVX
            'direct_translation': {'sketch': 'no', 'multipath': 'no', 'pruning': 'no'},  # XXX
            'sketch_only': {'sketch': 'yes', 'multipath': 'no', 'pruning': 'no'},  # VXX
            'direct_translation_multipath': {'sketch': 'no', 'multipath': 'yes', 'pruning': 'no'},  # XVX
            'direct_translation_pruning': {'sketch': 'no', 'multipath': 'no', 'pruning': 'yes'},  # XXV
            # Pruning ablation methods
            'existence_pruning_majority_vote': {'sketch': 'yes', 'multipath': 'yes', 'pruning': 'existence'},  # Special pruning
            'uniqueness_pruning_majority_vote': {'sketch': 'yes', 'multipath': 'yes', 'pruning': 'uniqueness'},  # Special pruning
        }
        
        # Handle path ablation methods dynamically
        if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            # Path ablation methods use same settings as sketchformal but with different number of paths
            config = {'sketch': 'yes' if config_info['has_sketch'] else 'no', 'multipath': 'yes', 'pruning': 'yes'}
        else:
            config = method_configs.get(method_name, {'sketch': '', 'multipath': '', 'pruning': ''})
        
        # Set path pruning columns based on semantic pruning
        if config['pruning'] == 'yes':
            path_pruning = 'yes'
            path_pruning_existence = 'yes' 
            path_pruning_uniqueness = 'yes'
        elif config['pruning'] == 'no':
            path_pruning = 'no'
            path_pruning_existence = 'no'
            path_pruning_uniqueness = 'no'
        elif config['pruning'] == 'existence':
            path_pruning = 'yes'
            path_pruning_existence = 'yes'
            path_pruning_uniqueness = 'no'
        elif config['pruning'] == 'uniqueness':
            path_pruning = 'yes'
            path_pruning_existence = 'no'
            path_pruning_uniqueness = 'yes'
        else:
            path_pruning = ''
            path_pruning_existence = ''
            path_pruning_uniqueness = ''
        
        # Set ensemble based on multi-path exploration
        ensemble = 'yes' if config['multipath'] == 'yes' else ('no' if config['multipath'] == 'no' else '')
        
        # Override sketch value based on method (for display purposes)
        sketch_value = config['sketch'] if config['sketch'] else ('yes' if config_info['has_sketch'] else 'no')
        
        # Determine actual paths per sample for this method
        method_name = result['method']
        if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            # For path ablation, K should be the number of paths actually used
            actual_paths_per_sample = int(method_name.split('_')[2])  # Extract number from 'path_ablation_X_paths'
        else:
            # For other methods (like sketchformal), use the maximum number of paths available
            actual_paths_per_sample = args.expected_paths
        
        row = {
            'ID': f"{exp_id}_{result['method']}",
            'Benchmarks': dataset.upper(),
            '#shots in ICL': config_info['shots'],
            'ICL sample source': 'logic-lm autoformalization ICL',
            'sketch': sketch_value,
            '#total samples': result['total'],
            'K (#paths per sample)': actual_paths_per_sample,
            'path pruning': path_pruning,
            'path pruning (existence)': path_pruning_existence,
            'path pruning (uniqueness)': path_pruning_uniqueness,
            'ensemble': ensemble,
            'sketch-gen model': config_info['plan_model'],
            'code-gen model': config_info['code_model'],
            'sketch temp': 1,  # Default value as specified
            'code temp': 0,  # Default value as specified
            '#samples failed by syntax error': len([d for d in result['details'] if d['syntax_error_count'] > 0]),
            '#paths failed by syntax error': result['syntax_errors'],
            'syntax error rate': result['syntax_errors'] / result['total_paths_before'] if result['total_paths_before'] > 0 else 0,
            'Total #paths before pruning': result['total_paths_before'],
            'Total #paths after pruning': result['total_paths_after'],
            'Avg #paths before pruning': result['avg_paths_before'],
            'Avg #paths after pruning': result['avg_paths_after'],
            'tied voting rate': result.get('tied_voting_rate', 0),
            '#samples with auto-formalization failure': result['failed_extractions'],
            'backup method': 'none',
            'overall accuracy': result['accuracy'],
            'accuracy by path (successfully auto-formalized only, discard those with syntax errors)': result['accuracy_by_path']
        }
        rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Save to both CSV and XLSX formats
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(script_dir, 'standard-experiments')
    xlsx_dir = os.path.join(script_dir, 'standard-experiments-xlsx')
    
    # Create directories if they don't exist
    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(xlsx_dir, exist_ok=True)
    
    # Save CSV file
    csv_filename = f"{exp_id}.csv"
    csv_output_file = os.path.join(csv_dir, csv_filename)
    df.to_csv(csv_output_file, index=False)
    
    # Save XLSX file
    xlsx_filename = f"{exp_id}.xlsx"
    xlsx_output_file = os.path.join(xlsx_dir, xlsx_filename)
    try:
        df.to_excel(xlsx_output_file, index=False, engine='openpyxl')
        xlsx_saved = True
    except ImportError:
        print("Warning: openpyxl not installed. XLSX file not saved. Install with: pip install openpyxl")
        xlsx_saved = False
    
    return df, csv_output_file, xlsx_output_file if xlsx_saved else None

def calculate_path_level_metrics(all_solver_outputs, true_label, dataset=None):
    """Calculate path-level metrics for accuracy by path calculation."""
    correct_paths = 0
    syntactic_correct_paths = 0
    
    for output_str in all_solver_outputs:
        parsed_output = parse_solver_output(output_str, dataset)
        if parsed_output != 'syntax error':
            syntactic_correct_paths += 1
            flat_output = list(_flatten(parsed_output))
            if len(flat_output) == 1:
                try:
                    path_answer = flat_output[0]
                    
                    # Handle different answer formats
                    if dataset and dataset.lower() == 'ar-lsat':
                        # AR-LSAT: numeric comparison
                        path_answer = int(path_answer)
                        true_label_int = int(true_label)
                        if path_answer == true_label_int:
                            correct_paths += 1
                    else:
                        # Other datasets: string comparison
                        if str(path_answer) == str(true_label):
                            correct_paths += 1
                except (ValueError, TypeError):
                    pass
    
    return correct_paths, syntactic_correct_paths

def extract_answer_majority_vote(all_solver_outputs, dataset=None):
    """Extract answer using majority vote across all outputs."""
    if not all_solver_outputs:
        return None, False  # predicted_answer, has_tied_voting
    
    # Count frequency of each complete output string
    output_counts = Counter(all_solver_outputs)
    
    # Check for tied voting
    has_tied_voting = False
    if len(output_counts) > 1:
        vote_counts = list(output_counts.values())
        max_votes = max(vote_counts)
        tied_count = sum(1 for count in vote_counts if count == max_votes)
        if tied_count > 1:
            has_tied_voting = True
    
    most_frequent_output = output_counts.most_common(1)[0][0]
    
    # Parse the most frequent output to get the answer list
    parsed_output = parse_solver_output(most_frequent_output, dataset)
    flat_output = list(_flatten(parsed_output))
    
    # Extract the answer from the majority vote result
    if len(flat_output) == 0 or parsed_output == 'syntax error':
        return None, has_tied_voting
    
    # Return the appropriate answer format based on dataset
    if dataset and dataset.lower() in ['proofwriter', 'folio', 'prontoqa', 'logicaldeduction']:
        return flat_output[0], has_tied_voting  # String format
    else:
        # AR-LSAT numeric format
        try:
            predicted_answer = int(flat_output[0])
            return predicted_answer, has_tied_voting
        except (ValueError, TypeError):
            if isinstance(flat_output[0], int):
                return flat_output[0], has_tied_voting
            else:
                return None, has_tied_voting

def apply_existence_pruning(all_solver_outputs, dataset=None):
    """Apply existence pruning: keep only outputs with length >= 1 (can be satisfied)."""
    filtered_outputs = []
    for output_str in all_solver_outputs:
        parsed_output = parse_solver_output(output_str, dataset)
        if parsed_output != 'syntax error':
            flat_output = list(_flatten(parsed_output))
            if len(flat_output) >= 1:  # Can be satisfied (has at least one solution)
                filtered_outputs.append(output_str)
    return filtered_outputs

def apply_uniqueness_pruning(all_solver_outputs, dataset=None):
    """Apply uniqueness pruning: keep only outputs with length <= 1 (unique solution)."""
    filtered_outputs = []
    for output_str in all_solver_outputs:
        parsed_output = parse_solver_output(output_str, dataset)
        if parsed_output != 'syntax error':
            flat_output = list(_flatten(parsed_output))
            if len(flat_output) <= 1:  # Unique solution
                filtered_outputs.append(output_str)
    return filtered_outputs

def extract_answer_existence_pruning_majority_vote(all_solver_outputs, dataset=None):
    """Extract answer using existence pruning then majority vote."""
    filtered_outputs = apply_existence_pruning(all_solver_outputs, dataset)
    if not filtered_outputs:
        return None, False
    return extract_answer_majority_vote(filtered_outputs, dataset)

def extract_answer_uniqueness_pruning_majority_vote(all_solver_outputs, dataset=None):
    """Extract answer using uniqueness pruning then majority vote."""
    filtered_outputs = apply_uniqueness_pruning(all_solver_outputs, dataset)
    if not filtered_outputs:
        return None, False
    return extract_answer_majority_vote(filtered_outputs, dataset)


def extract_answer_first_list(all_solver_outputs, dataset=None):
    """Extract answer from first output that meets pruning criteria."""
    if not all_solver_outputs:
        return None
    
    first_output = all_solver_outputs[0]
    parsed_output = parse_solver_output(first_output, dataset)
    
    if parsed_output != 'syntax error':
        flat_output = list(_flatten(parsed_output))
        
        # Check pruning criteria based on dataset
        if len(flat_output) == 1:
            if dataset and dataset.lower() == 'ar-lsat':
                # AR-LSAT: value 0-4
                try:
                    value = int(flat_output[0])
                    if 0 <= value <= 4:
                        return value
                except (ValueError, TypeError):
                    pass
            elif dataset and dataset.lower() in ['proofwriter', 'folio']:
                # ProofWriter/FOLIO: True, False, Unknown
                if flat_output[0] in ['True', 'False', 'Unknown']:
                    return flat_output[0]
            elif dataset and dataset.lower() == 'prontoqa':
                # ProntoQA: True, False only
                if flat_output[0] in ['True', 'False']:
                    return flat_output[0]
            elif dataset and dataset.lower() == 'logicaldeduction':
                # LogicalDeduction: A-G
                if flat_output[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                    return flat_output[0]
            else:
                # Default AR-LSAT behavior for backward compatibility
                try:
                    value = int(flat_output[0])
                    if 0 <= value <= 4:
                        return value
                except (ValueError, TypeError):
                    pass
    
    return None

def extract_answer_pruning_majority_vote(all_solver_outputs, dataset=None):
    """Extract answer using pruning criteria first, then majority vote on filtered outputs."""
    if not all_solver_outputs:
        return None, False  # predicted_answer, has_tied_voting
    
    # Step 1: Apply pruning criteria to filter valid outputs
    filtered_outputs = []
    for output_str in all_solver_outputs:
        parsed_output = parse_solver_output(output_str, dataset)
        
        if parsed_output != 'syntax error':
            flat_output = list(_flatten(parsed_output))
            
            # Check pruning criteria based on dataset
            if len(flat_output) == 1:
                is_valid = False
                if dataset and dataset.lower() == 'ar-lsat':
                    # AR-LSAT: value 0-4
                    try:
                        value = int(flat_output[0])
                        if 0 <= value <= 4:
                            is_valid = True
                    except (ValueError, TypeError):
                        continue
                elif dataset and dataset.lower() in ['proofwriter', 'folio']:
                    # ProofWriter/FOLIO: True, False, Unknown
                    if flat_output[0] in ['True', 'False', 'Unknown']:
                        is_valid = True
                elif dataset and dataset.lower() == 'prontoqa':
                    # ProntoQA: True, False only
                    if flat_output[0] in ['True', 'False']:
                        is_valid = True
                elif dataset and dataset.lower() == 'logicaldeduction':
                    # LogicalDeduction: A-G
                    if flat_output[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                        is_valid = True
                else:
                    # Default AR-LSAT behavior for backward compatibility
                    try:
                        value = int(flat_output[0])
                        if 0 <= value <= 4:
                            is_valid = True
                    except (ValueError, TypeError):
                        continue
                
                if is_valid:
                    filtered_outputs.append(output_str)
    
    # Step 2: If no outputs pass pruning criteria, return None
    if not filtered_outputs:
        return None, False
    
    # Step 3: Apply majority vote on filtered outputs
    output_counts = Counter(filtered_outputs)
    
    # Check for tied voting
    has_tied_voting = False
    if len(output_counts) > 1:
        vote_counts = list(output_counts.values())
        max_votes = max(vote_counts)
        tied_count = sum(1 for count in vote_counts if count == max_votes)
        if tied_count > 1:
            has_tied_voting = True
    
    most_frequent_output = output_counts.most_common(1)[0][0]
    
    # Parse the most frequent filtered output to get the answer
    parsed_output = parse_solver_output(most_frequent_output, dataset)
    flat_output = list(_flatten(parsed_output))
    
    if len(flat_output) == 0 or parsed_output == 'syntax error':
        return None, has_tied_voting
    
    # Return the appropriate answer format based on dataset
    if dataset and dataset.lower() in ['proofwriter', 'folio', 'prontoqa', 'logicaldeduction']:
        return flat_output[0], has_tied_voting  # String format
    else:
        # AR-LSAT numeric format
        try:
            predicted_answer = int(flat_output[0])
            return predicted_answer, has_tied_voting
        except (ValueError, TypeError):
            if isinstance(flat_output[0], int):
                return flat_output[0], has_tied_voting
            else:
                return None, has_tied_voting

def calculate_accuracy_generic(results, method_name, extraction_func, dataset=None, expected_paths_per_sample=30):
    """Generic function to calculate accuracy for any extraction method."""
    correct = 0
    total = 0
    failed_extractions = 0
    syntax_errors = 0
    total_paths_before = 0
    total_paths_after = 0
    correct_paths = 0
    syntactic_correct_paths = 0
    tied_voting_samples = 0
    details = []
    
    # For path ablation methods, determine the actual number of paths used
    if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
        paths_used_per_sample = int(method_name.split('_')[2])  # Extract number from 'path_ablation_X_paths'
    else:
        paths_used_per_sample = expected_paths_per_sample
    
    for item in results:
        if 'problem' not in item:
            continue
        
        # 'label' for AR-LSAT, 'answer' for others
        if 'label' in item['problem']:
            true_label = item['problem']['label']
        elif 'answer' in item['problem']:
            true_label = item['problem']['answer']
        else:
            continue
            
        all_solver_outputs = item.get('all_solver_outputs', [])
        
        # For path ablation methods, limit to only the first n paths
        if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            all_solver_outputs = all_solver_outputs[:paths_used_per_sample]
        
        total += 1
        
        # Calculate total paths before pruning, accounting for missing paths due to syntax errors
        actual_paths = len(all_solver_outputs)
        # For path ablation, we only count the paths we actually use
        # Missing paths are considered syntax errors only up to the number we need
        missing_paths = max(0, paths_used_per_sample - actual_paths)
        total_paths_before += paths_used_per_sample
        
        # Count syntax errors in existing outputs plus missing paths
        explicit_syntax_errors = sum(1 for output in all_solver_outputs if "error" in str(output).lower())
        syntax_error_count = explicit_syntax_errors + missing_paths
        syntax_errors += syntax_error_count
        
        # Calculate path-level metrics
        item_correct_paths, item_syntactic_correct_paths = calculate_path_level_metrics(all_solver_outputs, true_label, dataset)
        correct_paths += item_correct_paths
        syntactic_correct_paths += item_syntactic_correct_paths
        
        # Extract answer using the provided extraction function (all functions now take dataset parameter)
        extraction_result = extraction_func(all_solver_outputs, dataset)
        
        # Determine method characteristics
        multipath_methods = ['sketchformal', 'direct_translation_multipath_pruning', 'sketchformal_majority_vote', 'direct_translation_multipath',
                            'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']
        pruning_methods = ['sketchformal', 'direct_translation_multipath_pruning', 'sketchformal_pruning_only', 'direct_translation_pruning',
                          'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']
        
        # Add path ablation methods to multipath_methods (they use majority voting)
        if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            multipath_methods.append(method_name)
            pruning_methods.append(method_name)  # Path ablation methods also use pruning
        
        # Handle different return types from extraction functions
        if method_name in multipath_methods:  # Methods using majority vote
            predicted_answer, has_tied_voting = extraction_result
            if has_tied_voting:
                tied_voting_samples += 1
        else:  # Single path methods
            predicted_answer = extraction_result
            has_tied_voting = False
        
        # Calculate paths after pruning based on method type
        if method_name in pruning_methods:
            # Pruning methods: count valid outputs that pass pruning criteria
            pruned_count = 0
            for output_str in all_solver_outputs:
                parsed_output = parse_solver_output(output_str, dataset)
                if parsed_output != 'syntax error':
                    flat_output = list(_flatten(parsed_output))
                    if len(flat_output) == 1:
                        is_valid = False
                        if dataset and dataset.lower() == 'ar-lsat':
                            try:
                                value = int(flat_output[0])
                                if 0 <= value <= 4:
                                    is_valid = True
                            except (ValueError, TypeError):
                                continue
                        elif dataset and dataset.lower() in ['proofwriter', 'folio']:
                            if flat_output[0] in ['True', 'False', 'Unknown']:
                                is_valid = True
                        elif dataset and dataset.lower() == 'prontoqa':
                            if flat_output[0] in ['True', 'False']:
                                is_valid = True
                        elif dataset and dataset.lower() == 'logicaldeduction':
                            if flat_output[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                                is_valid = True
                        else:
                            # Default AR-LSAT behavior
                            try:
                                value = int(flat_output[0])
                                if 0 <= value <= 4:
                                    is_valid = True
                            except (ValueError, TypeError):
                                continue
                        
                        if is_valid:
                            pruned_count += 1
            if method_name in multipath_methods:
                paths_after_pruning = pruned_count
            else:
                paths_after_pruning = 1 if predicted_answer is not None else 0
        else:
            # No pruning methods: use all paths or single path
            if method_name in multipath_methods:
                paths_after_pruning = len(all_solver_outputs)
            else:
                paths_after_pruning = 1 if predicted_answer is not None else 0
        
        total_paths_after += paths_after_pruning
        
        if predicted_answer is None:
            failed_extractions += 1
        
        # Handle different answer format comparisons
        is_correct = False
        if predicted_answer is not None:
            if dataset and dataset.lower() == 'ar-lsat':
                # AR-LSAT: numeric comparison
                try:
                    pred_int = int(predicted_answer)
                    true_int = int(true_label)
                    is_correct = pred_int == true_int
                except (ValueError, TypeError):
                    is_correct = False
            elif dataset and dataset.lower() in ['proofwriter', 'prontoqa']:
                is_correct = (predicted_answer == "True" and true_label == "A") or \
                             (predicted_answer == "False" and true_label == "B") or \
                             (predicted_answer == "Unknown" and true_label == "C")
            else:
                # Other datasets: string comparison
                is_correct = str(predicted_answer) == str(true_label)
        
        if is_correct:
            correct += 1
            
        details.append({
            'id': item['problem'].get('id_string', item['problem'].get('id', f'item_{total}')),
            'true_label': true_label,
            'predicted': predicted_answer,
            'correct': is_correct,
            'all_outputs': all_solver_outputs,
            'actual_paths': actual_paths,
            'expected_paths': expected_paths_per_sample,
            'missing_paths': missing_paths,
            'explicit_syntax_errors': explicit_syntax_errors,
            'syntax_error_count': syntax_error_count,
            'paths_after_pruning': paths_after_pruning
        })
    
    accuracy = correct / total if total > 0 else 0
    accuracy_by_path = correct_paths / syntactic_correct_paths if syntactic_correct_paths > 0 else 0
    tied_voting_rate = tied_voting_samples / total if total > 0 else 0
    
    return {
        'method': method_name,
        'correct': correct,
        'total': total,
        'accuracy': accuracy,
        'failed_extractions': failed_extractions,
        'syntax_errors': syntax_errors,
        'total_paths_before': total_paths_before,
        'total_paths_after': total_paths_after,
        'avg_paths_before': total_paths_before / total if total > 0 else 0,
        'avg_paths_after': total_paths_after / total if total > 0 else 0,
        'correct_paths': correct_paths,
        'syntactic_correct_paths': syntactic_correct_paths,
        'accuracy_by_path': accuracy_by_path,
        'tied_voting_samples': tied_voting_samples,
        'tied_voting_rate': tied_voting_rate,
        'details': details
    }

def calculate_accuracy_sketchformal(results, dataset=None, expected_paths_per_sample=5):
    """SketchFormal (VVV): Sketch Plans + Multi-path + Semantic Pruning."""
    return calculate_accuracy_generic(results, 'sketchformal', extract_answer_pruning_majority_vote, dataset, expected_paths_per_sample)

def calculate_accuracy_direct_translation_multipath_pruning(results, dataset=None, expected_paths_per_sample=5):
    """Direct translation with multi-path and pruning (XVV): No sketch + Multi-path + Semantic Pruning."""
    return calculate_accuracy_generic(results, 'direct_translation_multipath_pruning', extract_answer_pruning_majority_vote, dataset, expected_paths_per_sample)

def calculate_accuracy_sketchformal_pruning_only(results, dataset=None, expected_paths_per_sample=5):
    """SketchFormal with semantic pruning only (VXV): Sketch Plans + Single path + Semantic Pruning."""
    return calculate_accuracy_generic(results, 'sketchformal_pruning_only', extract_answer_first_list, dataset, expected_paths_per_sample)

def calculate_accuracy_sketchformal_majority_vote(results, dataset=None, expected_paths_per_sample=5):
    """SketchFormal with majority vote (VVX): Sketch Plans + Multi-path + No pruning."""
    return calculate_accuracy_generic(results, 'sketchformal_majority_vote', extract_answer_majority_vote, dataset, expected_paths_per_sample)

def calculate_accuracy_direct_translation(results, dataset=None, expected_paths_per_sample=5):
    """Direct translation (XXX): No sketch + Single path + No pruning."""
    return calculate_accuracy_generic(results, 'direct_translation', extract_answer_first_list, dataset, expected_paths_per_sample)

def calculate_accuracy_sketch_only(results, dataset=None, expected_paths_per_sample=5):
    """Sketch-only (VXX): Sketch Plans + Single path + No pruning."""
    return calculate_accuracy_generic(results, 'sketch_only', extract_answer_first_list, dataset, expected_paths_per_sample)

def calculate_accuracy_direct_translation_multipath(results, dataset=None, expected_paths_per_sample=5):
    """Direct translation with multi-path (XVX): No sketch + Multi-path + No pruning."""
    return calculate_accuracy_generic(results, 'direct_translation_multipath', extract_answer_majority_vote, dataset, expected_paths_per_sample)

def calculate_accuracy_direct_translation_pruning(results, dataset=None, expected_paths_per_sample=5):
    """Direct translation with pruning (XXV): No sketch + Single path + Semantic Pruning."""
    return calculate_accuracy_generic(results, 'direct_translation_pruning', extract_answer_first_list, dataset, expected_paths_per_sample)

# Voter Sensitivity Analysis Functions
def parse_solver_output_for_voting(output_str: str, dataset=None):
    """Parse solver output string to list of integers for voting analysis."""
    if dataset and dataset.lower() == 'ar-lsat':
        try:
            # Remove brackets and split by comma
            cleaned = output_str.strip('[]')
            if not cleaned:
                return []
            return [int(x.strip()) for x in cleaned.split(',')]
        except:
            return []
    else:
        # Use existing parsing logic for other datasets
        parsed = parse_solver_output(output_str, dataset)
        if parsed == 'syntax error':
            return []
        return list(_flatten(parsed))

def is_valid_single_answer_for_voting(output_str: str, dataset=None):
    """Check if output is a valid single answer for voting."""
    try:
        parsed = parse_solver_output_for_voting(output_str, dataset)
        if dataset and dataset.lower() == 'ar-lsat':
            return len(parsed) == 1 and 0 <= parsed[0] <= 4
        elif dataset and dataset.lower() in ['proofwriter', 'folio']:
            return len(parsed) == 1 and parsed[0] in ['True', 'False', 'Unknown']
        elif dataset and dataset.lower() == 'prontoqa':
            return len(parsed) == 1 and parsed[0] in ['True', 'False']
        elif dataset and dataset.lower() == 'logicaldeduction':
            return len(parsed) == 1 and parsed[0] in ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        else:
            # Default AR-LSAT behavior
            return len(parsed) == 1 and 0 <= parsed[0] <= 4
    except:
        return False

def filter_valid_outputs_for_voting(solver_outputs, dataset=None):
    """Filter solver outputs to only include valid single answers."""
    return [output for output in solver_outputs if is_valid_single_answer_for_voting(output, dataset)]

def get_majority_vote_from_outputs(solver_outputs, dataset=None):
    """Calculate majority vote from filtered valid solver outputs."""
    # Filter to only valid single answers
    valid_outputs = filter_valid_outputs_for_voting(solver_outputs, dataset)
    
    if not valid_outputs:
        return None  # No valid outputs
    
    # Extract the single answer from each valid output
    answers = []
    for output in valid_outputs:
        parsed = parse_solver_output_for_voting(output, dataset)
        if len(parsed) == 1:
            answers.append(parsed[0])
    
    if not answers:
        return None
    
    # Count occurrences and get majority
    counter = Counter(answers)
    most_common = counter.most_common(1)[0]
    return most_common[0]

def simulate_voting_with_n_voters(all_outputs, n_voters: int, num_simulations: int = 100, dataset=None):
    """
    Simulate majority voting with n voters by:
    1. First sampling n candidates from all available outputs
    2. Then filtering the sampled candidates to only valid single answers
    3. Finally performing majority vote on the filtered results
    """
    if len(all_outputs) == 0:
        return [None] * num_simulations
    
    results = []
    
    for _ in range(num_simulations):
        # Step 1: Sample k candidates from all available outputs
        if len(all_outputs) >= n_voters:
            sampled_candidates = random.sample(all_outputs, n_voters)
        else:
            # If we don't have enough outputs, sample with replacement
            sampled_candidates = random.choices(all_outputs, k=n_voters)
        
        # Step 2 & 3: Filter and get majority vote
        majority_vote = get_majority_vote_from_outputs(sampled_candidates, dataset)
        results.append(majority_vote)
    
    return results

# Pruning ablation study methods
def calculate_accuracy_existence_pruning_majority_vote(results, dataset=None, expected_paths_per_sample=5):
    """Existence pruning + majority vote: Keep outputs with length >= 1."""
    return calculate_accuracy_generic(results, 'existence_pruning_majority_vote', extract_answer_existence_pruning_majority_vote, dataset, expected_paths_per_sample)

def calculate_accuracy_uniqueness_pruning_majority_vote(results, dataset=None, expected_paths_per_sample=5):
    """Uniqueness pruning + majority vote: Keep outputs with length <= 1."""
    return calculate_accuracy_generic(results, 'uniqueness_pruning_majority_vote', extract_answer_uniqueness_pruning_majority_vote, dataset, expected_paths_per_sample)

# Path ablation study methods (same as voter sensitivity but integrated into main analysis)
def extract_answer_path_ablation_majority_vote(all_solver_outputs, dataset=None, num_paths=5):
    """Extract answer using majority vote with a specific number of paths (same as voter sensitivity)."""
    if not all_solver_outputs:
        return None, False
    
    # Since all_solver_outputs has already been sliced to the first num_paths in calculate_accuracy_generic,
    # we just need to apply majority vote to all available outputs
    return extract_answer_pruning_majority_vote(all_solver_outputs, dataset)

def calculate_accuracy_path_ablation(results, num_paths, dataset=None, expected_paths_per_sample=5):
    """Calculate accuracy using a specific number of paths with majority vote."""
    def extraction_func(all_solver_outputs, dataset_param=None):
        return extract_answer_path_ablation_majority_vote(all_solver_outputs, dataset_param, num_paths)
    
    method_name = f'path_ablation_{num_paths}_paths'
    return calculate_accuracy_generic(results, method_name, extraction_func, dataset, expected_paths_per_sample)


def generate_path_counts_from_config(num_paths):
    """Generate appropriate path counts based on the num_paths parameter from config.yaml."""
    if num_paths <= 0:
        print("Warning: Invalid num_paths in config, using default path counts [1, 3, 5]")
        return [1, 3, 5]
    
    # Generate path counts: start with 1, then odd numbers up to num_paths, then num_paths if even
    path_counts = [1]
    
    # Add odd numbers up to num_paths
    for i in range(3, num_paths + 1, 2):
        path_counts.append(i)
    
    # Add num_paths if it's even and not already included
    if num_paths % 2 == 0 and num_paths not in path_counts:
        path_counts.append(num_paths)
    
    print(f"Config num_paths: {num_paths}")
    print(f"Generated path counts for ablation: {path_counts}")
    
    return path_counts


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Analyze experimental results with SketchFormal method (primary) and optional ablation studies.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Run only SketchFormal method (default)
    python custom_ablation_analysis.py results/experiment_folder/
    
    # Run all three methods
    python custom_ablation_analysis.py results/experiment_folder/ --all-methods
    
    # Run specific methods
    python custom_ablation_analysis.py results/experiment_folder/ --methods sketchformal ablation_study_1
        """
    )
    
    parser.add_argument('results_directory', 
                       help='Path to the experiment results directory')
    
    parser.add_argument('--all-methods', action='store_true',
                       help='Run all methods for the experiment type: 6 methods for two-step (VVV,VXX,VXV,VVX + 2 pruning ablations) or 6 methods for one-step (XXX,XXV,XVX,XVV + 2 pruning ablations)')
    
    parser.add_argument('--pruning-ablation', action='store_true',
                        help='Run pruning ablation study: no pruning, existence pruning, uniqueness pruning, and combined')
    
    parser.add_argument('--path-ablation', action='store_true',
                       help='Add path ablation study results to the standard CSV output (majority voting with different numbers of paths)')
    
    parser.add_argument('--methods', nargs='+', 
                       choices=['sketchformal', 'direct_translation_multipath_pruning', 'sketchformal_pruning_only', 
                               'sketchformal_majority_vote', 'direct_translation', 'sketch_only', 
                               'direct_translation_multipath', 'direct_translation_pruning',
                               'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote'],
                       default=['sketchformal'],
                       help='Specify which methods to run (default: sketchformal only)')
    
    parser.add_argument('--expected-paths', type=int, default=5,
                       help='Expected number of paths per sample (default: 5). Missing paths are treated as syntax errors.')
    
    parser.add_argument('--path-counts', nargs='+', type=int, 
                       default=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,30],
                       help='List of path counts to analyze for path ablation (default: auto-generate from config num_paths - e.g., for 5 paths: 1,3,5; for 30 paths: 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,30)')
    
    args = parser.parse_args()
    
    results_dir = args.results_directory
    # If relative path, make it absolute
    if not os.path.isabs(results_dir):
        results_dir = os.path.abspath(results_dir)
    
    # Load config to determine experiment type
    config_file = os.path.join(results_dir, 'config.yaml')
    config = load_config(config_file)
    exp_id = os.path.basename(results_dir.rstrip('/'))
    config_info = extract_config_info(config, exp_id)
    
    # Generate path counts from config if path ablation is requested and no custom path counts provided
    if args.path_ablation:
        args.path_counts = generate_path_counts_from_config(args.expected_paths)

    # import pdb; pdb.set_trace()
    # Determine which methods to run based on experiment type
    if args.pruning_ablation:
        # Pruning ablation study: compare different pruning strategies
        methods_to_run = ['sketchformal_majority_vote', 'existence_pruning_majority_vote', 
                         'uniqueness_pruning_majority_vote', 'sketchformal']
    elif args.all_methods:
        # Check if this is a two-step or one-step experiment
        if config_info['has_sketch']:
            # Two-step: VVV, VXX, VXV, VVX + 2 semantic pruning ablations
            methods_to_run = ['sketchformal', 'sketch_only', 'sketchformal_pruning_only', 'sketchformal_majority_vote',
                             'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']
        else:
            # One-step: XXX, XXV, XVX, XVV + 2 semantic pruning ablations
            methods_to_run = ['direct_translation', 'direct_translation_pruning', 'direct_translation_multipath', 'direct_translation_multipath_pruning',
                             'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']

    elif args.path_ablation:
        methods_to_run = [f'path_ablation_{num_paths}_paths' for num_paths in args.path_counts]
        print(f"Running path ablation methods: {methods_to_run}")
        
    else:
        methods_to_run = args.methods
        
    
    # File paths - check both direct path and summary subdirectory
    summary_file = os.path.join(results_dir, 'summary.txt')
    
    
    if not os.path.exists(summary_file):
        # Try summary subdirectory
        summary_file_alt = os.path.join(results_dir, 'summary', 'summary.txt')
        if os.path.exists(summary_file_alt):
            summary_file = summary_file_alt
    
    # Check if summary file exists
    if not os.path.exists(summary_file):
        print(f"Error: summary.txt not found at {os.path.join(results_dir, 'summary.txt')} or {os.path.join(results_dir, 'summary', 'summary.txt')}")
        sys.exit(1)
    
    # Detect dataset from config
    dataset = config.get('dataset', 'ar-lsat').lower()  # Default to AR-LSAT for backward compatibility
    print(f"Detected dataset: {dataset.upper()}")
    print(f"Experiment type: {'Two-step (sketch-based)' if config_info['has_sketch'] else 'One-step (direct translation)'}")
    
    # Regular analysis
    print("Loading results...")
    results = load_results(summary_file)
    print(f"Loaded {len(results)} items")
    
    print(f"\nRunning methods: {', '.join(methods_to_run)}")
    
    # Dictionary to store results
    method_results = {}
    
    # Run selected methods
    expected_paths = args.expected_paths
    print(f"Expected paths per sample: {expected_paths}")
    
    # Method calculation mapping
    method_calculators = {
        'sketchformal': (calculate_accuracy_sketchformal, "🎯 SketchFormal (VVV): Sketch Plans + Multi-path + Semantic Pruning"),
        'direct_translation_multipath_pruning': (calculate_accuracy_direct_translation_multipath_pruning, "📊 Direct translation with multi-path and pruning (XVV)"),
        'sketchformal_pruning_only': (calculate_accuracy_sketchformal_pruning_only, "📊 SketchFormal with semantic pruning only (VXV)"),
        'sketchformal_majority_vote': (calculate_accuracy_sketchformal_majority_vote, "📊 SketchFormal with majority vote (VVX)"),
        'direct_translation': (calculate_accuracy_direct_translation, "📊 Direct translation (XXX)"),
        'sketch_only': (calculate_accuracy_sketch_only, "📊 Sketch-only (VXX)"),
        'direct_translation_multipath': (calculate_accuracy_direct_translation_multipath, "📊 Direct translation with multi-path (XVX)"),
        'direct_translation_pruning': (calculate_accuracy_direct_translation_pruning, "📊 Direct translation with pruning (XXV)"),
        'existence_pruning_majority_vote': (calculate_accuracy_existence_pruning_majority_vote, "🔍 Existence pruning + majority vote (length >= 1)"),
        'uniqueness_pruning_majority_vote': (calculate_accuracy_uniqueness_pruning_majority_vote, "🔍 Uniqueness pruning + majority vote (length <= 1)")
    }
    
    for method_name in methods_to_run:
        if method_name in method_calculators:
            calc_func, description = method_calculators[method_name]
            print(f"\n{description} for {dataset.upper()}...")
            method_results[method_name] = calc_func(results, dataset, expected_paths)
        elif method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            # Handle path ablation methods dynamically
            num_paths = int(method_name.split('_')[2])  # Extract number from 'path_ablation_X_paths'
            print(f"\n🛤️  Path ablation with {num_paths} paths for {dataset.upper()}...")
            method_results[method_name] = calculate_accuracy_path_ablation(results, num_paths, dataset, expected_paths)
    
    # Print results
    print("\n" + "="*80)
    print("EXPERIMENTAL RESULTS")
    print("="*80)
    
    # Define method display names and order
    method_display = {
        'sketchformal': '🎯 SKETCHFORMAL (VVV) - PRIMARY METHOD',
        'direct_translation_multipath_pruning': '📊 DIRECT TRANSLATION + MULTIPATH + PRUNING (XVV)',
        'sketchformal_pruning_only': '📊 SKETCHFORMAL + PRUNING ONLY (VXV)',
        'sketchformal_majority_vote': '📊 SKETCHFORMAL + MAJORITY VOTE (VVX)',
        'direct_translation': '📊 DIRECT TRANSLATION (XXX)',
        'sketch_only': '📊 SKETCH-ONLY (VXX)',
        'direct_translation_multipath': '📊 DIRECT TRANSLATION + MULTIPATH (XVX)',
        'direct_translation_pruning': '📊 DIRECT TRANSLATION + PRUNING (XXV)',
        'existence_pruning_majority_vote': '🔍 EXISTENCE PRUNING + MAJORITY VOTE (length >= 1)',
        'uniqueness_pruning_majority_vote': '🔍 UNIQUENESS PRUNING + MAJORITY VOTE (length <= 1)'
    }
    
    # Add path ablation method display names dynamically
    for method_name in method_results.keys():
        if method_name.startswith('path_ablation_') and method_name.endswith('_paths'):
            num_paths = int(method_name.split('_')[2])
            method_display[method_name] = f'🛤️  PATH ABLATION ({num_paths} paths)'
    
    # Print results in the order they were run, with SketchFormal first if present
    method_order = ['sketchformal', 'direct_translation_multipath_pruning', 'sketchformal_pruning_only', 
                   'sketchformal_majority_vote', 'direct_translation', 'sketch_only', 
                   'direct_translation_multipath', 'direct_translation_pruning',
                   'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']
    
    # Add path ablation methods to the order (they'll be printed after the standard methods)
    path_ablation_methods = [method for method in method_results.keys() if method.startswith('path_ablation_')]
    method_order.extend(sorted(path_ablation_methods))
    
    
    for method_name in method_order:
        if method_name in method_results:
            result = method_results[method_name]
            print(f"\n=== {method_display[method_name]} ===")
            print(f"Correct: {result['correct']}")
            print(f"Total: {result['total']}")
            print(f"Accuracy: {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")
            print(f"Accuracy by path: {result['accuracy_by_path']:.4f} ({result['accuracy_by_path']*100:.2f}%)")
            print(f"Correct paths: {result['correct_paths']}")
            print(f"Syntactic correct paths: {result['syntactic_correct_paths']}")
            
            # Only show tied voting for methods that use majority vote (multi-path exploration)
            multipath_methods = ['sketchformal', 'direct_translation_multipath_pruning', 'sketchformal_majority_vote', 'direct_translation_multipath',
                                'existence_pruning_majority_vote', 'uniqueness_pruning_majority_vote']
            if method_name in multipath_methods:
                print(f"Tied voting samples: {result['tied_voting_samples']}")
                print(f"Tied voting rate: {result['tied_voting_rate']:.4f} ({result['tied_voting_rate']*100:.2f}%)")
            
            print(f"Failed extractions: {result['failed_extractions']}")
            print(f"Syntax errors: {result['syntax_errors']}")
            print(f"Total paths before pruning: {result['total_paths_before']}")
            print(f"Total paths after pruning: {result['total_paths_after']}")
            print(f"Avg paths before pruning: {result['avg_paths_before']:.2f}")
            print(f"Avg paths after pruning: {result['avg_paths_after']:.2f}")
    
    # Create CSV and detailed results only if we have results
    if method_results:
        print("\nCreating comprehensive CSV file...")
        
        # Convert method_results to the expected format for CSV creation
        results_list = []
        for method_name in method_order:
            if method_name in method_results:
                results_list.append(method_results[method_name])
        
        result = create_comprehensive_csv(results_dir, summary_file, config_file, dataset, *results_list, args=args)
        df, csv_output_file, xlsx_output_file = result if len(result) == 3 else (result[0], result[1], None)
        
        print(f"\nCSV Results saved to: {csv_output_file}")
        if xlsx_output_file:
            print(f"XLSX Results saved to: {xlsx_output_file}")
        # print("\nCSV Preview:")
        # print(df.to_string(index=False))
        
        # Save detailed results with new naming
        detailed_results = {}
        method_mapping = {
            'sketchformal': 'sketchformal_VVV_primary_method',
            'direct_translation_multipath_pruning': 'direct_translation_multipath_pruning_XVV',
            'sketchformal_pruning_only': 'sketchformal_pruning_only_VXV',
            'sketchformal_majority_vote': 'sketchformal_majority_vote_VVX',
            'direct_translation': 'direct_translation_XXX',
            'sketch_only': 'sketch_only_VXX',
            'direct_translation_multipath': 'direct_translation_multipath_XVX',
            'direct_translation_pruning': 'direct_translation_pruning_XXV',
            'existence_pruning_majority_vote': 'existence_pruning_majority_vote',
            'uniqueness_pruning_majority_vote': 'uniqueness_pruning_majority_vote'
        }
        
        for method_name, result in method_results.items():
            if method_name in method_mapping:
                detailed_results[method_mapping[method_name]] = result
            else:
                # Handle path ablation methods or other dynamic methods
                detailed_results[method_name] = result
    
    detailed_output_file = os.path.join(results_dir, 'detailed_ablation_results.json')
    with open(detailed_output_file, 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\nDetailed results saved to: {detailed_output_file}")

if __name__ == "__main__":
    main()
