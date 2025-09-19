# Partitioned Neural-Symbolic Reasoning

A system that combines neural language models with symbolic reasoning to solve logical reasoning problems using a multi-step approach with plan generation and code synthesis.

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/Partitioned-Neural-Symbolic-Reasoning.git
cd Partitioned-Neural-Symbolic-Reasoning
pip install -r requirements.txt
```

### 2. Required Dependencies
- python >= 3.8
- google-generativeai (for Gemini models)
- openai (for GPT models)
- z3-solver (for logical reasoning)
- pyyaml (for configuration files)
- pandas (for analysis)

### 3. Run an Experiment
```bash
# Run with Gemini (multi-key batch distribution)
python main.py config_gemini_multi_key.yaml

# Run with GPT-4 (Azure OpenAI)
python main.py config_gpt4_2-CoT-align.yaml
```

## 📋 Configuration System

The system uses YAML configuration files with enhanced model field naming:

### 🆕 New Model Field Names (Recommended)
- `plan_model`: Model used for plan generation
- `code_model`: Model used for code generation and fixing

### 📁 Sample Configuration
```yaml
# Enhanced model configuration
dataset: "AR-LSAT"
test_file: "./data/AR-LSAT/blob/main/complete_lsat_data/test_ar.json"
reasoning_method: "two-step"

# New model field names (clear semantics)
plan_model: "gemini-2.5-flash"  # Model for plan generation
code_model: "gemini-2.5-flash"  # Model for code generation

# Multiple API keys for batch-based distribution
gemini_api_keys:
  - "your-api-key-1"
  - "your-api-key-2"
  - "your-api-key-3"

# Experiment settings
temperature: 0
max_repairs: 3
desired_indices: [0, 1, 2, 3, 4]  # Test specific samples
prompt_path: "./prompts/AR-LSAT-prompts-two-step-partition/"
shots: "three"
```

### 🔄 Backward Compatibility
Legacy field names (`model`, `fix_model`) are still supported for existing configurations.

## 🏗️ System Architecture

### Reasoning Methods
- **`two-step`**: Plan generation → Code synthesis → Execution
- **`one-step`**: Direct code generation → Execution  
- **`cot`**: Chain-of-thought reasoning

### Supported Models
- **Gemini**: `gemini-2.5-flash`, `gemini-1.5-pro`
- **GPT**: `gpt-4`, `gpt-4o` (via Azure OpenAI)

### API Key Management
- **Single Key**: Traditional single API key usage
- **🆕 Multi-Key Batch Distribution**: Distribute samples across multiple API keys to avoid rate limits

## 📊 Results and Analysis

### Experiment Output Structure
Each experiment creates a timestamped results folder:
```
results/results_2025-09-19/
└── two-step-AR-LSAT-plan-with-gemini-2.5-flash-code-with-gemini-2.5-flash-three_shot_CoT-{uuid}/
    ├── config.yaml              # 🆕 Enhanced config with both old/new field names
    ├── prompts/                  # 🆕 Complete copy of prompts folder
    │   ├── plan.txt
    │   ├── code.txt
    │   ├── fix_semantic_errors.txt
    │   ├── fix_syntax_errors.txt
    │   └── prompt_metadata.json  # 🆕 Metadata about prompts
    ├── summary/                  # Individual test results (JSON)
    ├── log/                      # Execution logs
    ├── code/                     # Generated code files
    ├── plan/                     # Generated plan files
    ├── summary.txt               # Merged results
    ├── ablation_study_results.csv # Comprehensive analysis
    └── detailed_ablation_results.json
```

### 🆕 Enhanced Saving Features
- **Configuration Preservation**: Saves both new and legacy model field names
- **Prompt Archiving**: Complete copy of prompts folder for reproducibility
- **Metadata Tracking**: Timestamps and experiment details

## 📈 Analysis Workflow

### Step 1: Merge Individual Results
```bash
python analysis_simple.py /path/to/experiment/summary/
```
**Purpose**: Merges individual JSON result files into `summary.txt`

**Features**:
- Handles simplified data format (`timing`, `all_solver_outputs`)
- Calculates basic statistics (total samples, average time)
- Error-resistant JSON loading

### Step 2: Comprehensive Ablation Analysis  
```bash
python custom_ablation_analysis.py /path/to/experiment/folder/
```
**Purpose**: Creates detailed CSV analysis with multiple evaluation methods

**Analysis Methods**:
1. **Method 1**: No pruning + majority vote (uses all solver outputs)
2. **Method 2**: With pruning + first valid output (length=1, value 0-4)

**Output Metrics**:
- Overall accuracy (sample-level)
- Accuracy by path (path-level on syntactically correct paths)
- Syntax error rates and counts
- Tied voting analysis
- Path statistics (before/after pruning)
- Auto-formalization failure rates

**Generated Files**:
- `ablation_study_results.csv`: Comprehensive comparison table
- `detailed_ablation_results.json`: Raw analysis data

### Analysis Parameters Explained

| Parameter | Description |
|-----------|-------------|
| `#shots in ICL` | Number of in-context learning examples |
| `sketch` | Whether planning is used ("yes" for two-step, "no" for one-step/CoT) |
| `K (#paths per sample)` | Number of generated reasoning paths per sample |
| `plan_model` / `code_model` | Models used for plan and code generation |
| `syntax error rate` | Ratio of paths with syntax errors |
| `tied voting rate` | Samples with multiple answers having same vote count |
| `overall accuracy` | Correct samples / total samples |
| `accuracy by path` | Correct paths / syntactically correct paths |

## 🔧 Advanced Features

### Multi-Key Batch Distribution
Automatically distributes samples across multiple API keys:
```python
# Sample 0, 5, 10, ... → API Key #1
# Sample 1, 6, 11, ... → API Key #2  
# Sample 2, 7, 12, ... → API Key #3
```

### Parallel Processing
- Configurable parallel workers (default: 5 processes)
- Per-sample API key assignment for consistent usage
- Real-time logging with individual log files

### Error Handling & Recovery
- Automatic syntax error detection and fixing
- Multiple repair attempts (`max_repairs: 3`)
- Comprehensive error logging and analysis

## 📁 Project Structure

```
├── main.py                     # 🎯 Main entry point with enhanced saving
├── config.py                   # 🆕 Enhanced configuration with new model fields  
├── reasoners.py                # 🆕 Multi-key support + prompts archiving
├── call_api.py                 # 🆕 Multi-key rotation for Gemini
├── data_loaders.py             # Dataset loading and sampling
├── answer_extractors.py        # Answer extraction from solver outputs
├── analysis_simple.py          # 🆕 Simple result merging script
├── custom_ablation_analysis.py # 🆕 Comprehensive analysis script
├── config_gemini_multi_key.yaml # 🆕 Multi-key Gemini configuration
├── config_gpt4_2-CoT-align.yaml # GPT-4 Azure configuration
└── prompts/                    # Prompt templates by dataset/method
```

## 🗂️ Supported Datasets

| Dataset | Description | Source |
|---------|-------------|--------|
| **AR-LSAT** | Analytical Reasoning from LSAT | [AR-LSAT GitHub](https://github.com/zhongwanjun/AR-LSAT) |
| **ProofWriter** | Deductive logical reasoning | [Logic-LLM GitHub](https://github.com/teacherpeterpan/Logic-LLM) |
| **FOLIO** | Expert-written logical reasoning | [Logic-LLM GitHub](https://github.com/teacherpeterpan/Logic-LLM) |
| **ProntoQA** | Synthetic deductive reasoning | [Logic-LLM GitHub](https://github.com/teacherpeterpan/Logic-LLM) |
| **LogicalDeduction** | BigBench logical reasoning | [Logic-LLM GitHub](https://github.com/teacherpeterpan/Logic-LLM) |

## 🔄 Migration Guide

### From Legacy to New Model Fields
**Old Configuration**:
```yaml
model: "gemini-2.5-flash"      # Used for plan generation  
fix_model: "gemini-2.5-flash"  # Used for code generation
```

**New Configuration** (Recommended):
```yaml
plan_model: "gemini-2.5-flash"  # Clear: plan generation
code_model: "gemini-2.5-flash"  # Clear: code generation
```

**Result**: Both configurations work! The system maintains full backward compatibility.

## 🚀 Example Workflow

### 1. Run Experiment
```bash
python main.py config_gemini_multi_key.yaml
```

### 2. Analyze Results  
```bash
# Step 1: Merge individual results
python analysis_simple.py ./results/results_2025-09-19/your-experiment-folder/summary/

# Step 2: Generate comprehensive analysis
python custom_ablation_analysis.py ./results/results_2025-09-19/your-experiment-folder/
```

### 3. Review Outputs
- Check `ablation_study_results.csv` for comparison table
- Review `detailed_ablation_results.json` for raw data
- Examine `prompts/` folder for exact prompts used

## 🛠️ Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure valid API keys in configuration
2. **Rate Limits**: Use multi-key configuration for high-volume experiments
3. **Missing Prompts**: Verify `prompt_path` exists in your configuration
4. **Analysis Errors**: Run `analysis_simple.py` before `custom_ablation_analysis.py`

### Debug Mode
Add `import pdb; pdb.set_trace()` in `main.py` for step-by-step debugging.

## 📜 License

[Include your license information here]

---

## 🆕 Recent Updates

- ✅ **Enhanced Model Configuration**: Clear `plan_model` and `code_model` field names
- ✅ **Prompts Archiving**: Automatic copying of prompts folder for reproducibility  
- ✅ **Multi-Key Support**: Batch-based API key distribution for Gemini
- ✅ **Simplified Analysis**: Streamlined two-step analysis workflow
- ✅ **Backward Compatibility**: Legacy configurations still supported
- ✅ **Enhanced Results Structure**: Comprehensive experiment documentation