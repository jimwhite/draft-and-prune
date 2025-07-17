#!/usr/bin/env python3
import json
import google.generativeai as genai
import os
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, Union
import uuid
import openai
import traceback

from config import ReasonerConfig
from data_loaders import DataLoader
from answer_extractors import AnswerExtractor
from call_api import APIConfig, get_api_client
from pyke import knowledge_engine
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
        self.temp_cache_dir = os.path.join(self.results_folder, "temp_cache_dir")
        if os.path.exists("./compiled_krb"):
            print('removing compiled_krb')
            os.system(f'rm -rf ./compiled_krb')

        # Initialize API client
        api_config = APIConfig(
            model_name=config.model,
            temperature=config.temperature,
            max_repairs=config.max_repairs,
            inter_test_case_delay=config.test_delay
        )

        azure_params = {}
        if config.azure_endpoint:  # Check if Azure configuration is present
            self.api_provider = "azure-openai"
            azure_params = {
                'endpoint': config.azure_endpoint,
                'deployment': config.azure_deployment,
                'managed_identity_client_id': config.azure_managed_identity_client_id
            }
            # For Azure, api_key in config is not used for client init directly
        elif 'gemini' in config.model.lower():
            self.api_provider = "gemini"
            genai.configure(api_key=config.api_key)
        elif 'gpt' in config.model.lower():
            self.api_provider = "gpt"
            # For standard GPT, API key is set globally for the openai library
            openai.api_key = config.api_key
        else:
            raise ValueError(f"Unsupported model or configuration: {config.model}")
        
        self.api_client = get_api_client(self.api_provider, api_config, **azure_params)
        
        # Initialize fix_api_client if needed
        if config.reasoning_method == "two-step" or config.reasoning_method == "three-step":
            fix_api_config = APIConfig(
                model_name=config.fix_model,
                temperature=config.temperature,
                max_repairs=config.max_repairs,
                inter_test_case_delay=config.test_delay
            )
            
            fix_azure_params = {}
            # Determine provider for fix model separately
            if config.azure_endpoint: # Assuming fix model also uses Azure if primary does
                fix_api_provider = "azure-openai"
                fix_azure_params = {
                    'endpoint': config.azure_endpoint, # Use same endpoint
                    'deployment': config.fix_model,    # Deployment name might be same as model or different
                    'managed_identity_client_id': config.azure_managed_identity_client_id
                }
            elif 'gemini' in config.fix_model.lower():
                fix_api_provider = "gemini"
                # Ensure fix_api_key is used if available, otherwise fallback to primary api_key
                genai.configure(api_key=config.fix_api_key if config.fix_api_key else config.api_key)
            elif 'gpt' in config.fix_model.lower():
                fix_api_provider = "gpt"
                openai.api_key = config.fix_api_key if config.fix_api_key else config.api_key
            else:
                raise ValueError(f"Unsupported fix model: {config.fix_model}")
            self.fix_api_client = get_api_client(fix_api_provider, fix_api_config, **fix_azure_params)
            
    def __del__(self):
        """Clean up cache files"""
        if os.path.exists("./compiled_krb"):
            print('removing compiled_krb')
            os.system(f'rm -rf ./compiled_krb')

    @abstractmethod
    def reason(self, test_case: Dict) -> Dict:
        """Implement the reasoning strategy"""
        pass


    def create_results_folder(self) -> None:
        """Create results folder based on model name"""
        # append uuid to the results folder
        self.results_folder = f"./results/results_{datetime.now().strftime('%Y-%m-%d')}/{self.config.reasoning_method}-{self.config.dataset}-generate-with-{self.config.model}-fix-with-{self.config.fix_model}-{self.config.shots}_shot_CoT-{str(uuid.uuid4())}/"
        print(f"Results folder: {self.results_folder}")
        
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
       
    def clean_code(self, code_text: str) -> str:
        if self.config.dataset.lower() == 'ar-lsat':
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
        
        # Leave it to be processed at execution time
        elif self.config.dataset.lower() == 'proofwriter':
            return code_text
        
        elif self.config.dataset.lower() == 'folio':
            matches = re.search(r"```prover9\n(.*?)```", code_text, re.DOTALL)
            if matches:
                return matches.group(1)
            else:
                print("Warning: No ```prover9 code block found in the output text.")
                return code_text
        
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for Reasoner clean_code.")
    
    def execute_z3_code(self, z3_code: str) -> Tuple[bool, str]:
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
        
    def execute_pyke_code(self, pyke_code: str) -> Tuple[bool, str]:
        """Execute the PyKe code and return the results."""
        try:
            facts = re.search(r"```facts\n(.*?)```", pyke_code, re.DOTALL).group(1)
            rules = re.search(r"```rules\n(.*?)```", pyke_code, re.DOTALL).group(1)
            query = re.search(r"```query\n(.*?)```", pyke_code, re.DOTALL).group(1)

            if "True" in query:
                final_answer = True
                query = query.replace("True", "$target")
            elif "False" in query:
                final_answer = False
                query = query.replace("False", "$target")
            else:
                raise ValueError("Boolean value for the query target not found")
            
            os.makedirs(self.temp_cache_dir, exist_ok=True)
            with open(os.path.join(self.temp_cache_dir, "facts.kfb"), 'w') as fp:
                fp.write(facts)
            with open(os.path.join(self.temp_cache_dir, "rules.krb"), 'w') as fp:
                fp.write(rules)
                
            engine = knowledge_engine.engine(self.temp_cache_dir)
            engine.reset()
            engine.activate('rules')
            engine.get_kb('facts')

            with engine.prove_goal(query.strip()) as gen:
                found = False
                for vars, plan in gen:
                    found = True
                    return True, vars['target'] == final_answer
                if not found:
                    return True, None
                
        except Exception as e:
            return False, f"Error executing PyKe Program: {str(e)}"
        
        finally:
            if os.path.exists("./compiled_krb"):
                print('removing compiled_krb')
                os.system(f'rm -rf compiled_krb/*')
    
    def execute_prover9_code(self, prover9_code: str) -> Tuple[bool, str]:
        """Execute the Prover9 code and return the results."""
        def negate_prover9_goal(prover9_input: str) -> str:
            """
            Extract the formulas(goals) block from the Prover9 input,
            negate the formula inside it, and replace the original goal
            with the negated formula. Returns the modified input string.
            """
            goal_match = re.search(
                # r"formulas\(goals\)\.\s*(.*?)\s*\.\s*end_of_list\.",
                r"formulas\(goals\)\.\s*(.*?)\s*\.",
                prover9_input,
                re.DOTALL
            )
            if not goal_match:
                raise ValueError("formulas(goals) block not found or improperly formatted.")
            
            goal_formula = goal_match.group(1).strip()
            negated_goal = f"-({goal_formula})"
            new_goal_block = f"formulas(goals).\n  {negated_goal}.\nend_of_list."
            new_input = re.sub(
                r"formulas\(goals\)\.\s*.*?\s*end_of_list\.",
                new_goal_block,
                prover9_input,
                flags=re.DOTALL
            )
            return new_input
    
        try:
            PROVER9_BIN = "../Prover9/bin/prover9"
            TIMEOUT = 10
            result = subprocess.run(
                [PROVER9_BIN],
                input = prover9_code,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                timeout = TIMEOUT,
                text = True
            )
            
            if "THEOREM PROVED" in result.stdout:
                return True, True
            elif "SEARCH FAILED" in result.stdout:
                negate_prover9_code = negate_prover9_goal(prover9_code)
                result = subprocess.run(
                    [PROVER9_BIN],
                    input = negate_prover9_code,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    timeout = TIMEOUT,
                    text = True
                )
                if "THEOREM PROVED" in result.stdout:
                    return True, False
                elif "SEARCH FAILED" in result.stdout:
                    return True, None
                else:
                    return False, result.stderr 
            else:
                return False, result.stderr 
            
        except Exception as e:
            return False, f"Error executing Prover9 Program: {str(e)}"      
    
    
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
        
        base_prompt_path = os.path.join(self.config.prompt_path, "plan.txt")
        with open(base_prompt_path, "r") as file:
            PLAN_GENERATION_PROMPT = file.read()

        # Pre-format the answers with json.dumps
        if self.config.dataset.lower() == "ar-lsat":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]
            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = PLAN_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{answers}", str(answers))
            
        elif self.config.dataset.lower() == "proofwriter":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = PLAN_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            
        elif self.config.dataset.lower() == "folio":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = PLAN_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            
        else:
            raise ValueError(f"Unsupported dataset: {self.config.dataset}")

        return prompt

    def fix_semantic_errors(self, test_case, plan):
        """Fix the semantic errors in the plan with the given inputs."""
        # load the plan feedback prompt
        print(f"Using {self.config.fix_model} to fix the semantic errors in the plan")
        
        base_prompt_path = os.path.join(self.config.prompt_path, "fix_semantic_errors.txt")
        with open(base_prompt_path, "r") as file:
            base_prompt = file.read()
        
        if self.config.dataset.lower() == "ar-lsat":
            prompt = base_prompt.format(
                context=test_case["context"],
                question=test_case["question"],
                answers=test_case["answers"],
                plan=plan
            )
        elif self.config.dataset.lower() == "proofwriter": 
            prompt = base_prompt.format(
                context=test_case["context"],
                question=test_case["question"],
                plan=plan
            )
        elif self.config.dataset.lower() == "folio": 
            prompt = base_prompt.format(
                context=test_case["context"],
                question=test_case["question"],
                plan=plan
            )
        else:
            raise ValueError(f"Unsupported dataset: {self.config.dataset}")

        new_plan = self._call_fix_api(prompt)
        return new_plan
        
    def get_code_prompt(self, test_case, plan, feedback=None):
        """Get the code generation prompt with the given inputs."""
        # load the code generation prompt
        
        base_prompt_path = os.path.join(self.config.prompt_path, "code.txt")
        with open(base_prompt_path, "r") as file:
            CODE_GENERATION_PROMPT = file.read()
        
        # Pre-format the answers with json.dumps
        if self.config.dataset.lower() == "ar-lsat":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]
            prompt = CODE_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{answers}", str(answers))
            prompt = prompt.replace("{plan}", plan)
            
        elif self.config.dataset.lower() == "proofwriter":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = CODE_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{plan}", plan)    
            
        elif self.config.dataset.lower() == "folio":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = CODE_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{plan}", plan)    
        
        else:
            # Fallback or error for unsupported datasets
            raise ValueError(f"Dataset {self.config.dataset} not configured for TwoStepReasoner prompts.")
        
        return prompt 

    def fix_syntax_errors(self, test_case, plan, code, syntax_error):
        """Get the fix generation prompt with the given inputs."""
        # load the fix generation prompt
        base_prompt_path = os.path.join(self.config.prompt_path, "fix_syntax_errors.txt")
        with open(base_prompt_path, "r") as file:
            FIX_GENERATION_PROMPT = file.read()
            
        if self.config.dataset.lower() == "ar-lsat":
            prompt = FIX_GENERATION_PROMPT.format(
                context=test_case["context"],
                question=test_case["question"],
                answers=test_case["answers"],
                plan=plan,
                code=code,
                syntax_error=syntax_error
            )
        elif self.config.dataset.lower() == "proofwriter": 
            prompt = FIX_GENERATION_PROMPT.format(
                context=test_case["context"],
                question=test_case["question"],
                plan=plan,
                code=code,
                syntax_error=syntax_error
            )
        elif self.config.dataset.lower() == "folio": 
            prompt = FIX_GENERATION_PROMPT.format(
                context=test_case["context"],
                question=test_case["question"],
                plan=plan,
                code=code,
                syntax_error=syntax_error
            )
        else:
            raise ValueError(f"Unsupported dataset: {self.config.dataset}")
        
        return prompt
    
    # def reason_z3_code(self, test_case: Dict) -> Dict:
    #     """Use model to reason and choose the correct answer in two step"""
    #     current_plan = None
    #     current_code = None
    #     solver_output = None
    #     plan_feedback = None
    #     code_feedback = None

    #     if current_plan is None or plan_feedback:
    #         # Generate plan
    #         plan_prompt = self.get_plan_prompt(test_case, feedback=plan_feedback)
    #         current_plan = self._call_api(plan_prompt)
    #         print("\nGenerated plan:")
    #         print("=" * 80)
    #         print(current_plan)
    #         print("=" * 80)

    #         # current_plan = self.fix_semantic_errors(test_case, current_plan)
    #         # print("\nFixed plan:")
    #         # print("=" * 80)
    #         # print(current_plan)
    #         # print("=" * 80)

    #     if current_code is None or code_feedback:
    #         # Generate code
    #         code_prompt = self.get_code_prompt(test_case, current_plan, feedback=code_feedback)
    #         current_code = self._call_api(code_prompt)
    #         current_code = self.clean_code(current_code)
    #         print("\nGenerated Z3 Python code:")
    #         print("=" * 80)
    #         print(current_code)
    #         print("=" * 80)

    #     syntax_errors = []
    #     for iteration in range(self.config.max_repairs):
    #         print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
    #         # Execute code
    #         is_valid, solver_output = self.execute_z3_code(current_code)
    #         if not is_valid:
    #             print(f"\nZ3 code execution failed. Error type: {solver_output}")
    #             syntax_errors.append(solver_output)
            
    #             # Generate fix
    #             fix_prompt = self.fix_syntax_errors(test_case, current_plan, current_code, syntax_errors)
    #             print("Attempting to fix syntax errors...")
    #             current_code = self._call_api(fix_prompt)
    #             current_code = self.clean_code(current_code)
    #             print("\nFixed Z3 Python code:")
    #             print("=" * 80)
    #             print(current_code)
    #             print("=" * 80)
    #         else:
    #             print("Z3 code execution succeeded.")
    #             break
        
    #     # reached max repairs
    #     if iteration == self.config.max_repairs - 1:
    #         print(f"\nReached max repairs ({self.config.max_repairs})")
    #     return {
    #         "plan": current_plan,
    #         "code": current_code,
    #         "solver_output": solver_output,
    #         "plan_feedback": plan_feedback,
    #         "code_feedback": code_feedback,
    #         "syntax_errors": syntax_errors
    #     }

    def reason_z3_code(self, test_case: Dict) -> Dict:
        """Use model to reason and choose the correct answer with enhanced diversity parameters"""
        plan_feedback = None
        code_feedback = None

        # Enhanced plan generation configurations with diverse parameters
        # temp 2 results in non-readable plan
        plan_configs = [
            {"temperature": 1.0},
            {"temperature": 1.0},
            {"temperature": 1.0},
            {"temperature": 1.0},
            {"temperature": 1.0},
        ]
        
        all_plan_results = []
        
        # Store original parameters
        original_temp = self.api_client.temperature
        
        for plan_config_idx, plan_config in enumerate(plan_configs):
            print(f"\n{'='*80}")
            print(f"GENERATING PLAN {plan_config_idx + 1}/{len(plan_configs)} with config: {plan_config}")
            print(f"{'='*80}")
            
            # Set generation parameters for plan generation
            self.api_client.temperature = plan_config["temperature"]
            
            # Generate plan
            plan_prompt = self.get_plan_prompt(test_case, feedback=plan_feedback)
            current_plan_response = self._call_api(plan_prompt)
            current_plan = current_plan_response if isinstance(current_plan_response, str) else current_plan_response[0]
            
            print(f"\nGenerated plan (config={plan_config}):")
            print("=" * 80)
            print(current_plan)
            print("=" * 80)

            # Enhanced code generation with batch generation
            code_configs = [
                {"temperature": 0.0},
                # {"temperature": 0.6},
                # {"temperature": 1.0}
            ]
            
            plan_code_results = []
            total_codes_for_plan = len(code_configs)  # Now we generate 1 code per config
            
            print(f"\nGenerating {total_codes_for_plan} codes for plan {plan_config_idx + 1}")
            
            code_gen_idx = 1
            for code_config in code_configs:
                print(f"\nCode generation with config: {code_config}")
                
                # Set generation parameters for code generation
                self.api_client.temperature = code_config["temperature"]
                
                code_prompt = self.get_code_prompt(test_case, current_plan, feedback=code_feedback)
                temp_code_response = self._call_api(code_prompt)
                
                # Since we simplified the API to always return a single response
                temp_code = temp_code_response
                temp_code = self.clean_code(temp_code)
                
                print(f"\nGenerated Z3 Python code (plan={plan_config_idx + 1}, code={code_gen_idx}/{total_codes_for_plan}):")
                print("=" * 50)
                print(temp_code)
                print("=" * 50)
                
                # Execute the code to check solver output
                for iteration in range(self.config.max_repairs):
                    print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs} for plan={plan_config_idx + 1}, code={code_gen_idx}")
                    is_valid, temp_solver_output = self.execute_z3_code(temp_code)
                    if not is_valid:
                        print(f"\nZ3 code execution failed for plan={plan_config_idx + 1}, code={code_gen_idx}. Error type: {temp_solver_output}")
                    
                        # Generate fix using single generation
                        fix_prompt = self.fix_syntax_errors(test_case, current_plan, temp_code, temp_solver_output)
                        print("Attempting to fix syntax errors...")
                        fix_response = self._call_api(fix_prompt)
                        temp_code = fix_response  # API now always returns a single string
                        temp_code = self.clean_code(temp_code)
                        print(f"\nFixed Z3 Python code (plan={plan_config_idx + 1}, code={code_gen_idx}):")
                        print("=" * 50)
                        print(temp_code)
                        print("=" * 50)
                    else:
                        print(f"Z3 code execution succeeded for plan={plan_config_idx + 1}, code={code_gen_idx}.")
                        break
                
                # Store this code generation's results
                code_result = {
                    "plan_idx": plan_config_idx + 1,
                    "code_idx": code_gen_idx,
                    "code": temp_code,
                    "solver_output": temp_solver_output,
                    "is_valid": temp_solver_output is not None,
                    "generation_config": code_config.copy()
                }
                plan_code_results.append(code_result)
                
                print(f"Plan {plan_config_idx + 1} - Code {code_gen_idx} solver output: {temp_solver_output}")
                code_gen_idx += 1
            
            # Store this plan's results
            plan_result = {
                "plan_idx": plan_config_idx + 1,
                "plan_config": plan_config.copy(),
                "plan": current_plan,
                "code_results": plan_code_results
            }
            all_plan_results.append(plan_result)
        
        # Restore original parameters
        self.api_client.temperature = original_temp
        
        return {
            "all_plan_results": all_plan_results
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
        
        # Process all plan results and collect solver outputs for majority voting
        all_plan_results = reasoning_result.get("all_plan_results", [])
        total_code_count = 0
        plan_summaries = []
        all_solver_outputs = []  # Collect all valid solver outputs for majority voting
        
        for plan_result in all_plan_results:
            plan_idx = plan_result["plan_idx"]
            plan_config = plan_result["plan_config"]
            plan_temp = plan_config["temperature"]  # Extract temperature from config
            
            # Save the plan with config info
            plan_filepath = os.path.join(plan_folder, f"{problem_name}-{unique_id}-plan{plan_idx}-temp{plan_temp}.txt")
            with open(plan_filepath, "w") as f:
                f.write(f"Plan Config: {plan_config}\n\n")
                f.write(plan_result["plan"])
            
            # Process codes for this plan
            code_results = plan_result.get("code_results", [])
            plan_code_results = []
            
            for code_result in code_results:
                code_idx = code_result["code_idx"]
                generation_config = code_result.get("generation_config", {})
                
                # Save each code with generation config info
                code_filepath = os.path.join(code_folder, f"{problem_name}-{unique_id}-plan{plan_idx}-code{code_idx}.py")
                with open(code_filepath, "w") as f:
                    f.write(f"# Plan Config: {plan_config}\n")
                    f.write(f"# Generation Config: {generation_config}\n\n")
                    f.write(code_result["code"])
                
                # Collect solver outputs for majority voting (only valid ones)
                solver_output = code_result["solver_output"]
                if solver_output is not None and code_result["is_valid"]:
                    all_solver_outputs.append(solver_output)
                
                total_code_count += 1
                
                code_eval_result = {
                    "plan_idx": plan_idx,
                    "code_idx": code_idx,
                    "solver_output": solver_output,
                    "is_valid": code_result["is_valid"],
                    "generation_config": generation_config
                }
                plan_code_results.append(code_eval_result)
                
                print(f"Plan {plan_idx} - Code {code_idx}: {'VALID' if code_result['is_valid'] else 'INVALID'} (Output: {solver_output})")
            
            plan_summaries.append({
                "plan_idx": plan_idx,
                "plan_config": plan_config,
                "total_codes": len(code_results),
                "code_results": plan_code_results
            })
        
        # Perform majority voting on all valid solver outputs
        if all_solver_outputs:
            # Interpret results
            if self.config.dataset.lower() == "ar-lsat":
                is_correct, vote_result = self.answer_extractor.extract_answer_with_majority_vote(
                all_solver_outputs, 
                test_case["label"], 
                test_case["answers"], 
                self.config.reasoning_method
            )
            elif self.config.dataset.lower() == "proofwriter":
                is_correct, vote_result = self.answer_extractor.extract_answer_with_majority_vote(
                all_solver_outputs, 
                test_case["answer"], 
                self.config.reasoning_method
            )
            elif self.config.dataset.lower() == "folio":
                is_correct, vote_result = self.answer_extractor.extract_answer_with_majority_vote(
                all_solver_outputs, 
                test_case["answer"], 
                self.config.reasoning_method
            )
            else:
                raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner AnswerExtractor.")

            print(f"\n{'='*80}")
            print(f"MAJORITY VOTE RESULT: {'PASSED' if is_correct else 'FAILED'}")
            print(f"Details: {vote_result}")
            print(f"Total valid outputs used: {len(all_solver_outputs)}")
            print(f"Total codes generated: {total_code_count}")
            print(f"Valid output rate: {len(all_solver_outputs)}/{total_code_count} = {len(all_solver_outputs)/total_code_count:.2%}")
            print(f"{'='*80}")
            
            # Record result with majority voting information
            results = {
                "problem": test_case,
                "timing": case_time,
                "majority_vote_correct": is_correct,
                "majority_vote_details": vote_result,
                "total_valid_outputs": len(all_solver_outputs),
                "total_code_count": total_code_count,
                "valid_output_rate": len(all_solver_outputs) / total_code_count if total_code_count > 0 else 0,
                "all_solver_outputs": all_solver_outputs,
                "plan_summaries": plan_summaries
            }
        else:
            print(f"\n{'='*80}")
            print(f"NO VALID SOLVER OUTPUTS FOUND")
            print(f"Total codes generated: {total_code_count}")
            print(f"All codes failed to produce valid outputs")
            print(f"{'='*80}")
            
            # Record result with no valid outputs
            results = {
                "problem": test_case,
                "timing": case_time,
                "majority_vote_correct": False,
                "majority_vote_details": "no valid outputs",
                "total_valid_outputs": 0,
                "total_code_count": total_code_count,
                "valid_output_rate": 0,
                "all_solver_outputs": [],
                "plan_summaries": plan_summaries
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


    def reason_pyke_code(self, test_case: Dict) -> Dict:
        """Use model to reason and choose the correct answer in two step"""
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

            # current_plan = self.fix_semantic_errors(test_case, current_plan)
            # print("\nFixed plan:")
            # print("=" * 80)
            # print(current_plan)
            # print("=" * 80)

        if current_code is None or code_feedback:
            # Generate code
            code_prompt = self.get_code_prompt(test_case, current_plan, feedback=code_feedback)
            current_code = self._call_api(code_prompt)
            current_code = self.clean_code(current_code)
            print("\nGenerated PyKe code:")
            print("=" * 80)
            print(current_code)
            print("=" * 80)

        syntax_errors = []
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
            # Execute code
            is_valid, solver_output = self.execute_pyke_code(current_code)
            if not is_valid:
                print(f"\nPyKe code execution failed. Error type: {solver_output}")
                syntax_errors.append(solver_output)
            
                # Generate fix
                fix_prompt = self.fix_syntax_errors(test_case, current_plan, current_code, syntax_errors)
                print("Attempting to fix syntax errors...")
                current_code = self._call_api(fix_prompt)
                current_code = self.clean_code(current_code)
                print("\nFixed PyKe code:")
                print("=" * 80)
                print(current_code)
                print("=" * 80)
            else:
                print("PyKe code execution succeeded.")
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
    
    def reason_prover9_code(self, test_case: Dict) -> Dict:
        """Use model to reason and choose the correct answer in two step"""
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

            # current_plan = self.fix_semantic_errors(test_case, current_plan)
            # print("\nFixed plan:")
            # print("=" * 80)
            # print(current_plan)
            # print("=" * 80)

        if current_code is None or code_feedback:
            # Generate code
            code_prompt = self.get_code_prompt(test_case, current_plan, feedback=code_feedback)
            current_code = self._call_api(code_prompt)
            current_code = self.clean_code(current_code)
            print("\nGenerated Prover9 code:")
            print("=" * 80)
            print(current_code)
            print("=" * 80)

        syntax_errors = []
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
            # Execute code
            is_valid, solver_output = self.execute_prover9_code(current_code)
            if not is_valid:
                print(f"\nProver9 code execution failed. Error type: {solver_output}")
                syntax_errors.append(solver_output)
            
                # Generate fix
                fix_prompt = self.fix_syntax_errors(test_case, current_plan, current_code, syntax_errors)
                print("Attempting to fix syntax errors...")
                current_code = self._call_api(fix_prompt)
                current_code = self.clean_code(current_code)
                print("\nFixed Prover9 code:")
                print("=" * 80)
                print(current_code)
                print("=" * 80)
            else:
                print("Prover9 code execution succeeded.")
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
    
    def reason(self, test_case: Dict) -> Dict:
        """Generate formal code directly in two step and execute it"""
        if self.config.dataset.lower() == "ar-lsat":
            return self.reason_z3_code(test_case)
        elif self.config.dataset.lower() == "proofwriter":
            return self.reason_pyke_code(test_case)
        elif self.config.dataset.lower() == "folio":
            return self.reason_prover9_code(test_case)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for DirectReasoner reasoning.")
        
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
        if self.config.dataset.lower() == "ar-lsat":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["label"], test_case["answers"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "proofwriter":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["answer"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "folio":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["answer"], self.config.reasoning_method)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner AnswerExtractor.")

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


class DirectReasoner(Reasoner):
    """Direct reasoning approach - generates formal code in one step"""

    def __init__(self, 
                 config: ReasonerConfig,
                 data_loader: DataLoader,
                 answer_extractor: AnswerExtractor):
        super().__init__(config, data_loader, answer_extractor)

    def get_direct_prompt(self, test_case, feedback=None):
        """Get the direct code generation prompt with the given inputs."""
        # Load the direct prompt from the specified path
        prompt_path = os.path.join(self.config.prompt_path, "prompt.txt")
        
        with open(prompt_path, "r") as file:
            DIRECT_PROMPT = file.read()

        # Pre-format the answers with json.dumps
        if self.config.dataset.lower() == "ar-lsat":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]
            
            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = DIRECT_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{answers}", str(answers))
            
        elif self.config.dataset.lower() == "proofwriter":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = DIRECT_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
        
        elif self.config.dataset.lower() == "folio":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = DIRECT_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
        
        else:
            # Fallback or error for unsupported datasets
            raise ValueError(f"Dataset {self.config.dataset} not configured for DirectReasoner prompts.")
        
        return prompt

    def fix_syntax_errors(self, test_case, code, syntax_error):
        """Get the fix generation prompt with the given inputs."""
        # load the fix generation prompt
        base_prompt_path = os.path.join(self.config.prompt_path, "fix_syntax_errors.txt")
        with open(base_prompt_path, "r") as file:
            FIX_GENERATION_PROMPT = file.read()

        if self.config.dataset.lower() == "ar-lsat":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = FIX_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{answers}", str(answers))
            prompt = prompt.replace("{code}", code)
            prompt = prompt.replace("{syntax_error}", syntax_error)
        
        elif self.config.dataset.lower() == "proofwriter":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = FIX_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{code}", code)
            prompt = prompt.replace("{syntax_error}", syntax_error)
            
        elif self.config.dataset.lower() == "folio":
            context = test_case["context"]
            question = test_case["question"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = FIX_GENERATION_PROMPT.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{code}", code)
            prompt = prompt.replace("{syntax_error}", syntax_error)
            
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for DirectReasoner fix_syntax_errors.")
        
        return prompt
    
    def reason_z3_code(self, test_case: Dict) -> Dict:
        """Generate Z3 code directly in one step and execute it"""
        current_code = None
        solver_output = None
        code_feedback = None

        # Generate code directly
        direct_prompt = self.get_direct_prompt(test_case, feedback=code_feedback)
        current_code = self._call_api(direct_prompt)
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
                fix_prompt = self.fix_syntax_errors(test_case, current_code, syntax_errors[-1])  # Use latest error
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
            "code": current_code,
            "solver_output": solver_output,
            "code_feedback": code_feedback,
            "syntax_errors": syntax_errors
        }
        
    def reason_pyke_code(self, test_case: Dict) -> Dict:
        """Generate PyKe code directly in one step and execute it"""
        current_code = None
        solver_output = None
        code_feedback = None

        # Generate code directly
        direct_prompt = self.get_direct_prompt(test_case, feedback=code_feedback)
        current_code = self._call_api(direct_prompt)
        current_code = self.clean_code(current_code)
        print("\nGenerated PyKe code:")
        print("=" * 80)
        print(current_code)
        print("=" * 80)

        syntax_errors = []
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
            # Execute code
            is_valid, solver_output = self.execute_pyke_code(current_code)
            if not is_valid:
                print(f"\nPyKe code execution failed. Error type: {solver_output}")
                syntax_errors.append(solver_output)
            
                # Generate fix
                fix_prompt = self.fix_syntax_errors(test_case, current_code, syntax_errors[-1])  # Use latest error
                print("Attempting to fix syntax errors...")
                current_code = self._call_api(fix_prompt)
                current_code = self.clean_code(current_code)
                print("\nFixed PyKe code:")
                print("=" * 80)
                print(current_code)
                print("=" * 80)
            else:
                print("PyKe code execution succeeded.")
                break
        
        # reached max repairs
        if iteration == self.config.max_repairs - 1:
            print(f"\nReached max repairs ({self.config.max_repairs})")
            
        return {
            "code": current_code,
            "solver_output": solver_output,
            "code_feedback": code_feedback,
            "syntax_errors": syntax_errors
        }
    
    def reason_prover9_code(self, test_case: Dict) -> Dict:
        """Generate Prover9 code directly in one step and execute it"""
        current_code = None
        solver_output = None
        code_feedback = None

        # Generate code directly
        direct_prompt = self.get_direct_prompt(test_case, feedback=code_feedback)
        current_code = self._call_api(direct_prompt)
        current_code = self.clean_code(current_code)
        print("\nGenerated Prover9 code:")
        print("=" * 80)
        print(current_code)
        print("=" * 80)

        syntax_errors = []
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs}")
            # Execute code
            is_valid, solver_output = self.execute_prover9_code(current_code)
            if not is_valid:
                print(f"\nProver9 code execution failed. Error type: {solver_output}")
                syntax_errors.append(solver_output)
            
                # Generate fix
                fix_prompt = self.fix_syntax_errors(test_case, current_code, syntax_errors[-1])  # Use latest error
                print("Attempting to fix syntax errors...")
                current_code = self._call_api(fix_prompt)
                current_code = self.clean_code(current_code)
                print("\nFixed Prover9 code:")
                print("=" * 80)
                print(current_code)
                print("=" * 80)
            else:
                print("Prover9 code execution succeeded.")
                break
        
        # reached max repairs
        if iteration == self.config.max_repairs - 1:
            print(f"\nReached max repairs ({self.config.max_repairs})")
            
        return {
            "code": current_code,
            "solver_output": solver_output,
            "code_feedback": code_feedback,
            "syntax_errors": syntax_errors
        }
    
    def reason(self, test_case: Dict) -> Dict:
        """Generate formal code directly in one step and execute it"""
        if self.config.dataset.lower() == "ar-lsat":
            return self.reason_z3_code(test_case)
        elif self.config.dataset.lower() == "proofwriter":
            return self.reason_pyke_code(test_case)
        elif self.config.dataset.lower() == "folio":
            return self.reason_prover9_code(test_case)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for DirectReasoner reasoning.")
            
    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float) -> None:
        # save the "code" to the results_folder
        code_folder = os.path.join(self.results_folder, "code")
        if not os.path.exists(code_folder):
            os.makedirs(code_folder)

        # get the problem name from the id_string if it exists, otherwise use the id_string
        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        
        # Generate unique UUID for this code
        unique_id = str(uuid.uuid4())
        
        code_filepath = os.path.join(code_folder, f"{problem_name}-{unique_id}.py")
        with open(code_filepath, "w") as f:
            f.write(reasoning_result["code"])

        # Interpret results
        if self.config.dataset.lower() == "ar-lsat":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["label"], test_case["answers"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "proofwriter":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["answer"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "folio":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["solver_output"], test_case["answer"], self.config.reasoning_method)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner AnswerExtractor.")
        
        # Check if an answer was selected
        if is_correct:
            print(f"\nReasoning PASSED. Error type: {error_type}")
        else:
            print(f"\nReasoning FAILED. Error type: {error_type}")

        # Record result
        results = {
            "problem": test_case,
            "solver_output": reasoning_result["solver_output"],
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


class CoTReasoner(Reasoner):
    """Chain-of-Thought reasoning approach"""

    def __init__(self,
                 config: ReasonerConfig,
                 data_loader: DataLoader,
                 answer_extractor: AnswerExtractor):
        super().__init__(config, data_loader, answer_extractor)

    def get_cot_prompt(self, test_case: Dict) -> str:
        """Get the CoT prompt with the given inputs."""
        # Load the CoT prompt from the specified path
        # Assuming the prompt path is relative to the project root or a known directory
        # For example, using the path provided in the context
        prompt_path = os.path.join(self.config.prompt_path, "prompt.txt")
        
        with open(prompt_path, "r") as file:
            COT_PROMPT_TEMPLATE = file.read()

        if self.config.dataset.lower() == "ar-lsat":
            context = test_case["context"]
            question = test_case["question"]
            answers = test_case["answers"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = COT_PROMPT_TEMPLATE.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{answers}", str(answers))
            
        elif self.config.dataset.lower() == "proofwriter":
            context = test_case["context"]
            question = test_case["question"]
            options = test_case["options"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = COT_PROMPT_TEMPLATE.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{options}", str(options))    
        
        elif self.config.dataset.lower() == "folio":
            context = test_case["context"]
            question = test_case["question"]
            options = test_case["options"]

            # Use string replacement instead of .format() to avoid curly brace issues
            prompt = COT_PROMPT_TEMPLATE.replace("{context}", context)
            prompt = prompt.replace("{question}", question)
            prompt = prompt.replace("{options}", str(options))
        
        else:
            # Fallback or error for unsupported datasets
            raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner prompts.")
        
        return prompt

    def reason(self, test_case: Dict) -> Dict:
        """Generate reasoning using the CoT prompt"""
        cot_prompt = self.get_cot_prompt(test_case)
        
        print("\nGenerating CoT reasoning:")
        print("=" * 80)
        # print(cot_prompt) # Optional: print the prompt for debugging
        print("=" * 80)

        reasoning_output = self._call_api(cot_prompt)
        
        print("\nGenerated CoT Output:")
        print("=" * 80)
        print(reasoning_output)
        print("=" * 80)
        
        return {
            "reasoning_output": reasoning_output
        }

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float) -> None:
        # Save the "reasoning_output" to the results_folder
        reasoning_folder = os.path.join(self.results_folder, "reasoning")
        if not os.path.exists(reasoning_folder):
            os.makedirs(reasoning_folder)

        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        
        unique_id = str(uuid.uuid4())
        
        reasoning_filepath = os.path.join(reasoning_folder, f"{problem_name}-{unique_id}.txt")
        with open(reasoning_filepath, "w") as f:
            f.write(reasoning_result["reasoning_output"])

        if self.config.dataset.lower() == "ar-lsat":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["reasoning_output"], test_case["label"], test_case["answers"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "proofwriter":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["reasoning_output"], test_case["answer"], self.config.reasoning_method)
        elif self.config.dataset.lower() == "folio":
            is_correct, error_type = self.answer_extractor.extract_answer(reasoning_result["reasoning_output"], test_case["answer"], self.config.reasoning_method)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner AnswerExtractor.")
        
        if is_correct:
            print(f"\nReasoning PASSED. Error type: {error_type}")
        else:
            print(f"\nReasoning FAILED. Error type: {error_type}")

        results = {
            "problem": test_case,
            "reasoning_output": reasoning_result["reasoning_output"],
            "error_type": error_type,
            "success": is_correct,
            "timing": case_time
        }

        try:
            results_array = []
            if os.path.exists(self.summary_filepath) and os.path.getsize(self.summary_filepath) > 0:
                with open(self.summary_filepath, "r") as f:
                    try:
                        results_array = json.load(f)
                    except json.JSONDecodeError:
                        results_array = []
            
            results_array.append(results)
            
            with open(self.summary_filepath, "w") as f:
                json.dump(results_array, f, indent=2)
        except Exception as e:
            print(f"Error saving results to {self.summary_filepath}: {e}")