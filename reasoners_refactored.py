#!/usr/bin/env python3

import os
import re
import json
import time
import uuid
import shutil
import openai
import tempfile
import traceback
import subprocess
import multiprocessing as mp
import google.generativeai as genai

from datetime import datetime
from contextlib import redirect_stdout
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional, Any, Union, Literal, Callable
from pyke import knowledge_engine

from config import ReasonerConfig
from data_loaders import DataLoader
from answer_extractors import AnswerExtractor
from call_api import APIConfig, get_api_client, APIClient


def _parallel_worker(args: Tuple[Any, Dict, Any, int]) -> None:
    """
    Executes the test task in a single subprocess and redirects all standard output to the specified file
    """
    test_runner_instance, test_case, mp_lock, sample_index = args
    
    problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
    unique_id = str(uuid.uuid4())
    log_filepath = os.path.join(test_runner_instance.log_folder, f"{problem_name}-{unique_id}.txt")
    print(f"Start working on {problem_name}...")

    try:
        # Open a log file and redirect stdout to it
        with open(log_filepath, 'w', encoding='utf-8') as log_file:
            with redirect_stdout(log_file):
                # Start recording information in the log
                print(f"--- Log for Task ID: {problem_name} ---")
                print(f"Process ID: {os.getpid()}")
                start_process_time = time.time()
                print(f"Start Time: {datetime.fromtimestamp(start_process_time).strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 30 + "\n")

                # Assign API key based on sample index for batch-based key distribution
                if hasattr(test_runner_instance.config, 'gemini_api_keys') and test_runner_instance.config.gemini_api_keys:
                    num_keys = len(test_runner_instance.config.gemini_api_keys)
                    assigned_key_index = sample_index % num_keys
                    assigned_key = test_runner_instance.config.gemini_api_keys[assigned_key_index]
                    print(f"Sample {sample_index}: Assigned API Key #{assigned_key_index + 1} ({assigned_key[:20]}...)")
                    
                    # Update both main API client and fix API client with the assigned key
                    if hasattr(test_runner_instance.api_client, 'api_key'):
                        import google.generativeai as genai
                        genai.configure(api_key=assigned_key)
                        test_runner_instance.api_client.api_key = assigned_key
                        print(f"Main API client updated with key #{assigned_key_index + 1}")
                        
                        # Also update fix API client if it exists
                        if hasattr(test_runner_instance, 'code_api_client') and hasattr(test_runner_instance.code_api_client, 'api_key'):
                            test_runner_instance.code_api_client.api_key = assigned_key
                            print(f"Fix API client also updated with key #{assigned_key_index + 1}")

            # Call the instance's reason method
            reasoning_result = test_runner_instance.reason(test_case, mp_lock)
            
            test_runner_instance._process_results(test_case, reasoning_result, 0.0, unique_id, None)

            print(f"\n" + "-" * 30)
            print(f"Task finished.")

    except Exception as e:
        # If an error occurs during execution, the error message will also be recorded
        with open(log_filepath, 'a', encoding='utf-8') as log_file:
            log_file.write("\n\n****** AN ERROR OCCURRED ******\n")
            log_file.write(traceback.format_exc())
            
    finally:
        print(f"End working on {problem_name}")


class DatasetConfig:
    """Configuration for dataset-specific operations"""
    
    DATASET_SOLVER_MAP = {
        'ar-lsat': 'z3',
        'proofwriter': 'pyke', 
        'folio': 'prover9',
        'prontoqa': 'pyke',
        'logicaldeduction': 'pythonconstraint'
    }
    
    DATASET_IMPORTS = {
        'ar-lsat': 'from z3 import *',
        'logicaldeduction': 'from constraint import *'
    }
    
    @classmethod
    def get_solver(cls, dataset: str) -> str:
        """Get the solver name for a dataset"""
        return cls.DATASET_SOLVER_MAP.get(dataset.lower())
    
    @classmethod
    def get_required_import(cls, dataset: str) -> Optional[str]:
        """Get the required import statement for a dataset"""
        return cls.DATASET_IMPORTS.get(dataset.lower())


class PromptHandler:
    """Handles prompt generation for different datasets and reasoning methods"""
    
    def __init__(self, prompt_path: str, dataset: str):
        self.prompt_path = prompt_path
        self.dataset = dataset.lower()
    
    def _load_template(self, template_name: str) -> str:
        """Load a prompt template from file"""
        template_path = os.path.join(self.prompt_path, template_name)
        with open(template_path, "r") as file:
            return file.read()
    
    def _format_prompt(self, template: str, test_case: Dict, **kwargs) -> str:
        """Format a prompt template with test case data"""
        prompt = template
        
        # Common replacements for all datasets
        if 'context' in test_case:
            prompt = prompt.replace("{context}", test_case["context"])
        if 'question' in test_case:
            prompt = prompt.replace("{question}", test_case["question"])
        
        # Dataset-specific replacements
        if self.dataset == "ar-lsat" and 'answers' in test_case:
            prompt = prompt.replace("{answers}", str(test_case["answers"]))
        elif self.dataset in ["proofwriter", "folio", "prontoqa"] and 'options' in test_case:
            prompt = prompt.replace("{options}", str(test_case["options"]))
        elif self.dataset == 'logicaldeduction':
            if 'options' in test_case:
                prompt = prompt.replace("{options}", str(test_case["options"]))
        
        # Additional replacements from kwargs
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        
        return prompt
    
    def get_plan_prompt(self, test_case: Dict, feedback: Optional[str] = None) -> str:
        """Generate plan generation prompt"""
        template = self._load_template("plan.txt")
        return self._format_prompt(template, test_case)
    
    def get_code_prompt(self, test_case: Dict, plan: str, feedback: Optional[str] = None) -> str:
        """Generate code generation prompt"""
        template = self._load_template("code.txt")
        return self._format_prompt(template, test_case, plan=plan)
    
    def get_direct_prompt(self, test_case: Dict, feedback: Optional[str] = None) -> str:
        """Generate direct code generation prompt"""
        template = self._load_template("prompt.txt")
        return self._format_prompt(template, test_case)
    
    def get_cot_prompt(self, test_case: Dict) -> str:
        """Generate Chain-of-Thought prompt"""
        template = self._load_template("prompt.txt")
        return self._format_prompt(template, test_case)
    
    def get_fix_syntax_error_prompt(self, test_case: Dict, code: str, syntax_error: str, plan: Optional[str] = None) -> str:
        """Generate syntax error fix prompt"""
        template = self._load_template("fix_syntax_errors.txt")
        kwargs = {"code": code, "syntax_error": syntax_error}
        if plan is not None:
            kwargs["plan"] = plan
        return self._format_prompt(template, test_case, **kwargs)


class CodeExecutor:
    """Handles code execution for different solvers"""
    
    def __init__(self, temp_cache_dir: str):
        self.temp_cache_dir = temp_cache_dir
    
    def execute_z3_code(self, z3_code: str) -> Tuple[bool, str]:
        """Execute the Python Z3 code and return the results."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp_filename = tmp.name
            tmp.write(z3_code)

        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(['python3', tmp_filename],
                                   capture_output=True, text=True, timeout=30,
                                   env=env)
            os.unlink(tmp_filename)

            if result.returncode != 0:
                error_details = f"Stderr: {result.stderr}\nStdout: {result.stdout}"
                return False, f"Z3 execution error (return code {result.returncode}).\n{error_details}"

            output = result.stdout.strip()
            if "error" in output.lower() or "exception" in output.lower() or "traceback" in output.lower():
                 return False, f"Z3 execution potentially failed:\nOutput:\n```\n{output}\n```\nStderr:\n```\n{result.stderr}\n```"

            return True, output
        except subprocess.TimeoutExpired:
            os.unlink(tmp_filename)
            return False, "Timeout (30s) while running Z3 code. The problem or generated code may be too complex or incorrect."
        except Exception as e:
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

            answer_list = []
            with engine.prove_goal(query.strip()) as gen:
                found = False
                for vars, plan in gen:
                    found = True
                    answer_list.append(vars['target'])
                if not found:
                    return True, "Unknown"
                else:
                    if True in answer_list and False in answer_list:
                        return True, "multiple answers"
                    else:
                        return True, str(answer_list[0] == final_answer)
                    
        except Exception as e:
            return False, f"Error executing PyKe Program: {str(e)}"
        
        finally:
            if os.path.exists("./compiled_krb"):
                print('removing compiled_krb')
                os.system(f'rm -rf compiled_krb/*')
    
    def execute_csp_code(self, csp_code: str) -> Tuple[bool, str]:
        """Execute the Python CSP code and return the results."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp_filename = tmp.name
            tmp.write(csp_code)

        try:
            env = os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            result = subprocess.run(['python3', tmp_filename],
                                   capture_output=True, text=True, timeout=20,
                                   env=env)
            os.unlink(tmp_filename)

            if result.returncode != 0:
                error_details = f"Stderr: {result.stderr}\nStdout: {result.stdout}"
                return False, f"CSP execution error (return code {result.returncode}).\n{error_details}"

            output = result.stdout.strip()
            if "error" in output.lower() or "exception" in output.lower() or "traceback" in output.lower():
                 return False, f"CSP execution potentially failed:\nOutput:\n```\n{output}\n```\nStderr:\n```\n{result.stderr}\n```"

            return True, output
        except subprocess.TimeoutExpired:
            os.unlink(tmp_filename)
            return False, "Timeout (30s) while running CSP code. The problem or generated code may be too complex or incorrect."
        except Exception as e:
            if 'tmp_filename' in locals() and os.path.exists(tmp_filename):
                 os.unlink(tmp_filename)
            return False, f"Error executing CSP code: {str(e)}"
    
    def get_execute_function(self, solver_name: str) -> Callable[[str], Tuple[bool, str]]:
        """Get the execution function for a solver"""
        solver_map = {
            'z3': self.execute_z3_code,
            'pyke': self.execute_pyke_code,
            'pythonconstraint': self.execute_csp_code
        }
        return solver_map.get(solver_name)


class CodeCleaner:
    """Handles code cleaning for different datasets"""
    
    @staticmethod
    def clean_code(code_text: str, dataset: str) -> str:
        """Clean the code from the model output which have '```python' or '```' fences"""
        dataset = dataset.lower()
        
        if dataset in ['ar-lsat', 'logicaldeduction']:
            # Clean potential markdown fences
            cleaned_code = code_text
            if "```python" in cleaned_code:
                match = re.search(r"```python\n(.*?)```", cleaned_code, re.DOTALL)
                if match:
                    cleaned_code = match.group(1).strip()
            elif cleaned_code.strip().startswith("```") and cleaned_code.strip().endswith("```"):
                cleaned_code = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned_code.strip(), count=1)
                cleaned_code = re.sub(r"\n?```$", "", cleaned_code.strip(), count=1)
                cleaned_code = cleaned_code.strip()

            # Add required import if missing
            required_import = DatasetConfig.get_required_import(dataset)
            if required_import and not cleaned_code.strip().startswith(required_import):
                print(f"Warning: '{required_import}' missing from generated code. Prepending it.")
                cleaned_code = required_import + "\n\n" + cleaned_code

            return cleaned_code
        
        elif dataset == 'proofwriter':
            return code_text
        
        elif dataset == 'folio':
            matches = re.search(r"```prover9\n(.*?)```", code_text, re.DOTALL)
            if matches:
                return matches.group(1)
            else:
                print("Warning: No ```prover9 code block found in the output text.")
                return code_text
        
        elif dataset == 'prontoqa':
            return code_text
        
        else:
            raise ValueError(f"Dataset {dataset} not configured for code cleaning.")


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
        
        self.summary_folder = os.path.join(self.results_folder, "summary")
        self.log_folder = os.path.join(self.results_folder, "log")
        os.makedirs(self.summary_folder, exist_ok=True)
        os.makedirs(self.log_folder, exist_ok=True)
        
        # Initialize temp cache directory for PyKe
        self.temp_cache_dir = os.path.join(self.results_folder, "temp_cache_dir")
        if os.path.exists("./compiled_krb"):
            print('removing compiled_krb')
            os.system(f'rm -rf ./compiled_krb')

        # Initialize helper classes
        self.prompt_handler = PromptHandler(config.prompt_path, config.dataset)
        self.code_executor = CodeExecutor(self.temp_cache_dir)
        
        # Initialize API clients based on reasoning method
        if config.reasoning_method == "cot" or config.reasoning_method == "one-step":
            model = getattr(config, 'model', None)
            api_config = APIConfig(
                model_name=model,
                temperature=config.temperature,
                max_retries=config.max_retries,
                inter_test_case_delay=config.test_delay
            )
            self.api_client = self.initialize_api_client(model, api_config)

        # Initialize code_api_client if needed for code generation
        if config.reasoning_method == "two-step" or config.reasoning_method == "three-step":
            plan_model = getattr(config, 'plan_model', None)
            print(f"Plan model: {plan_model}")
            if plan_model is None:
                raise ValueError("plan_model is not set")
            api_config = APIConfig(
                model_name=plan_model,
                temperature=config.plan_temp,
                max_retries=config.max_retries,
                inter_test_case_delay=config.test_delay
            )
            self.api_client = self.initialize_api_client(plan_model, api_config)

            code_model = getattr(config, 'code_model', None)
            print(f"Code model: {code_model}")
            if code_model is None:
                raise ValueError("code_model is not set")
            fix_api_config = APIConfig(
                model_name=code_model,
                temperature=config.code_temp,
                max_retries=config.max_retries,
                inter_test_case_delay=config.test_delay
            )
            
            self.code_api_client = self.initialize_api_client(code_model, fix_api_config)

    def initialize_api_client(self, model_name: str, api_config: APIConfig) -> APIClient:
        """Initialize the API client for the given model name and API configuration"""
        client_params = {}
        if 'gpt' in model_name.lower():
            api_config.provider = "azure-openai"
            client_params = {
                'endpoint': self.config.azure_endpoint,
                'deployment': self.config.azure_deployment,
                'managed_identity_client_id': self.config.azure_managed_identity_client_id
            }
        elif 'gemini' in model_name.lower():
            api_config.provider = "gemini"
            if self.config.gemini_api_keys:
                client_params = {'api_keys': self.config.gemini_api_keys}
                print(f"Initialized Gemini client with {len(self.config.gemini_api_keys)} API keys for rotation")
            else:
                client_params = {'api_key': self.config.gemini_api_key}
        else:
            raise ValueError(f"Unsupported plan model: {model_name}")
        
        api_client = get_api_client(api_config.provider, api_config, **client_params)
        return api_client
    
    def save_prompts_folder(self) -> None:
        """Copy the prompts folder to the results directory to preserve exact prompts used"""
        if not os.path.exists(self.config.prompt_path):
            print(f"Warning: Prompt path {self.config.prompt_path} does not exist, skipping prompt folder copy")
            return
            
        prompts_dest = os.path.join(self.results_folder, "prompts")
        
        try:
            if os.path.exists(prompts_dest):
                print(f"Prompts folder already exists at {prompts_dest}, removing old copy...")
                shutil.rmtree(prompts_dest)
            
            shutil.copytree(self.config.prompt_path, prompts_dest)
            print(f"✅ Prompts folder copied to: {prompts_dest}")
            
            prompt_metadata = {
                "original_prompt_path": self.config.prompt_path,
                "copied_at": datetime.now().isoformat(),
                "reasoning_method": self.config.reasoning_method,
                "dataset": self.config.dataset,
                "shots": self.config.shots
            }
            
            metadata_path = os.path.join(prompts_dest, "prompt_metadata.json")
            with open(metadata_path, 'w') as f:
                json.dump(prompt_metadata, f, indent=2)
            
            print(f"✅ Prompt metadata saved to: {metadata_path}")
            
        except Exception as e:
            print(f"❌ Error copying prompts folder: {e}")
            print(f"   Source: {self.config.prompt_path}")
            print(f"   Destination: {prompts_dest}")

    @abstractmethod
    def reason(self, test_case: Dict) -> Dict:
        """Implement the reasoning strategy"""
        pass

    def create_results_folder(self) -> None:
        """Create results folder based on model name"""
        plan_model_name = getattr(self.config, 'plan_model', None)
        if plan_model_name is None:
            raise ValueError("plan_model is not set")
        code_model_name = getattr(self.config, 'code_model', None)
        if code_model_name is None:
            raise ValueError("code_model is not set")
        self.results_folder = f"./results/results_{datetime.now().strftime('%Y-%m-%d')}/{self.config.reasoning_method}-{self.config.dataset}-plan-with-{plan_model_name}-code-with-{code_model_name}-{self.config.shots}_shot_CoT-{str(uuid.uuid4())}/"
        print(f"Results folder: {self.results_folder}")
        
        if os.path.exists(self.results_folder):
            print(f"The results folder {self.results_folder} already exists, check whether you want to continue")
        else:
            print("No existing results found, starting fresh")
            os.makedirs(self.results_folder)
        return self.results_folder

    def _call_api(self, prompt: str) -> str:
        """Common method to call the API using the modular client"""
        return self.api_client.call(prompt)
    
    def _call_fix_api(self, prompt: str) -> str:
        """Common method to call the API using the modular client"""
        return self.code_api_client.call(prompt)
    
    def interpret_results(self, response_text: str) -> Tuple[bool, str, Optional[str]]:
        """Interpret the results from the reasoning"""
        return True, "Model passed the test.", response_text

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float, unique_id: str="", timing_data: Optional[Dict] = None) -> None:
        """Process the results of a single test case"""
        pass

    def run_all_tests(self) -> None:
        """Run reasoning on all test cases in the file with optional limit"""
        start_time_total = time.time()
        processed_count = 0
        for i, batch in enumerate(self.data_loader):
            reasoning_result = self.reason(batch[0])
            self._process_results(batch[0], reasoning_result, 0.0, str(uuid.uuid4()), None)

            processed_count += 1
            if processed_count < len(self.data_loader):
                print(f"Waiting {self.config.test_delay}s before next test case...")
                time.sleep(self.config.test_delay)

        total_execution_time = time.time() - start_time_total
        print(f"\nTotal execution time: {total_execution_time:.2f}s")
        
    def run_all_tests_parallel(self, num_processes: int=10) -> None:
        """Use multiple processes to run all test cases in parallel"""
        print(f"Start parallel testing, using {num_processes} processes...")
        print(f"Please visit the {self.log_folder} to view the real-time output log")

        start_time_total = time.time()
        
        mp_lock = mp.Lock()
        all_tasks = [(self, batch[0], mp_lock, idx) for idx, batch in enumerate(self.data_loader)]
        processes = []
        try:
            for task in all_tasks:
                while len(processes) >= num_processes:
                    processes = [p for p in processes if p.is_alive()]
                    time.sleep(0.1)
                p = mp.Process(target=_parallel_worker, args=(task,))
                p.start()
                processes.append(p)
        except KeyboardInterrupt:
            print("KeyboardInterrupt received! Terminating all processes...")
            for p in processes:
                if p.is_alive():
                    p.terminate()
        finally:
            for p in processes:
                p.join()
            print("All processes joined.")

        total_execution_time = time.time() - start_time_total
        print(f"\nTotal execution time: {total_execution_time:.2f}s")
        with open(os.path.join(self.results_folder, "total_execution_time.txt"), "w") as f:
            f.write(f"{total_execution_time:.2f}s")


class CodeBasedReasoner(Reasoner):
    """Base class for reasoners that generate and execute code"""
    
    def reason_code_diversity(self, 
                              test_case: dict,
                              solver_name: str,
                              mp_lock: Optional[Any] = None) -> dict:
        """Generate and execute code with diversity parameters"""
        execute_func = self.code_executor.get_execute_function(solver_name)
        if execute_func is None:
            raise ValueError(f"Unsupported solver: {solver_name}")
        
        return self._generate_and_execute_code(test_case, solver_name, execute_func, mp_lock)
    
    @abstractmethod
    def _generate_and_execute_code(self, test_case: dict, solver_name: str, execute_func: Callable, mp_lock: Optional[Any] = None) -> dict:
        """Generate and execute code - to be implemented by subclasses"""
        pass
    
    def reason(self, test_case: Dict, mp_lock: Optional[Any]=None) -> Dict:
        """Main reasoning entry point"""
        solver_name = DatasetConfig.get_solver(self.config.dataset)
        if solver_name is None:
            raise ValueError(f"Dataset {self.config.dataset} not configured for reasoning.")
        return self.reason_code_diversity(test_case, solver_name, mp_lock)


class TwoStepReasoner(CodeBasedReasoner):
    """Two-step reasoning approach"""

    def _generate_and_execute_code(self, test_case: dict, solver_name: str, execute_func: Callable, mp_lock: Optional[Any] = None) -> dict:
        """Generate plans and codes with diversity parameters"""
        plan_configs = [{"temperature": self.config.plan_temp} for _ in range(self.config.num_paths)]
        all_plan_results = []
        
        for plan_config_idx, plan_config in enumerate(plan_configs):
            print(f"Generating plan {plan_config_idx + 1}/{len(plan_configs)}...")
            self.api_client.temperature = plan_config["temperature"]
            
            # Generate plan
            plan_prompt = self.prompt_handler.get_plan_prompt(test_case)
            current_plan_response = self._call_api(plan_prompt)
            current_plan = current_plan_response if isinstance(current_plan_response, str) else current_plan_response[0]
            
            # Generate code
            code_configs = [{"temperature": self.config.code_temp}]
            plan_code_results = []
            
            for code_gen_idx, code_config in enumerate(code_configs, 1):
                self.code_api_client.temperature = code_config["temperature"]
                
                code_prompt = self.prompt_handler.get_code_prompt(test_case, current_plan)
                temp_code_response = self._call_fix_api(code_prompt)
                temp_code = CodeCleaner.clean_code(temp_code_response, self.config.dataset)
                
                # Execute with repair loop
                temp_code, temp_solver_output, is_valid = self._execute_with_repair(
                    test_case, temp_code, execute_func, mp_lock, current_plan, 
                    plan_config_idx + 1, code_gen_idx
                )
                
                code_result = {
                    "plan_idx": plan_config_idx + 1,
                    "code_idx": code_gen_idx,
                    "code": temp_code,
                    "solver_output": temp_solver_output,
                    "is_valid": is_valid,
                    "code_generation_config": code_config.copy()
                }
                plan_code_results.append(code_result)
            
            plan_result = {
                "plan_idx": plan_config_idx + 1,
                "plan_config": plan_config.copy(),
                "plan": current_plan,
                "code_results": plan_code_results
            }
            all_plan_results.append(plan_result)
        
        return {"all_plan_results": all_plan_results}
    
    def _execute_with_repair(self, test_case: dict, code: str, execute_func: Callable, 
                           mp_lock: Optional[Any], plan: str, plan_idx: int, code_idx: int) -> Tuple[str, str, bool]:
        """Execute code with repair attempts"""
        temp_code = code
        temp_solver_output = None
        is_valid = False
        
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs} for plan={plan_idx}, code={code_idx}")
            
            if mp_lock is not None:
                with mp_lock:
                    is_valid, temp_solver_output = execute_func(temp_code)
            else:
                is_valid, temp_solver_output = execute_func(temp_code)
                
            if not is_valid and iteration < self.config.max_repairs - 1:
                print(f"Code execution failed for plan={plan_idx}, code={code_idx}. Error: {temp_solver_output}")
                fix_prompt = self.prompt_handler.get_fix_syntax_error_prompt(test_case, temp_code, temp_solver_output, plan)
                fix_response = self._call_fix_api(fix_prompt)
                temp_code = CodeCleaner.clean_code(fix_response, self.config.dataset)
            else:
                if is_valid:
                    print(f"Code execution succeeded for plan={plan_idx}, code={code_idx}.")
                break
        
        return temp_code, temp_solver_output, is_valid

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float, unique_id: str="", timing_data: Optional[Dict] = None) -> None:
        """Save the plans, codes and results to the results_folder"""
        plan_folder = os.path.join(self.results_folder, "plan")
        code_folder = os.path.join(self.results_folder, "code")
        os.makedirs(plan_folder, exist_ok=True)
        os.makedirs(code_folder, exist_ok=True)

        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        all_plan_results = reasoning_result.get("all_plan_results", [])
        all_solver_outputs = []
        
        for plan_result in all_plan_results:
            plan_idx = plan_result["plan_idx"]
            plan_config = plan_result["plan_config"]
            plan_temp = plan_config["temperature"]
            
            # Save plan
            plan_filepath = os.path.join(plan_folder, f"{problem_name}-{unique_id}-plan{plan_idx}-temp{plan_temp}.txt")
            with open(plan_filepath, "w") as f:
                f.write(f"Plan Config: {plan_config}\n\n")
                f.write(plan_result["plan"])
            
            # Save codes
            for code_result in plan_result.get("code_results", []):
                code_idx = code_result["code_idx"]
                code_generation_config = code_result.get("code_generation_config", {})
                
                code_filepath = os.path.join(code_folder, f"{problem_name}-{unique_id}-plan{plan_idx}-code{code_idx}.py")
                with open(code_filepath, "w") as f:
                    f.write(f"# Plan Config: {plan_config}\n")
                    f.write(f"# Generation Config: {code_generation_config}\n\n")
                    f.write(code_result["code"])
                
                solver_output = code_result["solver_output"]
                if solver_output is not None:
                    all_solver_outputs.append(solver_output)
            
        results = {
            "problem": test_case,
            "timing": case_time,
            "all_solver_outputs": all_solver_outputs
        }

        summary_filepath = os.path.join(self.summary_folder, f"{problem_name}-{unique_id}.json")
        with open(summary_filepath, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


class DirectReasoner(CodeBasedReasoner):
    """Direct reasoning approach - generates formal code in one step"""

    def _generate_and_execute_code(self, test_case: dict, solver_name: str, execute_func: Callable, mp_lock: Optional[Any] = None) -> dict:
        """Generate multiple code variants with diverse parameters"""
        code_configs = [{"temperature": self.config.temperature} for _ in range(self.config.num_paths)]
        all_code_results = []
        original_temp = self.api_client.temperature
        
        for code_config_idx, code_config in enumerate(code_configs):
            print(f"Generating code {code_config_idx + 1}/{len(code_configs)}...")
            self.api_client.temperature = code_config["temperature"]
            
            # Generate code directly
            direct_prompt = self.prompt_handler.get_direct_prompt(test_case)
            current_code_response = self._call_api(direct_prompt)
            current_code = current_code_response if isinstance(current_code_response, str) else current_code_response[0]
            current_code = CodeCleaner.clean_code(current_code, self.config.dataset)
            
            # Execute with repair loop
            current_code, temp_solver_output, is_valid = self._execute_with_repair(
                test_case, current_code, execute_func, mp_lock, code_config_idx + 1
            )
            
            code_result = {
                "code_idx": code_config_idx + 1,
                "code": current_code,
                "solver_output": temp_solver_output,
                "is_valid": is_valid,
                "generation_config": code_config.copy()
            }
            all_code_results.append(code_result)
        
        self.api_client.temperature = original_temp
        return {"all_code_results": all_code_results}
    
    def _execute_with_repair(self, test_case: dict, code: str, execute_func: Callable, 
                           mp_lock: Optional[Any], code_idx: int) -> Tuple[str, str, bool]:
        """Execute code with repair attempts"""
        temp_code = code
        temp_solver_output = None
        is_valid = False
        
        for iteration in range(self.config.max_repairs):
            print(f"Starting syntax error iteration {iteration + 1}/{self.config.max_repairs} for code {code_idx}")
            
            if mp_lock is not None:
                with mp_lock:
                    is_valid, temp_solver_output = execute_func(temp_code)
            else:
                is_valid, temp_solver_output = execute_func(temp_code)
                
            if not is_valid and iteration < self.config.max_repairs - 1:
                print(f"Code execution failed for code {code_idx}. Error: {temp_solver_output}")
                fix_prompt = self.prompt_handler.get_fix_syntax_error_prompt(test_case, temp_code, temp_solver_output)
                fix_response = self._call_api(fix_prompt)
                temp_code = CodeCleaner.clean_code(fix_response, self.config.dataset)
            else:
                if is_valid:
                    print(f"Code execution succeeded for code {code_idx}.")
                break
        
        return temp_code, temp_solver_output, is_valid

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float, unique_id: str="", timing_data: Optional[Dict] = None) -> None:
        """Save the codes and results to the results_folder"""
        code_folder = os.path.join(self.results_folder, "code")
        os.makedirs(code_folder, exist_ok=True)

        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        all_code_results = reasoning_result.get("all_code_results", [])
        all_solver_outputs = []
        
        for code_result in all_code_results:
            code_idx = code_result["code_idx"]
            code_generation_config = code_result.get("generation_config", {})
            
            code_filepath = os.path.join(code_folder, f"{problem_name}-{unique_id}-code{code_idx}.py")
            with open(code_filepath, "w") as f:
                f.write(f"# Generation Config: {code_generation_config}\n\n")
                f.write(code_result["code"])
            
            solver_output = code_result["solver_output"]
            if solver_output is not None:
                all_solver_outputs.append(solver_output)
            
        results = {
            "problem": test_case,
            "timing": case_time,
            "all_solver_outputs": all_solver_outputs
        }
        
        summary_filepath = os.path.join(self.summary_folder, f"{problem_name}-{unique_id}.json")
        with open(summary_filepath, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    

class CoTReasoner(Reasoner):
    """Chain-of-Thought reasoning approach"""

    def reason(self, test_case: Dict, mp_lock: Optional[Any]=None) -> Dict:
        """Generate reasoning using the CoT prompt"""
        cot_prompt = self.prompt_handler.get_cot_prompt(test_case)
        print("\nGenerating CoT reasoning:")
        reasoning_output = self._call_api(cot_prompt)
        return {"reasoning_output": reasoning_output}

    def _process_results(self, test_case: Dict, reasoning_result: Dict, case_time: float, unique_id: str="", timing_data: Optional[Dict] = None) -> None:
        """Save the reasoning output and extract answers"""
        reasoning_folder = os.path.join(self.results_folder, "reasoning")
        os.makedirs(reasoning_folder, exist_ok=True)

        problem_name = test_case['id_string'] if 'id_string' in test_case else test_case['id']
        
        reasoning_filepath = os.path.join(reasoning_folder, f"{problem_name}-{unique_id}.txt")
        with open(reasoning_filepath, "w") as f:
            reasoning_output = reasoning_result.get("reasoning_output", "")
            if reasoning_output is None:
                reasoning_output = "[ERROR: No reasoning output generated]"
            f.write(reasoning_output)

        # Extract answer from reasoning output
        reasoning_output_for_extraction = reasoning_result.get("reasoning_output", "")
        if reasoning_output_for_extraction is None:
            reasoning_output_for_extraction = ""
        
        # Dataset-specific answer extraction
        if self.config.dataset.lower() == "ar-lsat":
            is_correct, error_type = self.answer_extractor.extract_answer(
                reasoning_output_for_extraction, test_case["label"], test_case["answers"], self.config.reasoning_method)
        elif self.config.dataset.lower() in ["proofwriter", "folio", "prontoqa", "logicaldeduction"]:
            is_correct, error_type = self.answer_extractor.extract_answer(
                reasoning_output_for_extraction, test_case["answer"], self.config.reasoning_method)
        else:
            raise ValueError(f"Dataset {self.config.dataset} not configured for CoTReasoner AnswerExtractor.")
        
        # Handle API failure case
        if reasoning_result.get("reasoning_output") is None:
            is_correct = False
            error_type = "API failure - no output generated"
        
        print(f"\nReasoning {'PASSED' if is_correct else 'FAILED'}. Error type: {error_type}")

        results = {
            "problem": test_case,
            "timing": case_time,
            "reasoning_output": reasoning_result["reasoning_output"],
            "error_type": error_type,
            "success": is_correct
        }
        
        summary_filepath = os.path.join(self.summary_folder, f"{problem_name}-{unique_id}.json")
        with open(summary_filepath, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
