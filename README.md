# Stata Llama Editor

A local Stata code editor and assistant bot powered by Llama 3.2.

## Overview

This project provides an intelligent code editor and assistant for Stata programming, running entirely locally using the Llama 3.2 language model. It helps with code completion, debugging, explanation, and optimization of Stata scripts.

## Features

- **Code Assistance**: Get intelligent suggestions and completions for Stata code
- **Code Explanation**: Understand complex Stata commands and syntax
- **Debugging Help**: Identify and fix issues in your Stata scripts
- **Local Execution**: All processing happens on your machine - no cloud dependencies
- **Privacy-Focused**: Your code never leaves your computer

## Requirements

- Python 3.8 or higher
- Ollama installed and running
- At least 8GB RAM (16GB recommended for better performance)

## Installation

1. Install Ollama:
   - Visit https://ollama.ai and download Ollama for your platform
   - Install and start Ollama

2. Pull the Llama 3.2 model:
```bash
ollama pull llama3.2
```

3. Clone this repository:
```bash
git clone <repository-url>
cd stata-llama-editor
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

Run the web application:
```bash
python src/app.py
```

Then open your browser to: **http://localhost:5000**

Features:
- 💬 Interactive chat interface
- 🔄 Real-time streaming responses
- 📖 Quick command buttons (/explain, /fix, /optimize)
- 🎨 Modern, responsive design

### Command Line Interface

Run the CLI version:
```bash
python src/main.py
```

### Available Commands

- Type your Stata code or questions
- Use `/help` for available commands
- Use `/explain <code>` to get explanations
- Use `/fix <code>` to get debugging assistance
- Use `/optimize <code>` to get optimization suggestions

## Configuration

Edit `config.yaml` to customize:
- Model parameters (temperature, max tokens, etc.)
- Editor settings
- Response formatting preferences

## Project Structure

```
stata-llama-editor/
├── src/           # Source code
├── tests/         # Unit tests
├── models/        # Model files (gitignored)
├── config.yaml    # Configuration file
├── requirements.txt
└── README.md
```

## Testing

Run comprehensive test suite to evaluate performance:

```bash
# Run all tests with detailed report
python tests/run_all_tests.py

# Run evaluation tests only
python tests/test_evaluation.py

# Run performance benchmarks only
python tests/test_performance.py

# Run unit tests
python tests/test_unit.py
```

Test results are saved as JSON files for analysis.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

TBD

## Acknowledgments

- Built with Llama 3.2 by Meta
- Designed for the Stata programming community
