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
├── reasoners.py                # Core reasoning logic (CoT, two-step, one-step)
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

## Supported Datasets

| Dataset | Description | Source |
|---------|-------------|--------|
| **AR-LSAT** | Analytical Reasoning from LSAT | [AR-LSAT Hugging Face](https://huggingface.co/datasets/tasksource/lsat-ar) |
| **ProofWriter** | Deductive logical reasoning | [ProofWriter Hugging Face](https://huggingface.co/datasets/tasksource/proofwriter) |
| **ProntoQA** | Synthetic deductive reasoning | [ProntoQA Hugging Face](https://huggingface.co/datasets/renma/ProntoQA) |
| **LogicalDeduction** | BigBench logical reasoning | [BigBenchHard Hugging Face](https://huggingface.co/datasets/maveriq/bigbenchhard) |

## License

[Include your license information here]
