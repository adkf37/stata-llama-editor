# Model Files

This directory should contain the Llama 3.2 model files in GGUF format.

## Downloading the Model

You have several options to download the Llama 3.2 model:

### Option 1: Using Hugging Face

1. Install the Hugging Face CLI:
```bash
pip install huggingface-hub
```

2. Download a quantized GGUF model (recommended for local use):
```bash
huggingface-cli download TheBloke/Llama-3.2-3B-Instruct-GGUF llama-3.2-3b-instruct.Q4_K_M.gguf --local-dir ./models --local-dir-use-symlinks False
```

### Option 2: Manual Download

1. Visit the Hugging Face model repository:
   - For 3B model: https://huggingface.co/TheBloke/Llama-3.2-3B-Instruct-GGUF
   - For 1B model (lighter): https://huggingface.co/TheBloke/Llama-3.2-1B-Instruct-GGUF

2. Download the GGUF file (recommended: Q4_K_M quantization for balance of size and quality)

3. Place the downloaded `.gguf` file in this directory

### Option 3: Using llama.cpp

If you prefer to quantize the model yourself:

1. Clone llama.cpp: https://github.com/ggerganov/llama.cpp
2. Follow their instructions to convert and quantize the model
3. Copy the resulting `.gguf` file to this directory

## Recommended Models

- **llama-3.2-3b-instruct.Q4_K_M.gguf** (~2.2GB) - Good balance of size and performance
- **llama-3.2-3b-instruct.Q5_K_M.gguf** (~2.7GB) - Higher quality, slightly larger
- **llama-3.2-1b-instruct.Q4_K_M.gguf** (~0.7GB) - Faster but less capable

## Configuration

After downloading, update the model path in `config.yaml` if needed:

```yaml
model:
  path: models/your-model-file-name.gguf
```

## Note

Model files are excluded from version control via `.gitignore` due to their large size.
