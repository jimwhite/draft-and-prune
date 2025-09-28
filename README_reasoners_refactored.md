# Refactored Reasoners Module

This document describes the refactored `reasoners_refactored.py` module that eliminates code redundancy while maintaining full functionality.

## 📊 Refactoring Results

- **Original**: 1,318 lines → **Refactored**: 881 lines
- **Reduction**: 437 lines (33% reduction)

## 🏗️ New Architecture

### Helper Classes (Extracted Common Functionality)

#### `DatasetConfig`
- Centralized dataset-to-solver mapping
- Dataset-specific import requirements
- Eliminates repeated mapping logic across classes

#### `PromptHandler`
- Unified prompt generation for all datasets and reasoning methods
- Single template loading and formatting logic
- Handles all prompt types: plan, code, direct, CoT, and fix prompts

#### `CodeExecutor`
- Consolidated code execution for all solvers (Z3, PyKE, CSP)
- Single implementation of execution logic
- Unified error handling and timeout management

#### `CodeCleaner`
- Centralized code cleaning logic for all datasets
- Markdown fence removal and import injection
- Dataset-specific processing rules

### Class Hierarchy

```
Reasoner (Abstract Base)
├── CodeBasedReasoner (Intermediate Base)
│   ├── TwoStepReasoner
│   └── DirectReasoner
└── CoTReasoner
```

#### `Reasoner` (Base Class)
- Common initialization and configuration
- API client management
- File operations and result folder creation
- Test execution (sequential and parallel)

#### `CodeBasedReasoner` (Intermediate Base)
- Shared logic for code-generating reasoners
- Common dataset-to-solver mapping
- Abstract code generation interface

#### `TwoStepReasoner`
- Plan generation → Code generation workflow
- Uses both `api_client` and `code_api_client`
- Saves both plans and codes

#### `DirectReasoner`
- Direct code generation in one step
- Uses single `api_client`
- Saves only codes

#### `CoTReasoner`
- Chain-of-Thought reasoning without code
- Answer extraction from reasoning output
- Saves reasoning text and evaluation results

## 🔄 Major Redundancies Eliminated

1. **Dataset-specific prompt formatting** → Single `PromptHandler`
2. **Code execution functions** → Single `CodeExecutor` 
3. **Dataset→solver mapping** → Centralized `DatasetConfig`
4. **Code cleaning logic** → Single `CodeCleaner`
5. **Result processing patterns** → Inheritance-based approach

## 🚀 Benefits

- **Maintainability**: Changes to common logic only need to be made once
- **Readability**: Clear separation of concerns
- **Extensibility**: Easy to add new datasets or reasoning methods
- **Bug Reduction**: Fewer places for inconsistencies
- **Performance**: Reduced code duplication

## 🔧 Usage

The refactored module is a **drop-in replacement** for the original `reasoners.py`:

```python
from reasoners_refactored import TwoStepReasoner, DirectReasoner, CoTReasoner

# Same API as before - no changes needed in calling code
reasoner = TwoStepReasoner(config, data_loader, answer_extractor)
result = reasoner.reason(test_case)
```

## 📁 File Structure Impact

The refactored code maintains identical output file structures:

- **TwoStepReasoner**: Creates `plan/` and `code/` folders
- **DirectReasoner**: Creates `code/` folder only  
- **CoTReasoner**: Creates `reasoning/` folder only
- **All**: Create `summary/` folder with JSON results

## 🔍 Key Design Patterns

1. **Strategy Pattern**: Different reasoning approaches via inheritance
2. **Template Method**: Common workflows with specialized implementations
3. **Composition**: Helper classes for specific responsibilities
4. **Factory Pattern**: Solver function selection via `CodeExecutor`

## 🧪 Testing

The refactored code has been verified to:
- ✅ Maintain identical functionality
- ✅ Produce same output formats
- ✅ Support all existing datasets
- ✅ Pass linting without errors
- ✅ Preserve all configuration options

