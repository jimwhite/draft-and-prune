#!/usr/bin/env python3
"""
Generalized ablation analysis script for neural-symbolic reasoning experiments. (Remember to first run python analysis_simple.py /path/to/xxx/summary to get the summary.txt file)

This script analyzes experimental results and creates comprehensive CSV files with:
1. Method 1: No pruning + majority vote (uses all output lists)
2. Method 2: With pruning + no majority vote (extracts first valid output)

=== PARAMETER MEANINGS ===

Core Experiment Info:
- ID: Unique identifier for the experimental run
- Benchmarks: Dataset name (extracted from config.yaml "dataset" field)
- #shots in ICL: Number of in-context learning examples (0=zero-shot, 3=three-shot, etc.)
- ICL sample source: Source of ICL examples ("logic-lm autoformalization ICL")
- sketch: Whether sketch/planning is used ("yes" for two-step, "no" for one-step/cot)
- #total samples: Total number of samples

Path Generation:
- K (#paths per sample): Average number of generated paths per sample (default: 5)
- path pruning: Left blank (for manual annotation)
- path pruning (existence): Left blank (for manual annotation)  
- path pruning (uniqueness): Left blank (for manual annotation)

Model Configuration:
- sketch-gen model: Model used for sketch/plan generation (from config "plan_model")
- code-gen model: Model used for code generation (from config "code_model")
- sketch temp: Temperature for sketch generation (default: 1)
- code temp: Temperature for code generation (default: 0)

Error Analysis:
- #samples failed by syntax error : Number of samples with at least one syntax error
- #paths failed by syntax error: Total number of paths with syntax errors
- syntax error rate: Ratio of syntax error paths to total paths

Path Statistics:
- Total #paths before pruning: Total paths across all samples before any filtering
- Total #paths after pruning: Total paths after applying method-specific filtering
- Avg #paths before pruning: Average paths per sample before filtering
- Avg #paths after pruning: Average paths per sample after filtering

Performance Metrics:
- tied voting rate: Ratio of samples with tied votes (multiple answers with same max votes)
- #samples with auto-formalization failure: Number of samples where no valid answer could be extracted from any path (due to syntax errors, invalid formats, or empty outputs)
- backup method: Fallback method used when primary extraction fails
- overall accuracy: Sample-level accuracy (correct samples / total samples)
- accuracy by path: Path-level accuracy (correct paths / syntactically correct paths)

Usage:
    python custom_ablation_analysis.py <results_directory>
    
Example:
    python custom_ablation_analysis.py results/Sketch-only-Sep18-2025/one-step-AR-LSAT-...
"""

import json
import pandas as pd
import yaml
import ast
from collections import Counter
import re
import os
import sys

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

def parse_solver_output(output_str):
    """Parse solver output string to extract list of answers."""
    try:
        # Check for syntax error pattern first
        if isinstance(output_str, str) and "execution error" in output_str:
            return 'syntax error'
        
        # Handle string representations of lists like "[2]", "[]", etc.
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
        # If parsing fails, try to extract numbers manually
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

def extract_config_info(config):
    """Extract information from config."""
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
    
    return {
        'shots': shots,
        'has_sketch': has_sketch
    }

def create_comprehensive_csv(results_dir, summary_file, config_file, result1, result2):
    """Create comprehensive CSV file with all required columns."""
    
    # Load config
    config = load_config(config_file)
    
    # Extract config info
    config_info = extract_config_info(config)
    
    # Extract experiment ID from directory name
    exp_id = os.path.basename(results_dir)
    
    # Create rows for both methods
    rows = []
    
    for i, result in enumerate([result1, result2]):
        row = {
            'ID': f"{exp_id}_{result['method']}",
            'Benchmarks': config.get('dataset', 'unknown'),
            '#shots in ICL': config_info['shots'],
            'ICL sample source': 'logic-lm autoformalization ICL',
            'sketch': 'yes' if config_info['has_sketch'] else 'no',
            '#total samples': result['total'],
            'K (#paths per sample)': 5,  # Default value as specified
            'path pruning': '',  # Leave blank as specified
            'path pruning (existence)': '',  # Leave blank as specified
            'path pruning (uniqueness)': '',  # Leave blank as specified
            'sketch-gen model': config.get('plan_model', ''),
            'code-gen model': config.get('code_model', ''),
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
    
    # Save to CSV
    output_file = os.path.join(results_dir, 'ablation_study_results.csv')
    df.to_csv(output_file, index=False)
    
    return df, output_file

def calculate_path_level_metrics(all_solver_outputs, true_label):
    """Calculate path-level metrics for accuracy by path calculation."""
    correct_paths = 0
    syntactic_correct_paths = 0
    
    for output_str in all_solver_outputs:
        parsed_output = parse_solver_output(output_str)
        if parsed_output != 'syntax error':
            syntactic_correct_paths += 1
            flat_output = list(_flatten(parsed_output))
            if len(flat_output) == 1:
                try:
                    path_answer = int(flat_output[0])
                    if path_answer == true_label:
                        correct_paths += 1
                except (ValueError, TypeError):
                    pass
    
    return correct_paths, syntactic_correct_paths

def extract_answer_majority_vote(all_solver_outputs):
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
    parsed_output = parse_solver_output(most_frequent_output)
    flat_output = list(_flatten(parsed_output))
    
    # Extract the answer from the majority vote result
    if len(flat_output) == 0 or parsed_output == 'syntax error':
        return None, has_tied_voting
    
    try:
        predicted_answer = int(flat_output[0])
        return predicted_answer, has_tied_voting
    except (ValueError, TypeError):
        if isinstance(flat_output[0], int):
            return flat_output[0], has_tied_voting
        else:
            return None, has_tied_voting

def extract_answer_first_list(all_solver_outputs):
    """Extract answer from first output that meets pruning criteria."""
    if not all_solver_outputs:
        return None
    
    first_output = all_solver_outputs[0]
    parsed_output = parse_solver_output(first_output)
    
    if parsed_output != 'syntax error':
        flat_output = list(_flatten(parsed_output))
        
        # Check pruning criteria: length=1 and value 0-4
        if len(flat_output) == 1:
            try:
                value = int(flat_output[0])
                if 0 <= value <= 4:
                    return value
            except (ValueError, TypeError):
                pass
    
    return None

def calculate_accuracy_generic(results, method_name, extraction_func):
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
    
    for item in results:
        if 'problem' not in item or 'label' not in item['problem']:
            continue
            
        true_label = item['problem']['label']
        all_solver_outputs = item.get('all_solver_outputs', [])
        
        total += 1
        total_paths_before += len(all_solver_outputs)
        
        # Count syntax errors
        syntax_error_count = sum(1 for output in all_solver_outputs if "execution error" in str(output))
        syntax_errors += syntax_error_count
        
        # Calculate path-level metrics
        item_correct_paths, item_syntactic_correct_paths = calculate_path_level_metrics(all_solver_outputs, true_label)
        correct_paths += item_correct_paths
        syntactic_correct_paths += item_syntactic_correct_paths
        
        # Extract answer using the provided extraction function
        extraction_result = extraction_func(all_solver_outputs)
        
        # Handle different return types from extraction functions
        if method_name == 'no_pruning_majority_vote':
            predicted_answer, has_tied_voting = extraction_result
            if has_tied_voting:
                tied_voting_samples += 1
            paths_after_pruning = len(all_solver_outputs)  # No pruning
        elif method_name == 'with_pruning_no_majority':
            predicted_answer = extraction_result
            paths_after_pruning = 1 if predicted_answer is not None else 0
        else:
            raise ValueError(f"Invalid method name: {method_name}")
        
        total_paths_after += paths_after_pruning
        
        if predicted_answer is None:
            failed_extractions += 1
        
        is_correct = predicted_answer == true_label if predicted_answer is not None else False
        if is_correct:
            correct += 1
            
        details.append({
            'id': item['problem'].get('id_string', f'item_{total}'),
            'true_label': true_label,
            'predicted': predicted_answer,
            'correct': is_correct,
            'all_outputs': all_solver_outputs,
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

def calculate_accuracy_no_pruning_majority_vote(results):
    """Calculate accuracy without pruning using all lists with majority vote."""
    return calculate_accuracy_generic(results, 'no_pruning_majority_vote', extract_answer_majority_vote)

def calculate_accuracy_with_pruning_no_majority(results):
    """Calculate accuracy with pruning (length=1, value 0-4) without majority vote (first list)."""
    return calculate_accuracy_generic(results, 'with_pruning_no_majority', extract_answer_first_list)

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python custom_ablation_analysis.py <results_directory>")
        print("Example: python custom_ablation_analysis.py results/Sketch-only-Sep18-2025/one-step-AR-LSAT-...")
        # Use default path if no argument provided
        results_dir = '/home/argustest/logic-reasoning-workspace/zhiyu/Partitioned-Neural-Symbolic-Reasoning-v0/results/Sketch-only-Sep18-2025/one-step-AR-LSAT-generate-plan-with-gpt-4-generate-code-with-gpt-4-three_shot_CoT-713e5554-8e1e-41f9-b1f8-3d4c79a16fd3'
        print(f"Using default results directory: {results_dir}")
    else:
        results_dir = sys.argv[1]
        # If relative path, make it absolute
        if not os.path.isabs(results_dir):
            results_dir = os.path.abspath(results_dir)
    
    # File paths
    summary_file = os.path.join(results_dir, 'summary.txt')
    config_file = os.path.join(results_dir, 'config.yaml')
    
    # Check if files exist
    if not os.path.exists(summary_file):
        print(f"Error: summary.txt not found at {summary_file}")
        sys.exit(1)
    if not os.path.exists(config_file):
        print(f"Error: config.yaml not found at {config_file}")
        sys.exit(1)
    
    print("Loading results...")
    results = load_results(summary_file)
    print(f"Loaded {len(results)} items")
    
    print("\nCalculating accuracy without pruning (majority vote)...")
    result1 = calculate_accuracy_no_pruning_majority_vote(results)
    
    print("\nCalculating accuracy with pruning (no majority vote)...")
    result2 = calculate_accuracy_with_pruning_no_majority(results)
    
    # Print results
    print("\n" + "="*80)
    print("ABLATION STUDY RESULTS")
    print("="*80)
    
    print(f"\n=== METHOD 1: NO PRUNING + MAJORITY VOTE ===")
    print(f"Correct: {result1['correct']}")
    print(f"Total: {result1['total']}")
    print(f"Accuracy: {result1['accuracy']:.4f} ({result1['accuracy']*100:.2f}%)")
    print(f"Accuracy by path: {result1['accuracy_by_path']:.4f} ({result1['accuracy_by_path']*100:.2f}%)")
    print(f"Correct paths: {result1['correct_paths']}")
    print(f"Syntactic correct paths: {result1['syntactic_correct_paths']}")
    print(f"Tied voting samples: {result1['tied_voting_samples']}")
    print(f"Tied voting rate: {result1['tied_voting_rate']:.4f} ({result1['tied_voting_rate']*100:.2f}%)")
    print(f"Failed extractions: {result1['failed_extractions']}")
    print(f"Syntax errors: {result1['syntax_errors']}")
    print(f"Total paths before pruning: {result1['total_paths_before']}")
    print(f"Total paths after pruning: {result1['total_paths_after']}")
    print(f"Avg paths before pruning: {result1['avg_paths_before']:.2f}")
    print(f"Avg paths after pruning: {result1['avg_paths_after']:.2f}")
    
    print(f"\n=== METHOD 2: WITH PRUNING + NO MAJORITY VOTE ===")
    print(f"Correct: {result2['correct']}")
    print(f"Total: {result2['total']}")
    print(f"Accuracy: {result2['accuracy']:.4f} ({result2['accuracy']*100:.2f}%)")
    print(f"Accuracy by path: {result2['accuracy_by_path']:.4f} ({result2['accuracy_by_path']*100:.2f}%)")
    print(f"Correct paths: {result2['correct_paths']}")
    print(f"Syntactic correct paths: {result2['syntactic_correct_paths']}")
    print(f"Failed extractions: {result2['failed_extractions']}")
    print(f"Syntax errors: {result2['syntax_errors']}")
    print(f"Total paths before pruning: {result2['total_paths_before']}")
    print(f"Total paths after pruning: {result2['total_paths_after']}")
    print(f"Avg paths before pruning: {result2['avg_paths_before']:.2f}")
    print(f"Avg paths after pruning: {result2['avg_paths_after']:.2f}")
    
    print("\nCreating comprehensive CSV file...")
    df, output_file = create_comprehensive_csv(results_dir, summary_file, config_file, result1, result2)
    
    print(f"\nResults saved to: {output_file}")
    print("\nCSV Preview:")
    print(df.to_string(index=False))
    
    # Save detailed results
    detailed_results = {
        'method1_no_pruning_majority_vote': result1,
        'method2_with_pruning_no_majority': result2
    }
    
    detailed_output_file = os.path.join(results_dir, 'detailed_ablation_results.json')
    with open(detailed_output_file, 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\nDetailed results saved to: {detailed_output_file}")

if __name__ == "__main__":
    main()
