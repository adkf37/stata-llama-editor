# Models (Ollama)

This project now uses **Ollama** for model management. No model files need to be stored in this directory.

## Setup

### 1. Install Ollama

If you haven't already:
- Visit: https://ollama.ai
- Download and install Ollama for your platform

### 2. Pull Llama 3.2

Run one of these commands to download the model:

```bash
# Standard Llama 3.2 (3B parameters)
ollama pull llama3.2

# Or specific size variants
ollama pull llama3.2:1b   # Smaller, faster
ollama pull llama3.2:3b   # Balanced (default)
```

### 3. Verify Installation

Check that Ollama is running and models are available:

```bash
# List installed models
ollama list

# Test the model
ollama run llama3.2 "Hello"
```

## Configuration

Update `config.yaml` to use your preferred model:

```yaml
model:
  name: llama3.2  # Or llama3.2:1b, llama3.2:3b, etc.
  path: models/your-model-file-name.gguf
```

## Note

Model files are excluded from version control via `.gitignore` due to their large size.
