# Partitioned Neural-Symbolic Reasoning

This project explores the combination of neural language models with symbolic reasoning engines to solve logical reasoning problems.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Partitioned-Neural-Symbolic-Reasoning.git
cd Partitioned-Neural-Symbolic-Reasoning

# Get the AR-LSAT dataset
git clone https://github.com/zhongwanjun/AR-LSAT.git

# Install dependencies
pip install -r requirements.txt
```

Required dependencies:
- python >= 3.8
- google-generativeai
- openai (optional, for GPT models)
- z3-solver

## Usage

Run the main script with the following parameters:

```bash
python main.py --api_key YOUR_API_KEY --test_file PATH_TO_TEST_FILE [options]
```

### Required Arguments

- `--api_key`: Google API key for accessing Gemini models
- `--test_file`: Path to the test file (e.g., AR-LSAT/blob/main/complete_lsat_data/test_ar.json)

### Optional Arguments

- `--limit`: Limit the number of samples to process
- `--model`: Model to use (default: "gemini-2.5-flash-preview-04-17")
- `--dataset`: Dataset type (default: "AR-LSAT")
- `--temperature`: Temperature for generation (default: 0.0)
- `--max-repairs`: Maximum repair attempts for API calls (default: 3)
- `--test-delay`: Delay between test cases in seconds (default: 5)
- `--reasoning-method`: Reasoning approach (default: "two-step")
  - Options: "CoT", "one-step", "two-step", "three-step"
- `--shots`: Number of examples to include (default: "zero")
  - Options: "zero", "one", "two", "three"

## Examples

### Two-step reasoning with the AR-LSAT dataset:

```bash
python main.py \
  --api_key YOUR_API_KEY \
  --test_file AR-LSAT/blob/main/complete_lsat_data/test_ar.json \
  --reasoning-method two-step \
  --shots zero
```

### Using a specific model with temperature adjustment:

```bash
python main.py \
  --api_key YOUR_API_KEY \
  --test_file AR-LSAT/blob/main/complete_lsat_data/test_ar.json \
  --model "gemini-1.5-pro" \
  --temperature 0.2 \
  --shots two
```

## Project Structure

- `main.py`: Entry point of the application
- `config.py`: Configuration management
- `reasoners.py`: Implements different reasoning approaches
- `data_loaders.py`: Loads and processes test data
- `answer_extractors.py`: Extracts answers from model responses
- `call_api.py`: Handles API interactions with LLM providers

## Supported Datasets

Currently supports:
- AR-LSAT: Analytical Reasoning tasks from the Law School Admission Test
  - Source: [AR-LSAT GitHub Repository](https://github.com/zhongwanjun/AR-LSAT)
  - Path: AR-LSAT/blob/main/complete_lsat_data/test_ar.json

## License

[Include your license information here]