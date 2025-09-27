#!/usr/bin/env python3
"""
Path-level analysis script for neural-symbolic reasoning experiments.

This script creates a detailed dataframe with path-level information including:
- Sample ID and Path ID for each individual path
- LLM API parameters (shots in ICL, ICL samples source)
- Correctness evaluation (parse solver output and compare with label)
- Pruning status (pruned by existence, pruned by uniqueness)
- Pruning results (None if pruned, otherwise original output)
- Combined existence & uniqueness pruning results

The script processes experiment results and generates a comprehensive path-level CSV/XLSX file.
It can automatically merge individual result files from a summary/ subdirectory if summary.txt is not found.

Usage:
    python path_level_analysis.py <results_directory> --expected-paths 5
    python path_level_analysis.py results/experiment_folder/ --expected-paths 5 --cot-summary path/to/cot_summary.txt
"""

import json
import glob
import pandas as pd
import yaml
import ast
import argparse
import os
import sys
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


def load_config(config_file):
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}


def _flatten(nested_list):
    """Flatten arbitrarily nested lists into a flat list (non-list elements)."""
    for item in nested_list:
        if isinstance(item, list):
            yield from _flatten(item)
        else:
            yield item


def parse_solver_output(output_str, dataset=None, problem_answers=None):
    """Parse solver output string to extract list of answers based on dataset format.
    
    For AR-LSAT dataset, handles multiple formats:
    1. Python literals: "[2]", "[]", "[0, 1, 2]"
    2. Answer choice matching: matches output against problem's answer choices
    3. Word numbers: "four", "three", "two" -> [4], [3], [2]
    
    Args:
        output_str: The solver output string to parse
        dataset: Dataset name (e.g., 'ar-lsat', 'proofwriter', etc.)
        problem_answers: List of answer choices for the problem (optional)
    
    Returns:
        List of parsed answers or 'syntax error' if parsing fails
    """
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
                    else:
                        return []
            return []
        
        elif dataset and dataset.lower() == 'ar-lsat':
            # AR-LSAT format: Handle string representations of lists like "[2]", "[]", etc.
            # Also handle option strings like "four", "three", etc.
            if isinstance(output_str, str):
                # Try to parse as Python literal first (existing logic)
                try:
                    parsed = ast.literal_eval(output_str)
                    if isinstance(parsed, list):
                        # Check if this is a list of strings that need to be mapped to indices
                        if problem_answers and all(isinstance(item, str) for item in parsed):
                            mapped_indices = []
                            for item in parsed:
                                # Try exact match first
                                for i, answer in enumerate(problem_answers):
                                    if item.strip().lower() == answer.strip().lower():
                                        mapped_indices.append(i)
                                        break
                            
                            # If we successfully mapped all items, return the indices
                            if len(mapped_indices) == len(parsed):
                                return mapped_indices
                            # If some items couldn't be mapped, return the original parsed list
                            else:
                                return parsed
                        else:
                            # If not all strings or no problem_answers, return parsed as-is
                            return parsed
                    else:
                        return [parsed] if parsed is not None else []
                except:
                    # If literal_eval fails, try answer matching first if provided
                    if problem_answers:
                        # Clean the output string for comparison
                        clean_output = output_str.strip()
                        
                        # Try exact match first
                        for i, answer in enumerate(problem_answers):
                            if clean_output.lower() == answer.lower():
                                return [i]
                        
                        # Try partial match (output contained in answer or vice versa)
                        for i, answer in enumerate(problem_answers):
                            if (clean_output.lower() in answer.lower()) or (answer.lower() in clean_output.lower()):
                                return [i]
                    
                    # If no answer match, check if it's a word number that needs to be converted to option index
                    word_to_option = {
                        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
                    }
                    
                    # Clean the string and check if it's a word number
                    clean_str = output_str.strip().lower()
                    if clean_str in word_to_option:
                        return [word_to_option[clean_str]]
                    
                    # If no match found, treat as empty list
                    return []
            elif isinstance(output_str, list):
                # Handle list of strings that might need to be mapped to option indices
                if problem_answers and all(isinstance(item, str) for item in output_str):
                    # Try to map each string in the list to its corresponding option index
                    mapped_indices = []
                    for item in output_str:
                        # Try exact match first
                        for i, answer in enumerate(problem_answers):
                            if item.strip().lower() == answer.strip().lower():
                                mapped_indices.append(i)
                                break
                        else:
                            # Try partial match if exact match fails
                            for i, answer in enumerate(problem_answers):
                                if (item.strip().lower() in answer.strip().lower()) or (answer.strip().lower() in item.strip().lower()):
                                    mapped_indices.append(i)
                                    break
                    
                    # If we successfully mapped all items, return the indices
                    if len(mapped_indices) == len(output_str):
                        return mapped_indices
                    # If some items couldn't be mapped, return the original list
                    else:
                        return output_str
                else:
                    # If not all strings or no problem_answers, return as-is
                    return output_str
            else:
                return []
        else:
            raise NotImplementedError(f"Invalid dataset: {dataset}")
    except:
        return []


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


def is_correct_path(parsed_output, true_label, dataset):
    """Determine if a parsed output is correct by comparing with true label."""
    if parsed_output == 'syntax error':
        return False
    
    flat_output = list(_flatten(parsed_output))
    if len(flat_output) != 1:
        return False
    
    try:
        path_answer = flat_output[0]
        
        # Handle different answer formats
        if dataset and dataset.lower() == 'ar-lsat':
            # AR-LSAT: numeric comparison
            path_answer = int(path_answer)
            true_label_int = int(true_label)
            return path_answer == true_label_int
        elif dataset and dataset.lower() in ['proofwriter', 'folio']:
            # ProofWriter/FOLIO: mapping between boolean and letters
            return (path_answer == "True" and true_label == "A") or \
                   (path_answer == "False" and true_label == "B") or \
                   (path_answer == "Unknown" and true_label == "C")
        elif dataset and dataset.lower() == 'prontoqa':
            # ProntoQA: mapping between boolean and letters
            return (path_answer == "True" and true_label == "A") or \
                   (path_answer == "False" and true_label == "B")
        elif dataset and dataset.lower() == 'logicaldeduction':
            # LogicalDeduction: direct letter comparison
            return str(path_answer) == str(true_label)
        else:
            # Default: string comparison
            return str(path_answer) == str(true_label)
    except (ValueError, TypeError):
        return False


def is_pruned_by_existence(parsed_output):
    """Check if output would be pruned by existence criteria (length >= 1)."""
    if parsed_output == 'syntax error':
        return False  # Syntax errors are pruned
    
    flat_output = list(_flatten(parsed_output))
    return len(flat_output) < 1  # Pruned if empty (length < 1)


def is_pruned_by_uniqueness(parsed_output):
    """Check if output would be pruned by uniqueness criteria (length <= 1)."""
    if parsed_output == 'syntax error':
        return False  # Syntax errors are pruned
    
    flat_output = list(_flatten(parsed_output))
    return len(flat_output) > 1  # Pruned if multiple answers (length > 1)


def load_results_from_directory(summary_directory):
    """Load all JSON results from a directory and merge them."""
    json_files = glob.glob(os.path.join(summary_directory, "*.json"))
    all_results = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                all_results.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            continue
    
    return all_results


def merge_summary(results_directory):
    """Merge individual result files into summary.txt."""
    summary_directory = os.path.join(results_directory, "summary")
    
    if not os.path.exists(summary_directory):
        print(f"Summary directory not found: {summary_directory}")
        return False
    
    # Load all results
    results = load_results_from_directory(summary_directory)
    
    if not results:
        print("No valid result files found in summary directory.")
        return False
    
    # Write merged results to summary.txt
    parent_dir = os.path.join(summary_directory, "../")
    summary_file = os.path.join(parent_dir, "summary.txt")
    
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Merged {len(results)} result files into: {summary_file}")
    print(f"Total samples: {len(results)}")
    
    # Basic statistics
    if results:
        total_time = sum(r.get("timing", 0) for r in results)
        avg_time = total_time / len(results) if results else 0
        print(f"Average time per sample: {avg_time:.2f} seconds")
        print(f"Total time: {total_time:.2f} seconds")
    
    return True


def create_path_level_dataframe(results, config, dataset, exp_id, expected_paths_per_sample=5):
    """Create path-level dataframe with detailed information for each path."""
    
    # Extract config info
    config_info = extract_config_info(config, exp_id)
    
    rows = []
    
    for item in results:
        if 'problem' not in item:
            continue
        
        # Get true label
        if 'label' in item['problem']:
            true_label = item['problem']['label']
        elif 'answer' in item['problem']:
            true_label = item['problem']['answer']
        else:
            continue
        
        sample_id = item['problem'].get('id_string', item['problem'].get('id', f'unknown_sample'))
        all_solver_outputs = item.get('all_solver_outputs', [])
        problem_answers = item['problem'].get('answers', None)  # Get answer choices for this problem
        
        # Process each path (up to expected_paths_per_sample)
        for path_idx in range(expected_paths_per_sample):
            path_id = f"{path_idx+1}"
            
            # Check if this path exists
            if path_idx < len(all_solver_outputs):
                output_str = all_solver_outputs[path_idx]
                # is_missing_path = False
            else:
                # Missing path - treat as syntax error
                output_str = "missing path"
                # is_missing_path = True
            
            # Parse the output with problem answers for better matching
            parsed_output = parse_solver_output(output_str, dataset, problem_answers)
            # Determine correctness
            is_correct = is_correct_path(parsed_output, true_label, dataset)
            
            # Determine pruning status
            pruned_by_existence = is_pruned_by_existence(parsed_output)
            pruned_by_uniqueness = is_pruned_by_uniqueness(parsed_output)
            
            # Determine if it's a syntax error
            is_syntax_error = (parsed_output == 'syntax error')
            
            # Calculate pruning results: None if pruned, otherwise keep original output
            existence_pruning_result = None if pruned_by_existence else (str(parsed_output) if parsed_output != 'syntax error' else 'syntax error')
            uniqueness_pruning_result = None if pruned_by_uniqueness else (str(parsed_output) if parsed_output != 'syntax error' else 'syntax error')
            
            # Calculate combined existence & uniqueness pruning result
            # Path is kept only if it passes BOTH existence AND uniqueness criteria
            # Calculate combined existence & uniqueness pruning result
            # Path is kept only if it passes BOTH existence AND uniqueness criteria
            if pruned_by_existence or pruned_by_uniqueness:
                combined_pruning_result = None
            else:
                if parsed_output != 'syntax error':
                    combined_pruning_result = str(parsed_output)
                else:
                    combined_pruning_result = 'syntax error'
            
            row = {
                'dataset': dataset.upper(),
                'sample_id': sample_id,
                # 'path_id': path_id,
                'path_index': path_idx,
                'experiment_id': exp_id,
                'shots_in_icl': config_info['shots'],
                'icl_sample_source': 'logic-lm autoformalization ICL',
                'sketch_gen_model': config_info['plan_model'],
                'code_gen_model': config_info['code_model'],
                'has_sketch': 'yes' if config_info['has_sketch'] else 'no',
                'raw_output': output_str,
                'parsed_output': str(parsed_output) if parsed_output != 'syntax error' else 'syntax error',
                'true_label': true_label,
                'is_correct': is_correct,
                'is_syntax_error': is_syntax_error,
                # 'is_missing_path': is_missing_path,
                'pruned_by_existence': pruned_by_existence,
                'existence_pruning_result': existence_pruning_result,
                'pruned_by_uniqueness': pruned_by_uniqueness,
                'uniqueness_pruning_result': uniqueness_pruning_result,
                'existence_uniqueness_pruning_result': combined_pruning_result,
                # 'passes_existence_filter': not pruned_by_existence,
                # 'passes_uniqueness_filter': not pruned_by_uniqueness,
                # 'output_length': len(list(_flatten(parsed_output))) if parsed_output != 'syntax error' else 0
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def calculate_one_path_accuracy(df, use_cot_backup=False):
    """Calculate accuracy metrics for one-path (single path) results."""
    # Filter to only path_index 0 (first path only)
    first_paths = df[df['path_index'] == 0].copy()
    
    if len(first_paths) == 0:
        return {
            'total_samples': 0,
            'correct_samples': 0,
            'accuracy': 0.0,
            'syntax_error_samples': 0,
            'syntax_error_rate': 0.0,
            'valid_samples': 0,
            'valid_accuracy': 0.0,
            'cot_backup_used': 0,
            'cot_backup_correct': 0
        }
    
    total_samples = len(first_paths)
    
    # Apply CoT backup for syntax errors if enabled
    cot_backup_used = 0
    cot_backup_correct = 0
    
    if use_cot_backup and 'cot_correctness' in first_paths.columns:
        # Create a copy to modify
        first_paths_with_backup = first_paths.copy()
        
        # Find syntax error samples that have CoT correctness available
        syntax_error_mask = first_paths_with_backup['is_syntax_error'] == True
        cot_available_mask = first_paths_with_backup['cot_correctness'].notna()
        cot_correct_mask = first_paths_with_backup['cot_correctness'] == True
        
        # Apply backup: use CoT result for syntax errors where CoT was correct
        backup_mask = syntax_error_mask & cot_available_mask & cot_correct_mask
        
        if backup_mask.any():
            cot_backup_used = backup_mask.sum()
            # Mark these samples as correct (CoT backup succeeded)
            first_paths_with_backup.loc[backup_mask, 'is_correct'] = True

            cot_backup_correct = cot_backup_used  # All CoT backups are correct by definition
            
            print(f"CoT backup applied to {cot_backup_used} syntax error samples in first path accuracy")
        
        # Use the modified dataframe for calculations
        first_paths = first_paths_with_backup
    
    correct_samples = first_paths['is_correct'].sum()
    syntax_error_samples = first_paths['is_syntax_error'].sum()
    valid_samples = total_samples - syntax_error_samples
    
    # Overall accuracy (including syntax errors as incorrect)
    overall_accuracy = correct_samples / total_samples if total_samples > 0 else 0.0
    
    # Accuracy excluding syntax errors
    valid_accuracy = correct_samples / valid_samples if valid_samples > 0 else 0.0
    
    # Syntax error rate
    syntax_error_rate = syntax_error_samples / total_samples if total_samples > 0 else 0.0
    
    return {
        'total_samples': total_samples,
        'correct_samples': correct_samples,
        'accuracy': overall_accuracy,
        'syntax_error_samples': syntax_error_samples,
        'syntax_error_rate': syntax_error_rate,
        'valid_samples': valid_samples,
        'valid_accuracy': valid_accuracy,
        'cot_backup_used': cot_backup_used,
        'cot_backup_correct': cot_backup_correct
    }



def add_cot_correctness_column(df, cot_summary_file):
    """Add CoT correctness column to path-level dataframe by mapping id_string to sample_id."""
    if not os.path.exists(cot_summary_file):
        print(f"Warning: CoT summary file not found: {cot_summary_file}")
        return df
    
    print(f"Adding CoT correctness from: {cot_summary_file}")
    
    # Load CoT summary
    try:
        cot_results = load_results(cot_summary_file)
        if not cot_results:
            print("Warning: No CoT results found")
            return df
    except Exception as e:
        print(f"Error loading CoT summary: {e}")
        return df
    
    # Create mapping from id_string to success
    id_to_success = {}
    for result in cot_results:
        if 'problem' in result and 'id_string' in result['problem']:
            id_string = result['problem']['id_string']
            success = result.get('success', False)
            id_to_success[id_string] = success
    
    print(f"Loaded {len(id_to_success)} CoT results")
    
    # Add cot_correctness column to dataframe
    df['cot_correctness'] = df['sample_id'].map(id_to_success)
    
    # Report mapping statistics
    mapped_count = df['cot_correctness'].notna().sum()
    total_count = len(df)
    print(f"Successfully mapped {mapped_count}/{total_count} samples ({mapped_count/total_count*100:.1f}%)")
    
    if mapped_count < total_count:
        unmapped_samples = df[df['cot_correctness'].isna()]['sample_id'].unique()
        print(f"Warning: {len(unmapped_samples)} samples could not be mapped to CoT results")
        if len(unmapped_samples) <= 10:
            print(f"Unmapped sample IDs: {list(unmapped_samples)}")
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Create path-level analysis dataframe for neural-symbolic reasoning experiments.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python path_level_analysis.py results/experiment_folder/ --expected-paths 5
    python path_level_analysis.py results/experiment_folder/ --expected-paths 5 --cot-summary path/to/cot_summary.txt
        """
    )
    
    parser.add_argument('results_directory', 
                       help='Path to the experiment results directory')
    
    parser.add_argument('--expected-paths', type=int, default=5,
                       help='Expected number of paths per sample (default: 5)')
    
    parser.add_argument('--output-format', choices=['csv', 'xlsx', 'both'], default='both',
                       help='Output format (default: both)')
    
    parser.add_argument('--force-merge', action='store_true',
                       help='Force merge individual result files even if summary.txt exists')
    
    parser.add_argument('--cot-summary', type=str,
                       help='Path to CoT summary.txt file to add cot_correctness column')
    
    parser.add_argument('--cot-backup', action='store_true',
                       help='Use CoT as backup for syntax errors in first path accuracy calculation')
    
    args = parser.parse_args()
    
    results_dir = args.results_directory
    # If relative path, make it absolute
    if not os.path.isabs(results_dir):
        results_dir = os.path.abspath(results_dir)
    
    # Try to merge summary files first if summary.txt doesn't exist
    summary_file = os.path.join(results_dir, 'summary.txt')
    config_file = os.path.join(results_dir, 'config.yaml')
    
    # Check if summary.txt exists, or if force-merge is requested
    if not os.path.exists(summary_file) or args.force_merge:
        if args.force_merge:
            print(f"Force merge requested, merging individual result files...")
        else:
            print(f"summary.txt not found at {summary_file}")
            print("Attempting to merge individual result files...")
        
        merge_success = merge_summary(results_dir)
        
        if not merge_success or not os.path.exists(summary_file):
            # Try alternative summary subdirectory location
            summary_file_alt = os.path.join(results_dir, 'summary', 'summary.txt')
            if os.path.exists(summary_file_alt):
                summary_file = summary_file_alt
                print(f"Using summary file from subdirectory: {summary_file}")
            else:
                print(f"Error: summary.txt not found at {summary_file} or {summary_file_alt}")
                print("Also failed to merge individual result files.")
                sys.exit(1)
    else:
        print(f"Found existing summary.txt at: {summary_file}")
    
    if not os.path.exists(config_file):
        print(f"Error: config.yaml not found at {config_file}")
        sys.exit(1)
    
    # Load data
    print("Loading results and config...")
    results = load_results(summary_file)
    config = load_config(config_file)
    
    # Extract experiment info
    exp_id = os.path.basename(results_dir.rstrip('/'))
    dataset = config.get('dataset', 'ar-lsat').lower()
    
    print(f"Experiment ID: {exp_id}")
    print(f"Dataset: {dataset.upper()}")
    print(f"Loaded {len(results)} samples")
    print(f"Expected paths per sample: {args.expected_paths}")
    
    # Create path-level dataframe
    print("Creating path-level dataframe...")
    df = create_path_level_dataframe(results, config, dataset, exp_id, args.expected_paths)
    
    print(f"Created dataframe with {len(df)} rows (paths)")
    
    # Add CoT correctness column if specified
    if args.cot_summary:
        df = add_cot_correctness_column(df, args.cot_summary)
    
    # Summary statistics
    total_paths = len(df)
    correct_paths = df['is_correct'].sum()
    syntax_error_paths = df['is_syntax_error'].sum()
    # missing_paths = df['is_missing_path'].sum()
    
    print(f"\nSummary Statistics:")
    print(f"Total paths: {total_paths}")
    print(f"Correct paths: {correct_paths} ({correct_paths/total_paths*100:.2f}%)")
    print(f"Syntax error paths: {syntax_error_paths} ({syntax_error_paths/total_paths*100:.2f}%)")
    # print(f"Missing paths: {missing_paths} ({missing_paths/total_paths*100:.2f}%)")
    
    # Pruning statistics
    pruned_existence = df['pruned_by_existence'].sum()
    pruned_uniqueness = df['pruned_by_uniqueness'].sum()
    # pruned_semantic = df['pruned_by_semantic'].sum()
    
    print(f"\nPruning Statistics:")
    print(f"Pruned by existence: {pruned_existence} ({pruned_existence/total_paths*100:.2f}%)")
    print(f"Pruned by uniqueness: {pruned_uniqueness} ({pruned_uniqueness/total_paths*100:.2f}%)")
    # print(f"Pruned by semantic: {pruned_semantic} ({pruned_semantic/total_paths*100:.2f}%)")
    
    # Calculate one-path accuracy (first path only)
    print(f"\n" + "="*60)
    print("ONE-PATH ACCURACY ANALYSIS (First Path Only, without pruning)")
    print("="*60)
    
    one_path_results = calculate_one_path_accuracy(df, use_cot_backup=args.cot_backup)
    print(f"Total samples: {one_path_results['total_samples']}")
    print(f"Correct samples: {one_path_results['correct_samples']}")
    print(f"Overall accuracy: {one_path_results['accuracy']:.4f} ({one_path_results['accuracy']*100:.2f}%)")
    print(f"Syntax error samples: {one_path_results['syntax_error_samples']}")
    print(f"Syntax error rate: {one_path_results['syntax_error_rate']:.4f} ({one_path_results['syntax_error_rate']*100:.2f}%)")
    print(f"Valid samples (excluding syntax errors): {one_path_results['valid_samples']}")
    print(f"Accuracy on valid samples only: {one_path_results['valid_accuracy']:.4f} ({one_path_results['valid_accuracy']*100:.2f}%)")
    
    # Show CoT backup statistics if enabled
    if args.cot_backup:
        print(f"CoT backup used: {one_path_results['cot_backup_used']} samples")
        print(f"CoT backup correct: {one_path_results['cot_backup_correct']} samples")
        if one_path_results['cot_backup_used'] > 0:
            backup_accuracy = one_path_results['cot_backup_correct'] / one_path_results['cot_backup_used']
            print(f"CoT backup accuracy: {backup_accuracy:.4f} ({backup_accuracy*100:.2f}%)")
    
    
    # Save results
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'path-level-analysis')
    os.makedirs(output_dir, exist_ok=True)
    
    base_filename = f"{exp_id}_path_level"
    
    if args.output_format in ['csv', 'both']:
        csv_output_file = os.path.join(output_dir, f"{base_filename}.csv")
        df.to_csv(csv_output_file, index=False)
        print(f"\nCSV saved to: {csv_output_file}")
    
    if args.output_format in ['xlsx', 'both']:
        xlsx_output_file = os.path.join(output_dir, f"{base_filename}.xlsx")
        try:
            df.to_excel(xlsx_output_file, index=False, engine='openpyxl')
            print(f"XLSX saved to: {xlsx_output_file}")
        except ImportError:
            print("Warning: openpyxl not installed. XLSX file not saved. Install with: pip install openpyxl")
    
    # Display sample of the dataframe
    # print(f"\nSample of the dataframe (first 5 rows):")
    # print(df.head().to_string(index=False))
    
    return df


if __name__ == "__main__":
    main()
