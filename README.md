# Partitioned Neural-Symbolic Reasoning

A system that combines neural language models with symbolic reasoning to solve logical reasoning problems.

## Quick Start

1. Clone and setup:
```bash
git clone https://github.com/yourusername/Partitioned-Neural-Symbolic-Reasoning.git
cd Partitioned-Neural-Symbolic-Reasoning
pip install -r requirements.txt
```

Required dependencies:
- python >= 3.8
- google-generativeai
- openai (optional, for GPT models)
- z3-solver

## Usage

The repo now uses YAML configuration files for easy setup and reproducible experiments.

### Azure OpenAI Setup
1. **Update the Azure configuration** (`config_azure_ar_lsat_test.yaml`):
   - Set `azure_endpoint` to your Azure OpenAI endpoint
   - Set `azure_deployment` to your deployment name
   - Optionally set `azure_managed_identity_client_id` for managed identity
   - Leave `api_key` empty (Azure uses Entra ID authentication)

2. **Run with Azure OpenAI:**
   ```bash
   python main.py config_azure_ar_lsat_test.yaml
   ```

## Features

### Reasoning Methods
- `"CoT"`: Chain of Thought
- `"one-step"`: Single-step reasoning
- `"two-step"`: Two-step reasoning (plan then code)

### Models
- `"gemini-2.5-flash-preview-04-17"` (default)
- `"gemini-1.5-pro"`
- `"gpt-4"`

### Analysis
The `analysis.py` script generates detailed reports of verification results:

```bash
python analysis.py <results_file>
```

Reports include:
- Success rates and statistics
- Error analysis
- Timing information
- Problem-by-problem breakdown
- Failed problem details

#### CoT Backup Analysis
The `analysis_include_cot_as_backup.py` script provides enhanced analysis by using Chain of Thought (CoT) results as a backup for specific failure cases:

```bash
python analysis_include_cot_as_backup.py <main_results_file> <cot_results_file>
```

## Project Structure

- `main.py`: Application entry point
- `config.py`: Configuration management
- `reasoners.py`: Reasoning approaches
- `data_loaders.py`: Test data processing
- `answer_extractors.py`: Answer extraction
- `call_api.py`: LLM API interactions
- `analysis.py`: Results analysis
- `analysis_include_cot_as_backup.py`: Enhanced analysis with CoT backup functionality

## Supported Datasets

- AR-LSAT: Analytical Reasoning tasks from LSAT
  - Source: [AR-LSAT GitHub](https://github.com/zhongwanjun/AR-LSAT)
  - Path: `AR-LSAT/blob/main/complete_lsat_data/test_ar.json`

## To Do
- [ ] Implement checker/verifier

## License

[Include your license information here]