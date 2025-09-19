#!/usr/bin/env python3
"""
Simplified analysis script for the new format.
This script only merges individual result files into summary.txt.
Detailed analysis is handled by custom_ablation_analysis.py.
"""

import json
import glob
import os
import sys

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

def main():
    """Main function to merge individual result files into summary.txt."""
    if len(sys.argv) != 2:
        print("Usage: python analysis_simple.py <summary_directory>")
        sys.exit(1)
    
    summary_directory = sys.argv[1]
    
    if not os.path.exists(summary_directory):
        print(f"Directory not found: {summary_directory}")
        sys.exit(1)
    
    # Load all results
    results = load_results_from_directory(summary_directory)
    
    if not results:
        print("No valid result files found.")
        results = []
    
    # Write merged results to summary.txt
    parent_dir = os.path.join(summary_directory, "../")
    summary_file = os.path.join(parent_dir, "summary.txt")
    
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"The merged summary file has been generated: {summary_file}")
    print(f"Merged {len(results)} result files.")
    
    # Basic statistics
    if results:
        total_time = sum(r.get("timing", 0) for r in results)
        avg_time = total_time / len(results) if results else 0
        print(f"Total samples: {len(results)}")
        print(f"Average time per sample: {avg_time:.2f} seconds")
        print(f"Total time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()