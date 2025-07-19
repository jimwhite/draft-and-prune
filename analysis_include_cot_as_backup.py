import json
import re
import argparse

def parse_summary_file(file_path):
    """Reads and parses a summary.txt file.
    
    The function tries multiple strategies to parse the file:
    1. As a standard JSON array directly from the file stream.
    2. If that fails, it reads the content, tries to fix common issues 
       (like missing enclosing brackets for a list of objects) and then parses.
    3. If that also fails, it attempts to parse as newline-delimited JSON (NDJSON).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Strategy 1: Try to load as a standard JSON array from the file stream
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Error: File {file_path} parsed as JSON, but is not a list (type: {type(data)}). Expected a list of results.")
                    return None
            except json.JSONDecodeError as e:
                print(f"Could not parse {file_path} as a single JSON array: {e}. Attempting other parsing strategies.")
                f.seek(0) # Rewind file to read content again for alternative parsing
                content = f.read().strip()
                if not content:
                    print(f"Warning: File {file_path} is empty or contains only whitespace after initial parse attempt.")
                    return []

                # Strategy 2: Try to fix if it's a list of objects missing brackets
                fixed_content = content
                if fixed_content.endswith(','): # Remove trailing comma from the whole content string
                    fixed_content = fixed_content[:-1]
                
                if not fixed_content.startswith('['):
                    fixed_content = '[' + fixed_content
                if not fixed_content.endswith(']'):
                    fixed_content = fixed_content + ']'
                
                try:
                    data = json.loads(fixed_content)
                    if isinstance(data, list):
                        print(f"Successfully parsed {file_path} by wrapping content in array brackets.")
                        return data
                    else:
                        print(f"Error: Wrapped content of {file_path} parsed as JSON, but is not a list (type: {type(data)}).")
                        return None
                except json.JSONDecodeError as e2:
                    print(f"Could not parse {file_path} even after trying to wrap with brackets: {e2}.")
                    
                    # Strategy 3: Try parsing as newline-delimited JSON (NDJSON)
                    print(f"Attempting to parse {file_path} as newline-delimited JSON (NDJSON).")
                    lines = content.splitlines()
                    parsed_ndjson = []
                    all_lines_parsed_ndjson = True
                    for i, line_str in enumerate(lines):
                        clean_line = line_str.strip()
                        if not clean_line: continue

                        clean_line_for_json = clean_line[:-1] if clean_line.endswith(',') else clean_line
                        
                        try:
                            if clean_line_for_json: # Ensure it's not empty after stripping comma
                                parsed_ndjson.append(json.loads(clean_line_for_json))
                        except json.JSONDecodeError as e_line:
                            print(f"Warning: Could not parse line {i+1} in {file_path} as JSON (NDJSON attempt): '{clean_line[:100]}...'. Error: {e_line}")
                            all_lines_parsed_ndjson = False
                            break
                    
                    if all_lines_parsed_ndjson and parsed_ndjson:
                        print(f"Successfully parsed {file_path} as NDJSON.")
                        return parsed_ndjson
                    elif not all_lines_parsed_ndjson:
                        print(f"Failed to parse {file_path} as NDJSON due to errors in one or more lines.")
                    else:
                        print(f"Failed to parse {file_path} as NDJSON (no valid JSON objects found line by line).")
                    
                    return None # All parsing strategies failed

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while processing {file_path}: {e}")
        return None

def is_option_format(solver_output):
    """Checks if solver_output matches 'Option [A-E] is correct'."""
    if not isinstance(solver_output, str):
        return False
    return re.match(r"Option [A-E] is correct", solver_output) is not None

def get_success_status(item):
    """Gets the success status from either 'majority_vote_correct' (new format) or 'success' (old format)."""
    if "majority_vote_correct" in item:
        return item.get("majority_vote_correct", False)
    else:
        return item.get("success", False)

def get_solver_outputs(item):
    """Gets solver outputs from either 'all_solver_outputs' (new format) or 'solver_output' (old format)."""
    if "all_solver_outputs" in item:
        return item.get("all_solver_outputs", [])
    else:
        solver_output = item.get("solver_output", "")
        return [solver_output] if solver_output else []

def is_new_format(item):
    """Determines if this is the new format (has majority_vote_correct) or old format (has success)."""
    return "majority_vote_correct" in item

def has_option_format_output(solver_outputs):
    """Checks if any of the solver outputs match the 'Option [A-E] is correct' format."""
    for output in solver_outputs:
        if is_option_format(output):
            return True
    return False

def no_single_answer_found(item):
    """Checks if the majority vote details indicate that no single answer was found."""
    majority_vote_details = item.get("majority_vote_details", "")
    if isinstance(majority_vote_details, str):
        return "no single answers found" in majority_vote_details.lower()
    return False

def main(main_results_file, cot_results_file):
    main_results = parse_summary_file(main_results_file)
    cot_results_raw = parse_summary_file(cot_results_file)

    if main_results is None or cot_results_raw is None:
        print("Failed to parse one or both input files. Exiting.")
        return

    if not main_results:
        print(f"No data found or parsed from the main results file: {main_results_file}")
        return
    
    # Detect format of main results
    first_item = main_results[0] if main_results else None
    if first_item:
        if is_new_format(first_item):
            print(f"Detected new format (majority_vote_correct) for main results file: {main_results_file}")
        else:
            print(f"Detected old format (success) for main results file: {main_results_file}")
    
    cot_results_map = {}
    if cot_results_raw:
        # Detect format of CoT results
        first_cot_item = cot_results_raw[0] if cot_results_raw else None
        if first_cot_item:
            if is_new_format(first_cot_item):
                print(f"Detected new format (majority_vote_correct) for CoT results file: {cot_results_file}")
            else:
                print(f"Detected old format (success) for CoT results file: {cot_results_file}")
        
        for item in cot_results_raw:
            problem_data = item.get("problem")
            if isinstance(problem_data, dict):
                problem_id = problem_data.get("id_string")
                if problem_id:
                    cot_results_map[problem_id] = item
                else:
                    print(f"Warning: CoT item missing 'id_string' in 'problem' field: {str(item)[:200]}")
            else:
                print(f"Warning: CoT item missing or invalid 'problem' field: {str(item)[:200]}")

    total_problems = 0
    correct_count = 0

    for main_item in main_results:
        total_problems += 1
        
        problem_data = main_item.get("problem")
        problem_id = None
        if isinstance(problem_data, dict):
            problem_id = problem_data.get("id_string")
        
        if not problem_id:
            print(f"Warning: Main result item missing 'id_string' or 'problem' field. Cannot use CoT backup for this item: {str(main_item)[:200]}")

        # Check if no single answer was found (regardless of ground truth success)
        if no_single_answer_found(main_item):
            # No single answer found, try CoT backup
            if problem_id and problem_id in cot_results_map:
                cot_item = cot_results_map[problem_id]
                if get_success_status(cot_item):
                    correct_count += 1
                    print(f"Info: Problem {problem_id} corrected by CoT backup (no single answer found in main).")
                else:
                    print(f"Info: Problem {problem_id} used CoT backup but CoT also failed.")
            elif problem_id:
                print(f"Info: Problem {problem_id} had no single answer found, but not found in CoT results.")
        else:
            # Single answer was found in main process, use main result
            is_successful = get_success_status(main_item)
            if is_successful:
                correct_count += 1
                print(f"Info: Problem {problem_id} solved correctly by main process.")
            else:
                print(f"Info: Problem {problem_id} had single answer from main process but was incorrect.")

    if total_problems > 0:
        success_rate = (correct_count / total_problems) * 100
        print(f"\n--- Final Results ---")
        print(f"Total problems processed: {total_problems}")
        print(f"Correctly solved (after CoT backup when no single answer found): {correct_count}")
        print(f"Final success rate: {success_rate:.2f}%")
    else:
        print("No problems processed from the main results file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate success rate with CoT backup when no single answer is found.\n"
                   "Supports both old format (with 'success' field) and new format (with 'majority_vote_correct' field).\n"
                   "CoT backup is only applied when the main process fails to find a single answer, not based on correctness.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("main_file", 
                        help="Path to the main results summary.txt file (e.g., one-step/two-step).")
    parser.add_argument("cot_file", 
                        help="Path to the CoT results summary.txt file (backup).")
    
    args = parser.parse_args()
    
    main(args.main_file, args.cot_file) 