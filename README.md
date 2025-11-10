# Sketch-and-Prune

A neuro-symbolic tool that combines LLMs with symbolic solvers to solve logical reasoning problems using a multi-path-ensemble approach with sketched planning, code generation, self-refinement and path pruning.

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/Partitioned-Neural-Symbolic-Reasoning.git
cd Partitioned-Neural-Symbolic-Reasoning
pip install -r requirements.txt
```

### 2. Run an Experiment
```bash
# Run with GPT-4 (Azure OpenAI)
python main.py config_gpt.yaml
```
Please refer to the `config_gpt.yaml` file for the configuration details. Gemini is not fully supported yet.

## Project Structure

```
├── main.py                     # Main entry point for experiments
├── config.py                   # Configuration management and parsing
├── reasoners.py                # Core reasoning logic (CoT, two-step, one-step).
├── call_api.py                 # API client implementations (GPT-4, Gemini)
├── data_loaders.py             # Dataset loading and sampling utilities
├── answer_extractors.py        # Answer extraction from solver outputs (only CoT is supported)
├── path_level_analysis.py      # Path-level analysis and evaluation
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── config_*.yaml               # Configuration files for different setups:
│   ├── config_gpt.yaml         #   GPT-4 Azure configuration (fully supported)
│
├── prompts-all-3-shot-aligned/  # 3-shot aligned prompt templates
│   ├── AR-LSAT-prompts-CoT/              #   Chain-of-thought reasoning
│   ├── AR-LSAT-prompts-one-step/         #   Direct code generation
│   ├── AR-LSAT-prompts-two-step-partition/ #   Plan + code generation
│   ├── ProofWriter-prompts-CoT/          #   Chain-of-thought reasoning
│   ├── ProofWriter-prompts-one-step/     #   Direct code generation
│   ├── ProofWriter-prompts-two-step-partition/ #   Plan + code generation
│   ├── ProntoQA-prompts-CoT/             #   Chain-of-thought reasoning
│   ├── ProntoQA-prompts-one-step/        #   Direct code generation
│   ├── ProntoQA-prompts-two-step-partition/ #   Plan + code generation
│   ├── LogicalDeduction-prompts-CoT/     #   Chain-of-thought reasoning
│   ├── LogicalDeduction-prompts-one-step/ #   Direct code generation
│   └── LogicalDeduction-prompts-two-step-partition/ #   Plan + code generation
│
├── data/                       # Dataset files
│   ├── AR-LSAT/                #   AR-LSAT test data
│   ├── ProofWriter/            #   ProofWriter dev/test/train data
│   ├── ProntoQA/               #   ProntoQA dev data
│   └── LogicalDeduction/       #   LogicalDeduction dev/train data
│
├── results/                    # Experiment output directory
│
└── [Generated Files]           # Runtime generated files:
    ├── logs/                   #   Execution logs
    ├── __pycache__/            #   Python cache files
```

Note: 
1. We use a 'clean_code' function in 'reasoners.py' to clean the code, which have '```python```' or '``` ```' fences or missing 'import' statements. This is not counted as syntax errors.
2. We only enable the online analysis for CoTReasoner, not for One-Step Reasoner and Two-Step Reasoner. All the analysis for One-Step Reasoner and Two-Step Reasoner are done offline. Please refer to the 'path_level_analysis.py' file for the offline analysis.

### Prompt Structure Details

Each reasoning method uses different prompt files:

#### **Two-Step Reasoning** (`two-step-partition/`)
- `plan.txt` - Plan generation prompts
- `code.txt` - Code generation prompts  
- `fix_syntax_errors.txt` - Syntax error fixing prompts

#### **One-Step Reasoning** (`one-step/`)
- `prompt.txt` - Direct code generation prompts
- `fix_syntax_errors.txt` - Syntax error fixing prompts

#### **Chain-of-Thought Reasoning** (`CoT/`)
- `prompt.txt` - Chain-of-thought reasoning prompts

## Results and Analysis

### Experiment Output Structure
Each experiment creates a timestamped results folder:
```
results/results_{timestamp}/
└── {reasoning_method}-{dataset}-plan-with-{plan_model}-code-with-{code_model}-{shots}_shot_CoT-{uuid}/
    ├── config.yaml                     # Configuration file for the experiment
    ├── total_execution_time.txt         # Total runtime for the entire benchmark
    ├── summary.txt                      # Concatenated results from summary/ folders
    ├── summary/                         # Symbolic solver outputs for all paths per sample (JSON format)
    │   └── *.json                      # Total count = #samples × #paths
    ├── plan/                           # Path-level sketched plans by LLMs if two-step reasoning is used
    │   └── *.txt                       # Total count = #samples × #paths
    ├── code/                           # Path-level program codes by LLMs  
    │   └── *.py                        # Total count = #samples × #paths
    ├── prompts/                        # Complete copy of prompts used
    │   ├── plan.txt                    # Plan generation prompts if two-step reasoning is used
    │   ├── code.txt                    # Code generation prompts
    │   ├── fix_syntax_errors.txt       # Syntax error fixing prompts
    │   └── prompt_metadata.json        # Timestamp metadata (not used in experiment)
    ├── log/                            # Execution timestamps
    │   └── *.log                       # Start timestamp for each sample (#samples total)
    └── temp_cache_dir/                 # Temporary Pyke cache (if using Pyke solver)
```

### Path-Level Analysis Script

The repository includes a comprehensive analysis script for processing experiment results:

#### **Usage**
```bash
# Basic path-level analysis
python path_level_analysis.py <results_directory> --expected-paths 30

# Include CoT results and add CoT correctness column
python path_level_analysis.py <results_directory> --expected-paths 30 --cot-summary path/to/cot_summary.txt

# Force reprocessing of individual result files
python path_level_analysis.py <results_directory> --expected-paths 30 --force-merge
```

#### **Features**
- **Path-level Analysis**: Creates detailed dataframe with individual path information
- **Automatic Result Merging**: Processes individual JSON files from `summary/` folder if `summary.txt` doesn't exist
- **Correctness Evaluation**: Parses solver outputs and compares with ground truth labels
- **Pruning Analysis**: Tracks paths pruned by existence and uniqueness constraints
- **Multiple Output Formats**: Generates both CSV and XLSX files
- **CoT Integration**: Optional, adds CoT correctness column

#### **Output Metrics**
- **Path-level Statistics**: Individual path correctness and syntax error rates
- **Pruning Statistics**: Tracks how many paths are filtered out
- **One-path Accuracy**: Performance using the first generated path only
- **Sample-level Analysis**: Aggregated results per problem sample

#### **Command Options**
- `--expected-paths N`: Number of paths per sample (default: 5, commonly 30 for two-step)
- `--output-format`: Choose 'csv', 'xlsx', or 'both' (default: both)
- `--force-merge`: Reprocess individual result files even if summary.txt exists
- `--cot-summary`: Path to CoT summary file for comparison analysis
- `--cot-backup`: Use CoT results as backup for syntax error cases

#### **Generated Files**
- `{experiment_name}_path_level.csv` - Detailed path-level data
- `{experiment_name}_path_level.xlsx` - Excel format with formatting
- Console output with comprehensive statistics

---

### Majority Voting Simulation Script

After generating path-level analysis results, you can evaluate the effectiveness of majority voting across different numbers of paths (k=1 to 20) with and without pruning.

#### **Usage**

```bash
# Simulate without pruning
python analysis_pruning_and_ensemble_simulation.py \
  results/experiment/path_level_analysis.csv

# Simulate with pruning
python analysis_pruning_and_ensemble_simulation.py \
  results/experiment/path_level_analysis.csv \
  --with-pruning

# Simulate both (recommended)
python analysis_pruning_and_ensemble_simulation.py \
  results/experiment/path_level_analysis.csv \
  --both

# Customize simulation parameters
python analysis_pruning_and_ensemble_simulation.py \
  results/experiment/path_level_analysis.csv \
  --both \
  --max-paths 20 \
  --num-simulations 100 \
  --output-csv results/experiment/custom_simulation.csv
```

#### **Input**

The script requires a CSV file generated by `path_level_analysis.py` with the following columns:
- `sample_id`: Unique identifier for each problem
- `path_index`: Path number (0-indexed)
- `parsed_output`: Raw solver output (e.g., `[1]`, `[2, 3]`, or `syntax error`)
- `existence_uniqueness_pruning_result`: Output after applying pruning filters
- `true_label`: Ground truth answer
- `dataset`: Dataset name (AR-LSAT, ProofWriter, ProntoQA, LogicalDeduction, FOLIO)

#### **Output**

The script generates one or two CSV files depending on the mode:

**Without Pruning** (`*_simulation_no_pruning.csv`):
- Uses `parsed_output` for majority voting
- Includes all paths regardless of validity

**With Pruning** (`*_simulation_existence_uniqueness_pruning.csv`):
- Uses `existence_uniqueness_pruning_result` for majority voting
- Filters paths based on:
  - **Existence**: Output must be non-empty (not None, not syntax error)
  - **Uniqueness**: Output must contain exactly one answer

Each output CSV contains:
```csv
k_paths,simulation,accuracy,total_samples,correct_samples,cot_backup_used
1,0,0.3456,100,35,0
1,1,0.3521,100,36,0
...
20,99,0.7234,100,72,0
```

- `k_paths`: Number of paths used (1 to max_paths)
- `simulation`: Simulation iteration number (0 to num_simulations-1)
- `accuracy`: Accuracy for this configuration
- `total_samples`: Total number of samples evaluated
- `correct_samples`: Number of correctly solved samples
- `cot_backup_used`: Reserved for future use (always 0)

#### **Command Options**

- `input_csv`: Path to CSV file from `path_level_analysis.py` (required, positional)
- `--with-pruning`: Calculate accuracy with existence+uniqueness pruning
- `--both`: Calculate both with and without pruning (generates two output files)
- `--max-paths`: Maximum number of paths to simulate (default: 20)
- `--num-simulations`: Number of simulation iterations per k_paths (default: 10)
- `--output-csv`: Custom output file path (default: auto-generated from input filename)

#### **How It Works**

For each value of k from 1 to max_paths:
1. Run multiple simulations (default: 10 iterations)
2. In each simulation:
   - For each problem sample, randomly sample k paths
   - Perform majority voting on the sampled paths
   - Compare voting result with ground truth label
   - Calculate accuracy across all samples
3. Use deterministic random seeds for reproducibility (based on k, simulation number, and sample_id)

**Majority Voting Logic**:
- Extracts answers from each path's output
- Counts frequency of each answer
- Returns the most common answer (ties broken deterministically)
- For multi-element outputs, checks if true label is present in the output

#### **Reproducibility**

The script uses deterministic random sampling with seeds calculated as:
```
seed = (simulation × 1000000 + k_paths × 1000 + sample_id_hash) % 2^31
```


## Supported Datasets

| Dataset | Description | Source |
|---------|-------------|--------|
| **AR-LSAT** | Analytical Reasoning from LSAT | [AR-LSAT Hugging Face](https://huggingface.co/datasets/tasksource/lsat-ar) |
| **ProofWriter** | Deductive logical reasoning | [ProofWriter Hugging Face](https://huggingface.co/datasets/tasksource/proofwriter) |
| **ProntoQA** | Synthetic deductive reasoning | [ProntoQA Hugging Face](https://huggingface.co/datasets/renma/ProntoQA) |
| **LogicalDeduction** | BigBench logical reasoning | [BigBenchHard Hugging Face](https://huggingface.co/datasets/maveriq/bigbenchhard) |

## License

[Include your license information here]
