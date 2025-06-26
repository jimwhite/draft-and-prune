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

The system now uses YAML configuration files for easy setup and reproducible experiments.

### Quick Start

1. **Copy the sample configuration:**
   ```bash
   cp config_sample.yaml my_config.yaml
   ```

2. **Edit the configuration file** (`my_config.yaml`) with your settings:
   - Add your API key
   - Set the path to your test file
   - Adjust other parameters as needed

3. **Run the system:**
   ```bash
   python main.py my_config.yaml
   ```

### Azure OpenAI Setup

1. **Copy the Azure sample configuration:**
   ```bash
   cp config_azure_sample.yaml my_azure_config.yaml
   ```

2. **Update the Azure configuration** (`my_azure_config.yaml`):
   - Set `azure_endpoint` to your Azure OpenAI endpoint
   - Set `azure_deployment` to your deployment name
   - Optionally set `azure_managed_identity_client_id` for managed identity
   - Leave `api_key` empty (Azure uses Entra ID authentication)

3. **Set up authentication** (choose one):
   - **Environment variables:**
     ```bash
     export ENDPOINT_URL="https://your-resource-name.openai.azure.com/"
     export DEPLOYMENT_NAME="gpt-4o"
     export MANAGED_IDENTITY_CLIENT_ID="your-client-id"  # Optional
     ```
   - **Azure CLI login:**
     ```bash
     az login
     ```

4. **Test the integration:**
   ```bash
   python test_azure_integration.py
   ```

5. **Run with Azure OpenAI:**
   ```bash
   python main.py my_azure_config.yaml
   ```

## API Keys

### Google AI (Gemini)
- Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Models: `gemini-2.5-flash-preview-04-17`, `gemini-1.5-pro`

### OpenAI (GPT)
- Get key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Models: `gpt-4-0613`, `gpt-3.5-turbo`

### Azure OpenAI
- Use Azure managed identity or environment variables for authentication
- Models: `gpt-4o`, `gpt-4`, `gpt-35-turbo`
- Requires Azure OpenAI service setup with Entra ID authentication
- Configuration via `config_azure_sample.yaml`

## Features

### Reasoning Methods
- `"CoT"`: Chain of Thought
- `"one-step"`: Single-step reasoning
- `"two-step"`: Two-step reasoning (plan then code)
- `"three-step"`: Three-step reasoning

### Models
- `"gemini-2.5-flash-preview-04-17"` (default)
- `"gemini-1.5-pro"`
- `gpt-4-0613`

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

This script:
- Takes results from a main reasoning method (e.g., one-step, two-step) and CoT results
- Identifies problems that failed in the main method but have non-standard output format
- Uses CoT results as backup for these specific cases to improve overall success rate
- Provides detailed reporting of which problems were corrected by the CoT backup

**Use case**: When your main reasoning method fails on certain problems but produces non-standard output (not "Option X is correct" format), the CoT backup can provide alternative solutions for those specific cases.

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