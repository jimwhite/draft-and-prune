# Reasoner Classes Function Usage Documentation

This document provides a guide to understanding the function usage in each reasoner class in 'reasoners.py'. The codebase contains several reasoner classes with many redundant functions that are repeated across different classes.

## Table of Contents
1. [Class Overview](#class-overview)
2. [Base Reasoner Class](#base-reasoner-class)
3. [TwoStepReasoner Class](#twostepReasoner-class)
4. [DirectReasoner Class](#directreasoner-class)
5. [CoTReasoner Class](#cotreasoner-class)
6. [Redundant Functions Analysis](#redundant-functions-analysis)
7. [Function Usage Workflows](#function-usage-workflows)

## Class Overview

1. **Reasoner (Base Class)** - Abstract base class with common functionality
2. **TwoStepReasoner** - Implements two-step reasoning (plan generation → code generation)
3. **DirectReasoner** - Implements direct code generation in one step
4. **CoTReasoner** - Implements Chain-of-Thought reasoning

## Base Reasoner Class
### Core Functions

#### 1. Initialization Functions
- **`__init__(config, data_loader, answer_extractor)`**
  - **Purpose**: Initialize the reasoner with configuration, data loader, and answer extractor
  - **Step-by-step usage**:
    1. Store configuration, data loader, and answer extractor
    2. Create results folder structure
    3. Initialize API clients based on reasoning method
    4. Set up temporary cache directory for PyKe

- **`initialize_api_client(model_name, api_config)`**
  - **Purpose**: Initialize API client for specific models (GPT/Gemini)
  - **Step-by-step usage**:
    1. Determine provider based on model name
    2. Set up client parameters
    3. Create and return API client instance

#### 2. File Management Functions
- **`create_results_folder()`**
  - **Purpose**: Create timestamped results folder
  - **Step-by-step usage**:
    1. Generate folder name with timestamp and UUID
    2. Create directory structure
    3. Return folder path

- **`save_prompts_folder()`**
  - **Purpose**: Copy prompts folder to results directory
  - **Step-by-step usage**:
    1. Check if prompt path exists
    2. Copy entire prompts folder to results
    3. Create metadata file with prompt information

#### 3. API Communication Functions
- **`_call_api(prompt)`**
  - **Purpose**: Call the main API client (used in plan generation of TwoStepReasoner, code generation of DirectReasoner, cot of CoTReasoner)
  - **Usage**: Direct wrapper for `self.api_client.call(prompt)`

- **`_call_fix_api(prompt)`**
  - **Purpose**: Call the fix/code API client (used in code generation and fixing syntax errors of TwoStepReasoner)
  - **Usage**: Direct wrapper for `self.code_api_client.call(prompt)`

#### 4. Code Processing Functions
- **`clean_code(code_text)`**
  - **Purpose**: Clean and format code output from models
  - **Step-by-step usage**:
    1. Remove markdown fences (```python, ```)
    2. Add required imports based on dataset:
       - AR-LSAT: `from z3 import *`
       - LogicalDeduction: `from constraint import *`
    3. Return cleaned code

#### 5. Code Execution Functions
- **`execute_z3_code(z3_code)`** *(Lines 386-427)*
  - **Purpose**: Execute Z3 SMT solver code
  - **Step-by-step usage**:
    1. Write code to temporary file
    2. Execute with subprocess (30s timeout)
    3. Check return code and output
    4. Return (success_bool, output_string)

- **`execute_pyke_code(pyke_code)`** *(Lines 429-484)*
  - **Purpose**: Execute PyKE knowledge engine code
  - **Step-by-step usage**:
    1. Extract facts, rules, and query from code
    2. Write facts and rules to temporary files
    3. Initialize PyKE engine
    4. Execute query and collect results
    5. Return (success_bool, result_string)

- **`execute_csp_code(csp_code)`** *(Lines 558-600)*
  - **Purpose**: Execute Constraint Satisfaction Problem code
  - **Step-by-step usage**:
    1. Write code to temporary file
    2. Execute with subprocess (20s timeout)
    3. Check return code and output
    4. Return (success_bool, output_string)

#### 6. Test Execution Functions
- **`run_all_tests()`**
  - **Purpose**: Run reasoning on all test cases sequentially
  - **Step-by-step usage**:
    1. Iterate through data loader batches
    2. Call `reason()` method for each test case
    3. Process results with `_process_results()`
    4. Add delay between test cases

- **`run_all_tests_parallel(num_processes)`**
  - **Purpose**: Run reasoning on all test cases in parallel
  - **Step-by-step usage**:
    1. Create multiprocessing lock
    2. Prepare task arguments for each test case
    3. Launch processes with `_parallel_worker`
    4. Monitor and join processes

#### 7. Abstract Methods
- **`reason(test_case)`** - Must be implemented by subclasses
- **`_process_results(test_case, reasoning_result, case_time, unique_id, timing_data)`** - Result processing

## TwoStepReasoner Class
### All Functions

#### 1. Prompt Generation Functions
- **`get_plan_prompt(test_case, feedback=None)`** *(Lines 612-651)*
  - **Purpose**: Generate prompt for plan generation step
  - **Step-by-step usage**:
    1. Load plan.txt template from prompt path
    2. Replace placeholders based on dataset:
       - AR-LSAT: {context}, {question}, {answers}
       - ProofWriter/FOLIO/ProntoQA: {context}, {question}
       - LogicalDeduction: {context}, {question}, {options}
    3. Return formatted prompt

- **`get_code_prompt(test_case, plan, feedback=None)`** *(Lines 653-695)*
  - **Purpose**: Generate prompt for code generation step
  - **Step-by-step usage**:
    1. Load code.txt template from prompt path
    2. Replace placeholders including {plan} from previous step
    3. Format based on dataset type
    4. Return formatted prompt

- **`get_fix_syntax_error_prompt(test_case, plan, code, syntax_error)`** *(Lines 697-722)*
  - **Purpose**: Generate prompt for fixing syntax errors
  - **Step-by-step usage**:
    1. Load fix_syntax_errors.txt template
    2. Format with code and syntax_error parameters
    3. Return fix prompt

#### 2. Core Reasoning Function
- **`reason_code_diversity(test_case, solver_name, execute_func, mp_lock)`** *(Lines 724-847)*
  - **Purpose**: Generate multiple plan-code combinations with diversity
  - **Step-by-step usage**:
    1. **Plan Generation Loop**:
       - Create plan configurations (temperature variations)
       - For each configuration:
         - Set API client temperature
         - Generate plan using `get_plan_prompt()`
         - Call API to get plan response
    2. **Code Generation Loop**:
       - For each plan, create code configurations
       - Generate code using `get_code_prompt()`
       - Clean code with `clean_code()`
    3. **Code Execution and Repair Loop**:
       - Execute code with provided execute_func
       - If execution fails and iterations remain:
         - Generate fix using `get_fix_syntax_error_prompt()`
         - Clean and retry execution
    4. **Result Collection**:
       - Store plan and code results with metadata
       - Return structured results dictionary

- **`reason(test_case, mp_lock=None)`** *(Lines 849-862)*
  - **Purpose**: Main reasoning entry point
  - **Step-by-step usage**:
    1. Determine solver and execution function based on dataset:
       - AR-LSAT → Z3 solver
       - ProofWriter/ProntoQA → PyKE solver  
       - FOLIO → Prover9 solver
       - LogicalDeduction → Python constraint solver
    2. Call `reason_code_diversity()` with appropriate parameters

#### 3. Result Processing Functions
- **`_process_results_diversity(test_case, reasoning_result, case_time, unique_id, timing_data)`** *(Lines 864-942)*
  - **Purpose**: Save plans, codes, and results to files
  - **Step-by-step usage**:
    1. Create plan and code folders
    2. Process all plan results:
       - Save each plan with configuration metadata
       - Process associated code results
       - Save each code with generation metadata
    3. Collect all solver outputs
    4. Create summary JSON with problem, timing, and outputs

## DirectReasoner Class
### All Functions

#### 1. Prompt Generation Functions
- **`get_direct_prompt(test_case, feedback=None)`** *(Lines 957-1006)*
  - **Purpose**: Generate prompt for direct code generation
  - **Step-by-step usage**:
    1. Load prompt.txt template from prompt path
    2. Replace placeholders based on dataset (same logic as TwoStepReasoner)
    3. Return formatted prompt

- **`get_fix_syntax_error_prompt(test_case, code, syntax_error)`** *(Lines 1008-1033)*
  - **Purpose**: Generate prompt for fixing syntax errors (similar to TwoStepReasoner)
  - **Step-by-step usage**:
    1. Load fix_syntax_errors.txt template
    2. Replace {code} and {syntax_error} placeholders
    3. Return fix prompt

#### 2. Core Reasoning Function
- **`reason_code_diversity(test_case, solver_name, execute_func, mp_lock)`** *(Lines 1035-1121)*
  - **Purpose**: Generate multiple code variants directly (no planning step)
  - **Step-by-step usage**:
    1. **Code Generation Loop**:
       - Create code configurations (temperature variations)
       - For each configuration:
         - Set API client temperature
         - Generate code using `get_direct_prompt()`
         - Clean code with `clean_code()`
    2. **Code Execution and Repair Loop** (identical to TwoStepReasoner):
       - Execute code with provided execute_func
       - If execution fails and iterations remain:
         - Generate fix using `get_fix_syntax_error_prompt()`
         - Clean and retry execution
    3. **Result Collection**:
       - Store code results with metadata
       - Return structured results dictionary

- **`reason(test_case, mp_lock=None)`** *(Lines 1123-1136)*
  - **Purpose**: Main reasoning entry point (identical dataset mapping as TwoStepReasoner)

#### 3. Result Processing Functions
- **`_process_results_diversity(test_case, reasoning_result, case_time, unique_id, timing_data)`** *(Lines 1138-1186)*
  - **Purpose**: Save codes and results to files (similar to TwoStepReasoner but no plans)
  - **Step-by-step usage**:
    1. Create code folder
    2. Process all code results:
       - Save each code with generation metadata
       - Collect solver outputs
    3. Create summary JSON with problem, timing, and outputs

## CoTReasoner Class
### All Functions

#### 1. Prompt Generation Function
- **`get_cot_prompt(test_case)`** *(Lines 1200-1244)*
  - **Purpose**: Generate Chain-of-Thought reasoning prompt
  - **Step-by-step usage**:
    1. Load prompt.txt template from prompt path
    2. Replace placeholders based on dataset:
       - AR-LSAT: {context}, {question}, {answers}
       - ProofWriter/FOLIO/ProntoQA: {context}, {question}, {options}
       - LogicalDeduction: {context}, {question}, {options}
    3. Return formatted prompt

#### 2. Core Reasoning Function
- **`reason(test_case, mp_lock=None)`** *(Lines 1246-1264)*
  - **Purpose**: Generate reasoning using CoT prompt
  - **Step-by-step usage**:
    1. Generate CoT prompt using `get_cot_prompt()`
    2. Call API to get reasoning output
    3. Return dictionary with reasoning_output

#### 3. Result Processing Function
- **`_process_results(test_case, reasoning_result, case_time, unique_id, timing_data)`** *(Lines 1266-1318)*
  - **Purpose**: Save reasoning output and extract answers
  - **Step-by-step usage**:
    1. Create reasoning folder
    2. Save reasoning output to text file
    3. Extract answer using answer_extractor based on dataset
    4. Create summary JSON with problem, timing, reasoning output, and success status

## Redundant Functions Analysis

### Highly Redundant Functions

1. **Prompt Generation Logic** - Nearly identical across classes:
   - Dataset-specific placeholder replacement
   - File loading from prompt path
   - String replacement instead of .format()

2. **Dataset Mapping Logic** - Repeated in `reason()`:
   - Same dataset → solver mapping
   - Same execution function selection

3. **Result Processing Patterns** - Similar structure:
   - Folder creation
   - File saving with metadata
   - JSON summary generation

### Partially Redundant Functions

1. **Fix Syntax Error Prompts** - Similar but slightly different:
   - TwoStepReasoner includes plan parameter
   - DirectReasoner excludes plan parameter
   - Same core logic otherwise

2. **Result Processing** - Similar patterns but different data:
   - All save files and create summaries
   - Different folder structures (plan vs no plan)
   - Different metadata fields

## Function Usage Workflows

### TwoStepReasoner Workflow
```
1. reason(test_case) 
   ↓
2. reason_code_diversity(test_case, solver, execute_func)
   ↓
3. For each plan configuration:
   - get_plan_prompt(test_case) → _call_api() → plan
   ↓
4. For each code configuration:
   - get_code_prompt(test_case, plan) → _call_fix_api() → code
   - clean_code(code) → cleaned_code
   ↓
5. For each repair iteration:
   - execute_func(cleaned_code) → (success, output)
   - If failed: get_fix_syntax_error_prompt() → _call_fix_api() → fixed_code
   ↓
6. _process_results_diversity() → save plans, codes, summaries
```

### DirectReasoner Workflow
```
1. reason(test_case)
   ↓
2. reason_code_diversity(test_case, solver, execute_func)
   ↓
3. For each code configuration:
   - get_direct_prompt(test_case) → _call_api() → code
   - clean_code(code) → cleaned_code
   ↓
4. For each repair iteration:
   - execute_func(cleaned_code) → (success, output)
   - If failed: get_fix_syntax_error_prompt() → _call_api() → fixed_code
   ↓
5. _process_results_diversity() → save codes, summaries
```

### CoTReasoner Workflow
```
1. reason(test_case)
   ↓
2. get_cot_prompt(test_case) → _call_api() → reasoning_output
   ↓
3. _process_results() → save reasoning, extract answer, create summary
```

