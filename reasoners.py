#!/usr/bin/env python3
import json
import google.generativeai as genai
import os
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, Union

from config import ReasonerConfig
from data_loaders import DatasetLoader
from answer_extractors import AnswerExtractor
from call_api import APIConfig, get_api_client
import subprocess
import tempfile
import re

class Reasoner(ABC):
    """Base class for different reasoning approaches"""
    
    def __init__(self, 
                 config: ReasonerConfig,
                 data_loader: DatasetLoader,
                 answer_extractor: AnswerExtractor):
        """Initialize the reasoner with the given components"""
        genai.configure(api_key=config.api_key)
        
        self.config = config
        self.data_loader = data_loader
        self.results_filename = self.config.get_results_filename()
        self.answer_extractor = answer_extractor
        
        # Initialize API client
        api_config = APIConfig(
            model_name=config.model_name,
            temperature=config.temperature,
            max_repairs=config.max_repairs,
            inter_test_case_delay=config.inter_test_case_delay
        )
        
        # Determine provider from model name
        if 'gemini' in config.model_name.lower():
            self.api_provider = "gemini"
        elif 'gpt' in config.model_name.lower():
            self.api_provider = "gpt"
        else:
            raise ValueError(f"Unsupported model: {config.model_name}")
            
        self.api_client = get_api_client(self.api_provider, api_config)

    @abstractmethod
    def reason(self, test_case: Dict) -> Dict:
        """Implement the reasoning strategy"""
        pass
    
    def _call_api(self, prompt: str) -> str:
        """Common method to call the API using the modular client"""
        return self.api_client.call(prompt)
    
    def interpret_results(self, response_text: str) -> Tuple[bool, str, Optional[str]]:
        """Interpret the results from the reasoning"""
        return True, "Model passed the test.", response_text

    def run_all_tests(self) -> List[Dict]:
        """Run reasoning on all test cases in the file with optional limit"""
        results = []
        start_time_total = time.time()
        if os.path.exists(self.results_filename):
            print("The results file already exists, check whether you want to continue")
            exit()
        else:
            print("No existing results found, starting fresh")

        # Load test cases
        test_cases = self.data_loader.load_data(self.config.data_path)

        # Filter out already processed cases and apply limit
        if self.config.limit is not None:
            cases_to_process = test_cases[:self.config.limit]
        else:
            cases_to_process = test_cases

        # Process each test case
        processed_count = 0
        for i, test_case in enumerate(cases_to_process):
            print(f"\n\n{'='*40} Processing Test Case {processed_count + 1}/{len(cases_to_process)} {'='*40}")
            print(f"\nAttempting reasoning")
            # Start timing for this test case
            start_time_case = time.time()
            
            # Apply reasoning
            reasoning_result = self.reason(test_case)
            
            # Display results
            print("\nModel Reasoning:")
            print("=" * 80)
            print(reasoning_result["solver_output"] if reasoning_result["solver_output"] else "[No reasoning extracted]")
            print("=" * 80)
            
            # Interpret results
            is_correct, result_message = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["label"])
            
            # Calculate total case time
            case_time = time.time() - start_time_case
            
            # Check if an answer was selected
            if is_correct:
                print(f"\nReasoning PASSED: {result_message}")
            else:
                print(f"\nReasoning FAILED: {result_message}")
            
            # Record result
            results.append({
                "problem": test_case,
                "reasoning_result": reasoning_result,
                "result_message": result_message,
                "success": is_correct,
                "timing": case_time
            })

            # Save progress after each test case
            try:
                with open(self.results_filename, "w") as f:
                    json.dump(results, f, indent=2)
            except Exception as e:
                print(f"Error saving results to {self.results_filename}: {e}")

            # Increment counter and delay before next test
            processed_count += 1
            if processed_count < len(cases_to_process):  # Avoid delay after the last item
                print(f"Waiting {self.config.inter_test_case_delay}s before next test case...")
                time.sleep(self.config.inter_test_case_delay)

        # Calculate total execution time
        total_execution_time = time.time() - start_time_total
        
        # Print summary of results
        self._print_summary(results)
        print(f"\nTotal execution time: {total_execution_time:.2f}s")
        
        return results
    
    def _print_summary(self, results: List[Dict]) -> None:
        """Print a summary of the test results"""
        print("\n\n" + "="*80)
        print("SUMMARY:")
        if not results:
            print("No results to summarize.")
            return

        # Filter results to only include those with valid IDs
        valid_results = [r for r in results]
        if not valid_results:
            print("No valid results to summarize.")
            return

        # Calculate success rate
        success_count = sum(1 for r in valid_results if r["success"])
        total_processed = len(valid_results)
        print(f"Passed: {success_count}/{total_processed} ({success_count/total_processed*100:.1f}%)")
        print(f"\nResults saved to {self.config.get_results_filename()}")
       
    def clean_code(self, code_text):
        # Clean potential markdown fences (though the prompt requests raw code)
        cleaned_code = code_text
        if "```python" in cleaned_code :
             match = re.search(r"```python\n(.*?)```", cleaned_code, re.DOTALL)
             if match:
                 cleaned_code = match.group(1).strip()
        elif cleaned_code.strip().startswith("```") and cleaned_code.strip().endswith("```"):
             cleaned_code = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned_code.strip(), count=1)
             cleaned_code = re.sub(r"\n?```$", "", cleaned_code.strip(), count=1)
             cleaned_code = cleaned_code.strip()

        # Basic check for Z3 import
        if not cleaned_code.strip().startswith("from z3 import *"):
             # If import is missing, prepend it. Add a newline for separation.
             print("Warning: 'from z3 import *' missing from generated code. Prepending it.")
             cleaned_code = "from z3 import *\n\n" + cleaned_code

        return cleaned_code
    
    def execute_z3_code(self, z3_code):
        """Execute the Python Z3 code and return the results."""
        # Identical to the original script's implementation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp_filename = tmp.name
            tmp.write(z3_code)

        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(['python3', tmp_filename],
                                   capture_output=True, text=True, timeout=30, # Reduced timeout slightly
                                   env=env)
            os.unlink(tmp_filename)

            if result.returncode != 0:
                # Include stderr and stdout for better debugging
                error_details = f"Stderr: {result.stderr}\nStdout: {result.stdout}"
                return False, f"Z3 execution error (return code {result.returncode}).\n{error_details}"

            output = result.stdout.strip() # Strip whitespace from output
            # Check common Z3 error indicators even if return code is 0
            if "error" in output.lower() or "exception" in output.lower() or "traceback" in output.lower():
                 return False, f"Z3 execution potentially failed:\nOutput:\n```\n{output}\n```\nStderr:\n```\n{result.stderr}\n```"

            # If return code is 0 and no obvious errors in output, assume success for execution step
            return True, output
        except subprocess.TimeoutExpired:
            os.unlink(tmp_filename)
            return False, "Timeout (30s) while running Z3 code. The problem or generated code may be too complex or incorrect."
        except Exception as e:
             # Clean up even if other exceptions occur
            if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
                 os.unlink(tmp_filename)
            return False, f"Error executing Z3 code: {str(e)}"
        
class TwoStepReasoner(Reasoner):
    """Two-step reasoning approach"""

    def __init__(self, 
                 config: ReasonerConfig,
                 data_loader: DatasetLoader,
                 answer_extractor: AnswerExtractor):
        super().__init__(config, data_loader, answer_extractor)

    def get_plan_prompt(self, test_case, feedback=None):
        """Get the plan generation prompt with the given inputs."""
        # load the plan generation prompt
        base_prompt_path = os.path.join(os.path.dirname(__file__), f"{self.config.dataset}-prompts/plan_base.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        if self.config.shots == "one":
            # prompt_path = os.path.join(base_prompt_path, "one-shot-plan.txt")
            raise ValueError(f"Unsupported number of shots: {self.config.shots}")
        elif self.config.shots == "two":
            shot_path = os.path.join(base_prompt_path, "plan_two_shot.txt")
        
        with open(shot_path, "r") as file:
            shot_prompt = file.read()

        # concatenate the base prompt and the shot prompt
        PLAN_GENERATION_PROMPT = base_prompt + shot_prompt

        # Pre-format the answers with json.dumps
        if self.config.dataset == "AR-LSAT":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]
            formatted_answers = json.dumps(answers, indent=2)
            
            prompt = PLAN_GENERATION_PROMPT.format(
                context=context,
                question=question,
                formatted_answers=formatted_answers
            )
        
        if feedback:
            prompt += f"\n\n# Feedback on Previous Plan Attempt:\n{feedback}\n# Please Regenerate the Plan Based on This Feedback:"
        
        return prompt

    def get_code_prompt(self, test_case, plan, feedback=None):
        """Get the code generation prompt with the given inputs."""
        # load the code generation prompt
        base_prompt_path = os.path.join(os.path.dirname(__file__), f"{self.config.dataset}-prompts/code_base.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        if self.config.shots == "one":
            # prompt_path = os.path.join(base_prompt_path, "one-shot-code.txt")
            raise ValueError(f"Unsupported number of shots: {self.config.shots}")
        elif self.config.shots == "two":
            shot_path = os.path.join(base_prompt_path, "code_two_shot.txt")

        with open(shot_path, "r") as file:
            shot_prompt = file.read()

        # concatenate the base prompt and the shot prompt
        CODE_GENERATION_PROMPT = base_prompt + shot_prompt

        # Pre-format the answers with json.dumps
        if self.config.dataset == "AR-LSAT":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]
            formatted_answers = json.dumps(answers, indent=2)

            # Now format with the regular variables
            prompt = CODE_GENERATION_PROMPT.format(
                context=context,
                question=question,
                formatted_answers=formatted_answers,
                plan=plan
            )
        
        if feedback:
            prompt += f"\n\n# Feedback on Previous Code Attempt (Based on the Plan):\n{feedback}\n# Please Correct the Code:"
        
        return prompt 

    def fix_syntax_errors(self, code, syntax_error):
        """Get the fix generation prompt with the given inputs."""
        # load the fix generation prompt
        base_prompt_path = os.path.join(os.path.dirname(__file__), f"{self.config.dataset}-prompts/fix_base.txt")
        with open(base_prompt_path, "r") as file:
            FIX_GENERATION_PROMPT = file.read()

        prompt = FIX_GENERATION_PROMPT.format(
            code=code,
            syntax_error=syntax_error
        )
        return prompt
    
    def reason(self, test_case: Dict) -> Dict:
        """Use model to reason and choose the correct answer in one step"""
        current_plan = None
        current_code = None
        solver_output = None
        plan_feedback = None
        code_feedback = None
        accumulated_errors = []
        accumulated_feedback = ""

        if current_plan is None or plan_feedback:
            # Generate plan
            plan_prompt = self.get_plan_prompt(test_case, feedback=plan_feedback)
            current_plan = self._call_api(plan_prompt)
            print("\nGenerated plan:")
            print("=" * 80)
            print(current_plan)
            print("=" * 80)

        if current_code is None or code_feedback:
            # Generate code
            code_prompt = self.get_code_prompt(test_case, current_plan, feedback=code_feedback)
            current_code = self._call_api(code_prompt)
            current_code = self.clean_code(current_code)
            print("\nGenerated Z3 Python code:")
            print("=" * 80)
            print(current_code)
            print("=" * 80)
    
        for iteration in range(self.config.max_repairs):
            # Execute code
            is_valid, solver_output = self.execute_z3_code(current_code)

            if not is_valid:
                error_message = f"Iteration {iteration+1}: Execution error: {solver_output}"
                print(f"\nZ3 code execution failed. Feedback: {solver_output}")
                
                # Add this error to accumulated errors
                accumulated_errors.append(error_message)
                
                # Create feedback with all accumulated errors
                accumulated_feedback = "\n\n".join(accumulated_errors)
                code_feedback = f"The generated code failed during execution. Please fix the errors and avoid previous mistakes:\n\nAll previous errors:\n```\n{accumulated_feedback}\n```"
                
                continue
            else:
                # combine current plan, code, and output, plan_feedback, code_feedback as dictionary
                return {
                    "plan": current_plan,
                    "code": current_code,
                    "solver_output": solver_output,
                    "plan_feedback": plan_feedback,
                    "code_feedback": code_feedback
                }
        
        # reached max repairs
        print(f"\nReached max repairs ({self.config.max_repairs})")
        return {
            "plan": current_plan,
            "code": current_code,
            "solver_output": solver_output,
            "plan_feedback": plan_feedback,
            "code_feedback": code_feedback
        }
        