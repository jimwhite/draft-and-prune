#!/usr/bin/env python3
import json
import google.generativeai as genai
import os
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, Union
import uuid
import openai

from config import ReasonerConfig
from data_loaders import DataLoader
from answer_extractors import AnswerExtractor
from call_api import APIConfig, get_api_client
import subprocess
import tempfile
import re
from datetime import datetime
class Reasoner(ABC):
    """Base class for different reasoning approaches"""
    
    def __init__(self, 
                 config: ReasonerConfig,
                 data_loader: DataLoader,
                 answer_extractor: AnswerExtractor):
        """Initialize the reasoner with the given components"""
        
        self.config = config
        self.data_loader = data_loader
        self.results_folder = self.create_results_folder()
        self.answer_extractor = answer_extractor
        self.summary_filepath = os.path.join(self.results_folder, "summary.txt")

        # Initialize API client
        api_config = APIConfig(
            model_name=config.model,
            temperature=config.temperature,
            max_repairs=config.max_repairs,
            inter_test_case_delay=config.test_delay
        )
        
        # Determine provider from model name and configure appropriate API
        if 'gemini' in config.model.lower():
            self.api_provider = "gemini"
            genai.configure(api_key=config.api_key)
        elif 'gpt' in config.model.lower():
            self.api_provider = "gpt"
            openai.api_key = config.api_key
        else:
            raise ValueError(f"Unsupported model: {config.model}")
            
        self.api_client = get_api_client(self.api_provider, api_config)
        fix_api_config = APIConfig(
            model_name=config.fix_model,
            temperature=config.temperature,
            max_repairs=config.max_repairs,
            inter_test_case_delay=config.test_delay
        )
        self.fix_api_client = get_api_client(self.api_provider, fix_api_config)

    @abstractmethod
    def reason(self, test_case: Dict) -> Dict:
        """Implement the reasoning strategy"""
        pass


    def create_results_folder(self) -> None:
        """Create results folder based on model name"""
        # append uuid to the results folder
        self.results_folder = f"./results/results_{datetime.now().strftime('%Y-%m-%d')}/{self.config.reasoning_method}-{self.config.dataset}-{self.config.model}-{self.config.shots}_shot_CoT-{str(uuid.uuid4())}/"
        if os.path.exists(self.results_folder):
            print(f"The results folder {self.results_folder} already exists, check whether you want to continue")
            # return self.results_folder
            # exit()
        else:
            print("No existing results found, starting fresh")
            os.makedirs(self.results_folder)
        return self.results_folder

    def _call_api(self, prompt: str) -> str:
        """Common method to call the API using the modular client"""
        return self.api_client.call(prompt)
    
    def _call_fix_api(self, prompt: str) -> str:
        """Common method to call the API using the modular client"""
        return self.fix_api_client.call(prompt)
    
    def interpret_results(self, response_text: str) -> Tuple[bool, str, Optional[str]]:
        """Interpret the results from the reasoning"""
        return True, "Model passed the test.", response_text

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float) -> None:
        """Process the results of a single test case"""
        pass

    def run_all_tests(self) -> None:
        """Run reasoning on all test cases in the file with optional limit"""
        start_time_total = time.time()
        processed_count = 0
        for i, batch in enumerate(self.data_loader):
            # Start timing for this test case
            start_time_case = time.time()
            
            # Apply reasoning
            reasoning_result = self.reason(batch[0])

            # Calculate total case time
            case_time = time.time() - start_time_case            
            
            self._process_results(batch[0], reasoning_result, case_time)

            # Increment counter and delay before next test
            processed_count += 1
            if processed_count < len(self.data_loader):  # Avoid delay after the last item
                print(f"Waiting {self.config.test_delay}s before next test case...")
                time.sleep(self.config.test_delay)

        # Calculate total execution time
        total_execution_time = time.time() - start_time_total
        print(f"\nTotal execution time: {total_execution_time:.2f}s")
       
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
                 data_loader: DataLoader,
                 answer_extractor: AnswerExtractor):
        super().__init__(config, data_loader, answer_extractor)

    def get_plan_prompt(self, test_case, feedback=None):
        """Get the plan generation prompt with the given inputs."""
        # load the plan generation prompt
        
        base_prompt_path = os.path.join(self.config.prompt_path, "plan_base.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        if self.config.shots == "zero":
            shot_prompt = ""
        else:
            shot_path = os.path.join(self.config.prompt_path, f"plan_{self.config.shots}_shot.txt")
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

    def fix_semantic_errors(self, test_case, plan):
        """Fix the semantic errors in the plan with the given inputs."""
        # load the plan feedback prompt
        print(f"Using {self.config.fix_model} to fix the semantic errors in the plan")
        
        base_prompt_path = os.path.join(self.config.prompt_path, "fix_semantic_errors.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        prompt = base_prompt.format(
            context=test_case["context"],
            question=test_case["question"],
            answers=test_case["answers"],
            plan=plan
        )

        new_plan = self._call_fix_api(prompt)
        return new_plan
        
    def get_code_prompt(self, test_case, plan, feedback=None):
        """Get the code generation prompt with the given inputs."""
        # load the code generation prompt
        
        base_prompt_path = os.path.join(self.config.prompt_path, "code_base.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        if self.config.shots == "zero":
            shot_prompt = ""
        else:
            shot_path = os.path.join(self.config.prompt_path, f"code_{self.config.shots}_shot.txt")

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
        base_prompt_path = os.path.join(self.config.prompt_path, "fix_syntax_errors.txt")
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

        if current_plan is None or plan_feedback:
            # Generate plan
            plan_prompt = self.get_plan_prompt(test_case, feedback=plan_feedback)
            current_plan = self._call_api(plan_prompt)
            print("\nGenerated plan:")
            print("=" * 80)
            print(current_plan)
            print("=" * 80)

            current_plan = self.fix_semantic_errors(test_case, current_plan)
            print("\nFixed plan:")
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

        syntax_errors = []
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
            # Execute code
            is_valid, solver_output = self.execute_z3_code(current_code)
            if not is_valid:
                print(f"\nZ3 code execution failed. Error type: {solver_output}")
                syntax_errors.append(solver_output)
            
                # Generate fix
                fix_prompt = self.fix_syntax_errors(current_code, syntax_errors)
                print("Attempting to fix syntax errors...")
                current_code = self._call_api(fix_prompt)
                current_code = self.clean_code(current_code)
                print("\nFixed Z3 Python code:")
                print("=" * 80)
                print(current_code)
                print("=" * 80)
            else:
                print("Z3 code execution succeeded.")
                break
        
        # reached max repairs
        if iteration == self.config.max_repairs - 1:
            print(f"\nReached max repairs ({self.config.max_repairs})")
        return {
            "plan": current_plan,
            "code": current_code,
            "solver_output": solver_output,
            "plan_feedback": plan_feedback,
            "code_feedback": code_feedback,
            "syntax_errors": syntax_errors
        }
        
    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float) -> None:
        # save the "plan" and "code" to the results_folder
        plan_folder = os.path.join(self.results_folder, "plan")
        code_folder = os.path.join(self.results_folder, "code")
        if not os.path.exists(plan_folder):
            os.makedirs(plan_folder)
        if not os.path.exists(code_folder):
            os.makedirs(code_folder)

        # get the problem name from the id_string if it exists, otherwise use the id_string
        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        
        # Generate unique UUID for this plan and code
        unique_id = str(uuid.uuid4())
        
        plan_filepath = os.path.join(plan_folder, f"{problem_name}-{unique_id}.txt")
        with open(plan_filepath, "w") as f:
            f.write(reasoning_result["plan"])
            
        code_filepath = os.path.join(code_folder, f"{problem_name}-{unique_id}.py")
        with open(code_filepath, "w") as f:
            f.write(reasoning_result["code"])

        # Display results
        # print("\nSolver Output:")
        # print("=" * 80)
        # print(reasoning_result["solver_output"] if reasoning_result["solver_output"] else "[No reasoning extracted]")
        # print("=" * 80)
        
        # Interpret results
        is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["label"])
        
        # Check if an answer was selected
        if is_correct:
            print(f"\nReasoning PASSED. Error type: {error_type}")
        else:
            print(f"\nReasoning FAILED. Error type: {error_type}")

        # Record result
        results = {
            "problem": test_case,
            "solver_output": reasoning_result["solver_output"],
            # "reasoning_result": reasoning_result,
            "error_type": error_type,
            "success": is_correct,
            "timing": case_time
        }

        # Append results to summary as a JSON array
        try:
            results_array = []
            if os.path.exists(self.summary_filepath) and os.path.getsize(self.summary_filepath) > 0:
                with open(self.summary_filepath, "r") as f:
                    try:
                        results_array = json.load(f)
                    except json.JSONDecodeError:
                        # If not a valid JSON, start with an empty array
                        results_array = []
            
            # Add new result to array
            results_array.append(results)
            
            # Write back the entire array
            with open(self.summary_filepath, "w") as f:
                json.dump(results_array, f, indent=2)
        except Exception as e:
            print(f"Error saving results to {self.summary_filepath}: {e}")