#!/usr/bin/env python3
"""Quick test of Ollama connection"""

from src.llama_client import LlamaClient

print("Initializing Ollama client...")
client = LlamaClient()
print("✓ Client initialized successfully!")

print("\nSending test query to Llama 3.2...")
response = client.generate("Say 'hello' in one word.")
print(f"✓ Response received: {response}")

print("\n✅ All tests passed! Your Stata Llama Editor is ready to use.")
print("\nRun the application with: python src/main.py")
