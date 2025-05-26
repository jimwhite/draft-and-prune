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

### Configuration File Structure

The YAML configuration file contains all necessary parameters:

```yaml
# Required fields
dataset: "AR-LSAT"                                    # Dataset name to use
test_file: "./data/AR-LSAT/blob/main/complete_lsat_data/test_ar.json"  # Test file path
reasoning_method: "two-step"                          # Reasoning approach
api_key: "YOUR_API_KEY_HERE"                         # Google API key for Gemini models
model: "gemini-2.5-flash-preview-04-17"             # Primary model name
fix_model: "gemini-2.5-flash-preview-04-17"         # Model for fixing/repair operations
temperature: 0                                       # Temperature for generation (0.0 to 1.0)
max_repairs: 3                                       # Maximum repair attempts
test_delay: 5                                        # Delay between test cases in seconds
prompt_path: "./prompts/AR-LSAT-prompts-two-step-partition/"  # Path to prompt templates
shots: "two"                                         # Number of examples ("zero", "one", "two", "three")
desired_indices: [0]                                 # Specific test case indices to run (optional)
```

## Configuration Options

### Reasoning Methods
- `"CoT"`: Chain of Thought reasoning
- `"one-step"`: Single-step reasoning
- `"two-step"`: Two-step reasoning (plan then code)
- `"three-step"`: Three-step reasoning

### Shots (Few-shot Learning)
- `"zero"`: No examples
- `"one"`: One example
- `"two"`: Two examples  
- `"three"`: Three examples

### Models
- `"gemini-2.5-flash-preview-04-17"` (default)
- `"gemini-1.5-pro"`
- Other Gemini models supported

## Examples

### Basic Usage with Two-step Reasoning:

```bash
# Copy and edit the sample config
cp config_sample.yaml experiment1.yaml
# Edit experiment1.yaml with your API key and settings
python main.py experiment1.yaml
```

### Running Different Experiments:

```bash
# Zero-shot experiment
cp config_sample.yaml zero_shot.yaml
# Edit zero_shot.yaml: set shots: "zero"
python main.py zero_shot.yaml

# Few-shot experiment  
cp config_sample.yaml few_shot.yaml
# Edit few_shot.yaml: set shots: "two"
python main.py few_shot.yaml

# Different model experiment
cp config_sample.yaml gemini_pro.yaml
# Edit gemini_pro.yaml: set model: "gemini-1.5-pro"
python main.py gemini_pro.yaml
```

## Project Structure

- `main.py`: Entry point of the application
- `config.py`: Configuration management
- `config_sample.yaml`: Sample configuration file
- `reasoners.py`: Implements different reasoning approaches
- `data_loaders.py`: Loads and processes test data
- `answer_extractors.py`: Extracts answers from model responses
- `call_api.py`: Handles API interactions with LLM providers

## Results

Results are automatically saved in timestamped folders:
- `results_YYYY-MM-DD/method-dataset-model-shots_shot_CoT/`
- Contains generated plans, code, and summary results
- Configuration is automatically saved for reproducibility

## Supported Datasets

Currently supports:
- AR-LSAT: Analytical Reasoning tasks from the Law School Admission Test
  - Source: [AR-LSAT GitHub Repository](https://github.com/zhongwanjun/AR-LSAT)
  - Path: AR-LSAT/blob/main/complete_lsat_data/test_ar.json

## To Do
- [ ] Implement checker/verifier

## License

[Include your license information here]