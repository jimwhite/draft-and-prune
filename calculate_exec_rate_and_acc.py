#!/usr/bin/env python3
"""
Calculate execution rate and execution accuracy for each path index.

exec_rate = #no-syntax-error / #total-samples
exec_acc = #correct / #no-syntax-error

With --cot-csv option:
  - Adds cot_is_correct column by aligning on sample_id
  - Calculates overall_acc: if syntax error, use CoT as backup
  - overall_acc = #overall_correct / #total-samples

Usage:
    python calculate_exec_rate_and_acc.py <path_level_analysis.csv>
    python calculate_exec_rate_and_acc.py <path_level_analysis.csv> --cot-csv <cot_path_level_analysis.csv>
"""

import pandas as pd
import argparse
import sys
from pathlib import Path


def calculate_metrics(csv_path: str, cot_csv_path: str = None):
    """Calculate execution rate and accuracy for each path index."""
    
    # Load the CSV
    df = pd.read_csv(csv_path)
    
    # Load CoT CSV if provided
    cot_df = None
    cot_acc = None
    if cot_csv_path:
        cot_df = pd.read_csv(cot_csv_path)
        print(f"CoT CSV loaded: {cot_csv_path}")
        print(f"CoT samples: {cot_df['sample_id'].nunique()}")
        
        # Calculate CoT accuracy (using first path, path_index=0)
        cot_first_path_df = cot_df[cot_df['path_index'] == 0]
        cot_total = len(cot_first_path_df)
        cot_correct = (cot_first_path_df['is_correct'] == True).sum()
        cot_acc = cot_correct / cot_total if cot_total > 0 else 0
        print(f"CoT Accuracy (path 0): {cot_correct}/{cot_total} = {cot_acc:.2%}")
        
        # Create a mapping from (sample_id, path_index) to cot_is_correct
        # For CoT, we typically use path_index 0 for backup (or average across paths)
        # Let's use the first path (path_index=0) as the CoT backup
        cot_first_path = cot_first_path_df[['sample_id', 'is_correct']].copy()
        cot_first_path = cot_first_path.rename(columns={'is_correct': 'cot_is_correct'})
        
        # Merge CoT correctness into the main dataframe
        df = df.merge(cot_first_path, on='sample_id', how='left')
        
        # Fill missing CoT values with False
        # df['cot_is_correct'] = df['cot_is_correct'].fillna(False)
        
        # Calculate overall_correct: if syntax error, use CoT as backup
        df['overall_correct'] = df.apply(
            lambda row: row['cot_is_correct'] if row['is_syntax_error'] else row['is_correct'],
            axis=1
        )
        
        print(f"Added cot_is_correct and overall_correct columns")
        print()
    
    # Get unique path indices
    path_indices = sorted(df['path_index'].unique())
    
    print(f"Dataset: {df['dataset'].iloc[0]}")
    print(f"Experiment: {df['experiment_id'].iloc[0]}")
    print(f"Total samples: {df['sample_id'].nunique()}")
    print(f"Total paths per sample: {len(path_indices)}")
    print()
    
    results = []
    
    # Header based on whether CoT is provided
    if cot_df is not None:
        print(f"{'Path':>6} | {'Total':>7} | {'No Error':>10} | {'Correct':>8} | {'Exec Rate':>10} | {'Exec Acc':>10} | {'Overall Acc':>12}")
        print("-" * 90)
    else:
        print(f"{'Path':>6} | {'Total':>7} | {'No Error':>10} | {'Correct':>8} | {'Exec Rate':>10} | {'Exec Acc':>10}")
        print("-" * 70)
    
    for path_idx in path_indices:
        path_df = df[df['path_index'] == path_idx]
        
        total_samples = len(path_df)
        no_syntax_error = (path_df['is_syntax_error'] == False).sum()
        correct = (path_df['is_correct'] == True).sum()
        
        exec_rate = no_syntax_error / total_samples if total_samples > 0 else 0
        exec_acc = correct / no_syntax_error if no_syntax_error > 0 else 0
        
        result = {
            'path_index': path_idx,
            'total_samples': total_samples,
            'no_syntax_error': no_syntax_error,
            'correct': correct,
            'exec_rate': exec_rate,
            'exec_acc': exec_acc
        }
        
        if cot_df is not None:
            overall_correct = (path_df['overall_correct'] == True).sum()
            overall_acc = overall_correct / total_samples if total_samples > 0 else 0
            result['overall_correct'] = overall_correct
            result['overall_acc'] = overall_acc
            print(f"{path_idx:>6} | {total_samples:>7} | {no_syntax_error:>10} | {correct:>8} | {exec_rate:>10.2%} | {exec_acc:>10.2%} | {overall_acc:>12.2%}")
        else:
            print(f"{path_idx:>6} | {total_samples:>7} | {no_syntax_error:>10} | {correct:>8} | {exec_rate:>10.2%} | {exec_acc:>10.2%}")
        
        results.append(result)
    
    if cot_df is not None:
        print("-" * 90)
    else:
        print("-" * 70)
    
    # Calculate aggregate statistics
    results_df = pd.DataFrame(results)
    
    avg_exec_rate = results_df['exec_rate'].mean()
    std_exec_rate = results_df['exec_rate'].std()
    avg_exec_acc = results_df['exec_acc'].mean()
    std_exec_acc = results_df['exec_acc'].std()
    
    print(f"\nAggregate Statistics (across {len(path_indices)} paths):")
    print(f"  Avg Exec Rate: {avg_exec_rate:.2%} ± {std_exec_rate:.2%}")
    print(f"  Avg Exec Acc:  {avg_exec_acc:.2%} ± {std_exec_acc:.2%}")
    
    if cot_df is not None:
        avg_overall_acc = results_df['overall_acc'].mean()
        std_overall_acc = results_df['overall_acc'].std()
        print(f"  CoT Acc (baseline): {cot_acc:.2%}")
        print(f"  Avg Overall Acc (with CoT backup): {avg_overall_acc:.2%} ± {std_overall_acc:.2%}")
    
    # Also calculate overall metrics (treating all paths as one pool)
    total_all = len(df)
    no_error_all = (df['is_syntax_error'] == False).sum()
    correct_all = (df['is_correct'] == True).sum()
    
    overall_exec_rate = no_error_all / total_all
    overall_exec_acc = correct_all / no_error_all if no_error_all > 0 else 0
    
    print(f"\nOverall (all paths pooled):")
    print(f"  Total paths: {total_all}")
    print(f"  No syntax error: {no_error_all} ({overall_exec_rate:.2%})")
    print(f"  Correct: {correct_all} ({overall_exec_acc:.2%} of valid)")
    
    if cot_df is not None:
        overall_correct_all = (df['overall_correct'] == True).sum()
        overall_acc_all = overall_correct_all / total_all
        print(f"  Overall correct (with CoT backup): {overall_correct_all} ({overall_acc_all:.2%})")
    
    # Save results to CSV
    output_path = Path(csv_path).parent / "exec_rate_and_acc_by_path.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")
    
    # If CoT was provided, also save the augmented dataframe
    if cot_df is not None:
        augmented_path = Path(csv_path).parent / "path_level_analysis_with_cot_backup.csv"
        df.to_csv(augmented_path, index=False)
        print(f"Augmented CSV saved to: {augmented_path}")
    
    return results_df


def main():
    parser = argparse.ArgumentParser(description="Calculate execution rate and accuracy per path")
    parser.add_argument("csv_path", help="Path to path_level_analysis.csv (autoformalization)")
    parser.add_argument("--cot-csv", dest="cot_csv_path", 
                        help="Path to CoT path_level_analysis.csv for backup calculation")
    
    args = parser.parse_args()
    
    if not Path(args.csv_path).exists():
        print(f"Error: File not found: {args.csv_path}")
        sys.exit(1)
    
    if args.cot_csv_path and not Path(args.cot_csv_path).exists():
        print(f"Error: CoT file not found: {args.cot_csv_path}")
        sys.exit(1)
    
    calculate_metrics(args.csv_path, args.cot_csv_path)


if __name__ == "__main__":
    main()
