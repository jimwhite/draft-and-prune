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

## API Keys

### Google AI (Gemini)
- Get key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Models: `gemini-2.5-flash-preview-04-17`, `gemini-1.5-pro`

### OpenAI (GPT)
- Get key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Models: `gpt-4-0314`, `gpt-3.5-turbo`

## Features

### Reasoning Methods
- `"CoT"`: Chain of Thought
- `"one-step"`: Single-step reasoning
- `"two-step"`: Two-step reasoning (plan then code)
- `"three-step"`: Three-step reasoning

### Models
- `"gemini-2.5-flash-preview-04-17"` (default)
- `"gemini-1.5-pro"`
- `gpt-4-0314`

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

## Project Structure

- `main.py`: Application entry point
- `config.py`: Configuration management
- `reasoners.py`: Reasoning approaches
- `data_loaders.py`: Test data processing
- `answer_extractors.py`: Answer extraction
- `call_api.py`: LLM API interactions
- `analysis.py`: Results analysis

## Supported Datasets

- AR-LSAT: Analytical Reasoning tasks from LSAT
  - Source: [AR-LSAT GitHub](https://github.com/zhongwanjun/AR-LSAT)
  - Path: `AR-LSAT/blob/main/complete_lsat_data/test_ar.json`

## To Do
- [ ] Implement checker/verifier

## License

[Include your license information here]