#!/usr/bin/env python3
"""
Script to analyze verification results and reasoning errors,
and generate a comprehensive summary report with visualizations.
"""

import json
import sys
import os
from collections import Counter, defaultdict
from tabulate import tabulate
import matplotlib.pyplot as plt
import re

def load_results(results_file):
    """Load results from JSON or TXT file containing JSON."""
    try:
        # Get file extension
        file_ext = os.path.splitext(results_file)[1].lower()
        
        with open(results_file, 'r') as f:
            # For both .json and .txt files, try to load as JSON
            data = json.load(f)
            
            # Handle Z3 verification format with nested structure
            if isinstance(data, dict) and "results" in data:
                results = data["results"]
                timing_info = data.get("timing-info", {})
                summary = data.get("summary", {})
                return results, timing_info, summary
            
            # Handle flat array format (could be Z3 old format, error analysis format, or new format)
            elif isinstance(data, list):
                # All flat array formats are treated the same now
                return data, {}, {}
                    
            # Handle other formats
            else:
                return data, {}, {}
                
    except Exception as e:
        print(f"Error loading results file: {e}")
        sys.exit(1)

def analyze_results(results):
    """Analyze the verification results and generate comprehensive statistics."""
    # Preprocessing
    for res in results:
        if "majority_vote_correct" in res and "success" not in res:
            res["success"] = res["majority_vote_correct"]
        if "majority_vote_details" in res and "error_type" not in res:
            res["error_type"] = res["majority_vote_details"]
    
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful
    
    # Calculate success rate
    success_rate = (successful / total) * 100 if total > 0 else 0
    
    # Calculate timing statistics
    total_time = 0
    timing_count = 0
    for result in results:
        # Check if timing is available in the result
        if "timing" in result and isinstance(result["timing"], (int, float)):
            total_time += result["timing"]
            timing_count += 1
    
    average_time = total_time / timing_count if timing_count > 0 else 0
    
    # Categorize by id_string prefix if available
    categories = {}
    for result in results:
        id_str = result.get("id", "unknown")
        # Handle new format where id might be in problem field
        if "problem" in result and "id_string" in result["problem"]:
            id_str = result["problem"]["id_string"]
            
        prefix = id_str.split('_')[0] if '_' in id_str else id_str
        
        if prefix not in categories:
            categories[prefix] = {
                "total": 0,
                "success": 0,
                "fail": 0
            }
        
        categories[prefix]["total"] += 1
        if result["success"]:
            categories[prefix]["success"] += 1
        else:
            categories[prefix]["fail"] += 1
    
    # Analyze error types
    error_types = Counter()
    error_by_problem_type = defaultdict(Counter)
    
    for result in results:
        if not result.get("success", False):
            # Extract problem type based on format
            if "problem" in result and "id_string" in result["problem"]:
                problem_id = result["problem"]["id_string"]
            else:
                problem_id = result.get("problem", {}).get("id_string", "unknown")
                
            problem_type = problem_id.split('_')[1] if '_' in problem_id and len(problem_id.split('_')) > 1 else "unknown"
            
            # Treat null/None error_type as semantic error
            error_type = result.get("error_type")
            if error_type is None:
                error_type = "semantic error"
            
            error_types[error_type] += 1
            error_by_problem_type[problem_type][error_type] += 1
        else:
            # For successful results, track by problem type
            if "problem" in result and "id_string" in result["problem"]:
                problem_id = result["problem"]["id_string"]
            else:
                problem_id = result.get("problem", {}).get("id_string", "unknown")
                
            problem_type = problem_id.split('_')[1] if '_' in problem_id and len(problem_id.split('_')) > 1 else "unknown"
            error_by_problem_type[problem_type]["success"] += 1
    
    # Calculate error rates
    error_rates = {error: (count / total) * 100 for error, count in error_types.items()}
    
    # Error subtypes for syntax errors
    error_subtypes = extract_error_subtypes(results)
    
    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
        "categories": categories,
        "timing": {
            "total_time": total_time,
            "average_time": average_time,
            "timing_count": timing_count
        },
        "error_counts": dict(error_types),
        "error_rates": error_rates,
        "error_by_problem_type": dict(error_by_problem_type),
        "error_subtypes": dict(error_subtypes)
    }

def extract_error_subtypes(results):
    """Extract more detailed error subtypes from syntax errors."""
    error_subtypes = Counter()
    
    for result in results:
        if result.get("error_type") == "syntax error":
            syntax_errors = result.get("reasoning_result", {}).get("syntax_errors", [])
            for error in syntax_errors:
                # Extract error message from the stack trace
                if "Z3Exception" in error:
                    match = re.search(r'Z3Exception: (.*?)(\n|$)', error)
                    if match:
                        error_message = match.group(1).strip()
                        error_subtypes[error_message] += 1
                elif "SyntaxError" in error:
                    match = re.search(r'SyntaxError: (.*?)(\n|$)', error)
                    if match:
                        error_message = match.group(1).strip()
                        error_subtypes[error_message] += 1
                else:
                    error_subtypes["Other syntax error"] += 1
                    
    return error_subtypes

def generate_combined_report(results, analysis, results_file, timing_info=None, summary=None):
    """Generate a comprehensive report combining verification and error analysis."""
    report = []
    
    # Add header
    report.append("# Comprehensive Analysis Report")
    report.append(f"File analyzed: {results_file}")
    report.append(f"Total problems: {analysis['total']}")
    report.append(f"Successful problems: {analysis['successful']} ({analysis['success_rate']:.2f}%)")
    report.append(f"Failed problems: {analysis['failed']} ({100 - analysis['success_rate']:.2f}%)\n")
    
    # Add timing analysis
    report.append("## Timing Analysis")
    report.append(f"Total time: {analysis['timing']['total_time']:.2f} seconds")
    report.append(f"Average time per problem: {analysis['timing']['average_time']:.2f} seconds")
    report.append(f"Problems with timing data: {analysis['timing']['timing_count']} / {analysis['total']}\n")
    
    # Add error breakdown
    if analysis['error_counts']:
        report.append("## Error Breakdown")
        for error_type, count in analysis['error_counts'].items():
            rate = analysis['error_rates'][error_type]
            report.append(f"- {error_type}: {count} problems ({rate:.2f}%)")
        
        # Add specific error type details
        if 'syntax error' in analysis['error_counts']:
            report.append(f"\n### Syntax Error Details")
            report.append(f"- Count: {analysis['error_counts']['syntax error']}")
            report.append(f"- Rate: {analysis['error_rates']['syntax error']:.2f}%")
            
            # Add syntax error subtypes if available
            if analysis['error_subtypes']:
                report.append("\n#### Syntax Error Subtypes")
                for subtype, count in analysis['error_subtypes'].items():
                    report.append(f"- {subtype}: {count} occurrences")
        
        if 'semantic error' in analysis['error_counts']:
            report.append(f"\n### Semantic Error Details")
            report.append(f"- Count: {analysis['error_counts']['semantic error']}")
            report.append(f"- Rate: {analysis['error_rates']['semantic error']:.2f}%")
    
    # Add summary information if available
    if summary:
        report.append("\n## Summary Information")
        summary_table = []
        for key, value in summary.items():
            summary_table.append([key, str(value)])
        report.append(tabulate(summary_table, headers=["Metric", "Value"], tablefmt="pipe"))
        report.append("")
    
    # Add timing information if available
    if timing_info:
        report.append("## Detailed Timing Information")
        timing_table = []
        for key, value in timing_info.items():
            timing_table.append([key, str(value)])
        report.append(tabulate(timing_table, headers=["Metric", "Value"], tablefmt="pipe"))
        report.append("")
    
    # Add category breakdown if available
    if analysis['categories']:
        report.append("## Results by Category")
        categories_table = []
        for category, stats in analysis['categories'].items():
            success_rate = (stats["success"] / stats["total"]) * 100 if stats["total"] > 0 else 0
            categories_table.append([
                category, 
                stats["total"], 
                stats["success"], 
                stats["fail"], 
                f"{success_rate:.2f}%"
            ])
        
        headers = ["Category", "Total", "Success", "Fail", "Success Rate"]
        report.append(tabulate(categories_table, headers=headers, tablefmt="pipe"))
        report.append("")
    
    # Add problem type breakdown
    if analysis['error_by_problem_type']:
        report.append("## Results by Problem Type")
        problem_type_table = []
        
        for problem_type, errors in analysis['error_by_problem_type'].items():
            total_for_type = sum(errors.values())
            success_count = errors.get('success', 0)
            success_rate = (success_count / total_for_type) * 100 if total_for_type > 0 else 0
            
            syntax_count = errors.get('syntax error', 0)
            syntax_rate = (syntax_count / total_for_type) * 100 if total_for_type > 0 else 0
            
            semantic_count = errors.get('semantic error', 0)
            semantic_rate = (semantic_count / total_for_type) * 100 if total_for_type > 0 else 0
            
            problem_type_table.append([
                problem_type,
                total_for_type,
                f"{success_count} ({success_rate:.2f}%)",
                f"{syntax_count} ({syntax_rate:.2f}%)",
                f"{semantic_count} ({semantic_rate:.2f}%)"
            ])
        
        headers = ["Problem Type", "Total", "Success", "Syntax Error", "Semantic Error"]
        report.append(tabulate(problem_type_table, headers=headers, tablefmt="pipe"))
        report.append("")
    
    # Add test details table
    report.append("## Problem Details")
    
    details_table = []
    for i, result in enumerate(results):
        # Handle different formats
        if "problem" in result and "id_string" in result["problem"]:
            id_str = result["problem"]["id_string"]
        else:
            id_str = result.get("id", f"test_{i}")
            
        status = "✓" if result["success"] else "✗"
        
        # Get expected answer based on format
        if "problem" in result and "label" in result["problem"] and "answers" in result["problem"]:
            label_idx = result["problem"]["label"]
            if 0 <= label_idx < len(result["problem"]["answers"]):
                expected = f"Option {chr(65+label_idx)}"
            else:
                expected = f"Label {label_idx}"
        else:
            expected = result.get("expected_answer", "?")
            
        timing = result.get("timing", "N/A")
        if isinstance(timing, (int, float)):
            timing = f"{timing:.2f}s"
        
        # Get result message based on format
        if "solver_output" in result:
            result_message = result["solver_output"]
        else:
            result_message = result.get("result_message", "N/A")
        
        # Get error type
        error_type = result.get("error_type", "None") if not result.get("success", False) else "N/A"
            
        details_table.append([
            i+1,
            id_str,
            status,
            expected,
            str(result_message)[:80],  # Truncate long messages
            timing,
            error_type
        ])
    
    headers = ["#", "Problem ID", "Status", "Expected", "Result Message", "Time (s)", "Error Type"]
    report.append(tabulate(details_table, headers=headers, tablefmt="pipe"))
    
    # Add failed test details
    failed_tests = [r for r in results if not r["success"]]
    if failed_tests:
        report.append("\n## Failed Problems Details")
        
        for i, test in enumerate(failed_tests):
            # Handle different formats
            if "problem" in test and "id_string" in test["problem"]:
                test_id = test["problem"]["id_string"]
                question = test["problem"].get("question", "N/A")
            elif "problem" in test and "id" in test["problem"]:
                test_id = test["problem"]["id"]
                question = test["problem"].get("question", "N/A")
            else:
                test_id = test.get("id", "unknown")
                question = test.get("question", "N/A")
                
            report.append(f"\n### Failed Problem {i+1}: {test_id}")
            report.append(f"**Question:** {question}")
            
            # Expected answer based on format
            if "problem" in test and "label" in test["problem"] and "answers" in test["problem"]:
                label_idx = test["problem"]["label"]
                if 0 <= label_idx < len(test["problem"]["answers"]):
                    expected_answer = f"Option {chr(65+label_idx)}: {test['problem']['answers'][label_idx]}"
                else:
                    expected_answer = f"Label {label_idx}"
            elif "problem" in test and "options" in test["problem"] and "answer" in test["problem"]:
                expected_answer = test["problem"]["answer"]
            else:
                expected_answer = test.get("expected_answer", "?")
                
            report.append(f"**Expected Answer:** {expected_answer}")
            
            # Get result message based on format
            if "solver_output" in test:
                result_message = test["solver_output"]
            else:
                result_message = test.get("result_message", "N/A")
                
            report.append(f"**Result Message:** {result_message}")
            report.append(f"**Error Type:** {test.get('error_type', 'semantic error')}")
            
            # Add a snippet of the code and output (truncated if too long)
            if "code" in test:
                report.append("\n**Code Snippet:**")
                code_lines = test.get("code", "").split("\n")
                report.append("```python")
                report.append("\n".join(code_lines[:20]) + ("..." if len(code_lines) > 20 else ""))
                report.append("```")
            
            if "output" in test:
                report.append("\n**Output Snippet:**")
                output_lines = test.get("output", "").split("\n")
                report.append("```")
                report.append("\n".join(output_lines[:10]) + ("..." if len(output_lines) > 10 else ""))
                report.append("```")
    
    return "\n".join(report)

def merge_summary(results_folder):
    """Merge all summary files in a folder"""
    # assert os.path.exists(results_folder) and os.path.isdir(results_folder), f"Invalid results_folder: {results_folder}"
    
    results_array = []
    for file in os.listdir(results_folder):
        if file.endswith(".json"):
            try:
                with open(os.path.join(results_folder, file), "r") as f:
                    results = json.load(f)
                results_array.append(results)
            except Exception as e:
                print(f"Error loading results from {os.path.join(results_folder, file)}: {e}")
                
    results_file = os.path.join(os.path.dirname(results_folder), "summary.txt")
    with open(results_file, "w") as f:
        json.dump(results_array, f, indent=2, ensure_ascii=False)
        
    print(f"The merged summary file has been generated: {results_file}")
    return results_file

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python analysis.py <results_file> [output_report_file/output_report_folder]")
        sys.exit(1)
    
    results_file = sys.argv[1]
    
    # If it is a folder, merge it first
    if os.path.exists(results_file) and os.path.isdir(results_file):
        results_file = merge_summary(results_file)
    
    # put the output file in the same directory as the results file
    output_file = os.path.join(os.path.dirname(results_file), os.path.basename(results_file).replace('.txt', '_analysis_report.md'))
    # file_prefix = os.path.splitext(output_file)[0]
    
    # Load results
    results, timing_info, summary = load_results(results_file)
    
    # Analyze results
    analysis = analyze_results(results)
    
    # Generate comprehensive report
    report = generate_combined_report(results, analysis, results_file, timing_info, summary)
    
    # Generate charts
    # generate_charts(analysis, file_prefix)
    
    # Output report
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Comprehensive analysis report generated: {output_file}")
    # print(f"Charts generated: {file_prefix}_*.png")

if __name__ == "__main__":
    main() 