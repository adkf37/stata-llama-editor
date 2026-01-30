"""
Llama Client Module
Handles interaction with the Llama 3.2 model
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class LlamaClient:
    """Client for interacting with Llama 3.2 model"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the Llama client with configuration"""
        self.config = self._load_config(config_path)
        self.model = None
        self.model_path = self.config.get('model', {}).get('path')
        self._initialize_model()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default config if file doesn't exist
            return {
                'model': {
                    'path': 'models/llama-3.2-3b-instruct.gguf',
                    'temperature': 0.7,
                    'max_tokens': 2048,
                    'top_p': 0.9,
                    'context_window': 4096
                }
            }
    
    def _initialize_model(self):
        """Initialize the Llama model"""
        try:
            from llama_cpp import Llama
            
            model_config = self.config.get('model', {})
            
            # Check if model file exists
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    f"Model file not found: {self.model_path}\n"
                    f"Please download the Llama 3.2 model and place it in the models/ directory.\n"
                    f"See models/README.md for instructions."
                )
            
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=model_config.get('context_window', 4096),
                n_threads=model_config.get('threads', 4),
                verbose=False
            )
            
        except ImportError:
            raise ImportError(
                "llama-cpp-python is not installed. "
                "Please run: pip install llama-cpp-python"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Llama model: {str(e)}")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        model_config = self.config.get('model', {})
        
        # Merge default config with kwargs
        generation_params = {
            'temperature': model_config.get('temperature', 0.7),
            'max_tokens': model_config.get('max_tokens', 2048),
            'top_p': model_config.get('top_p', 0.9),
            'stop': model_config.get('stop_sequences', []),
            **kwargs
        }
        
        # Format prompt with system message
        system_message = self.config.get('prompts', {}).get('system_message', '')
        formatted_prompt = self._format_prompt(prompt, system_message)
        
        # Generate response
        response = self.model(
            formatted_prompt,
            **generation_params
        )
        
        # Extract text from response
        return response['choices'][0]['text'].strip()
    
    def _format_prompt(self, user_prompt: str, system_message: str) -> str:
        """Format the prompt with system message"""
        if system_message:
            return f"<|system|>\n{system_message}\n<|user|>\n{user_prompt}\n<|assistant|>\n"
        return user_prompt
    
    def stream_generate(self, prompt: str, **kwargs):
        """
        Generate a streaming response from the model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Yields:
            Chunks of generated text
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        model_config = self.config.get('model', {})
        
        generation_params = {
            'temperature': model_config.get('temperature', 0.7),
            'max_tokens': model_config.get('max_tokens', 2048),
            'top_p': model_config.get('top_p', 0.9),
            'stream': True,
            **kwargs
        }
        
        system_message = self.config.get('prompts', {}).get('system_message', '')
        formatted_prompt = self._format_prompt(prompt, system_message)
        
        for chunk in self.model(formatted_prompt, **generation_params):
            if 'choices' in chunk and len(chunk['choices']) > 0:
                text = chunk['choices'][0].get('text', '')
                if text:
                    yield text
