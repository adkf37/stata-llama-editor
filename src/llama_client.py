"""
Llama Client Module
Handles interaction with the Llama 3.2 model via Ollama
"""

import os
from typing import Optional, Dict, Any
import yaml


class LlamaClient:
    """Client for interacting with Llama 3.2 model via Ollama"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the Llama client with configuration"""
        self.config = self._load_config(config_path)
        self.model_name = self.config.get('model', {}).get('name', 'llama3.2')
        self.ollama_host = self.config.get('model', {}).get('host', 'http://localhost:11434')
        self._initialize_ollama()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # Return default config if file doesn't exist
            return {
                'model': {
                    'name': 'llama3.2',
                    'host': 'http://localhost:11434',
                    'temperature': 0.7,
                    'max_tokens': 2048,
                    'top_p': 0.9
                }
            }
    
    def _initialize_ollama(self):
        """Initialize connection to Ollama"""
        try:
            import ollama
            self.client = ollama.Client(host=self.ollama_host)
            
            # Test connection by listing models
            try:
                models_response = self.client.list()
                if hasattr(models_response, 'models'):
                    model_names = [model.model for model in models_response.models]
                else:
                    model_names = []
                
                # Check if requested model is available
                if model_names and not any(self.model_name in name for name in model_names):
                    print(f"Warning: Model '{self.model_name}' not found in Ollama.")
                    print(f"Available models: {', '.join(model_names)}")
                    print(f"Run: ollama pull {self.model_name}")
            except Exception as e:
                # Silently ignore - model verification is optional
                pass
                
        except ImportError:
            raise ImportError(
                "ollama package is not installed. "
                "Please run: pip install ollama"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to connect to Ollama at {self.ollama_host}\n"
                f"Make sure Ollama is running. Error: {str(e)}"
            )
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response from the model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            Generated text response
        """
        model_config = self.config.get('model', {})
        
        # Get system message
        system_message = self.config.get('prompts', {}).get('system_message', '')
        
        # Build messages
        messages = []
        if system_message:
            messages.append({
                'role': 'system',
                'content': system_message
            })
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        # Merge default config with kwargs
        options = {
            'temperature': kwargs.get('temperature', model_config.get('temperature', 0.7)),
            'num_predict': kwargs.get('max_tokens', model_config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', model_config.get('top_p', 0.9)),
        }
        
        # Add stop sequences if provided
        stop_sequences = model_config.get('stop_sequences', [])
        if stop_sequences:
            options['stop'] = stop_sequences
        
        try:
            # Generate response
            response = self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options,
                stream=False
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")
    
    def stream_generate(self, prompt: str, **kwargs):
        """
        Generate a streaming response from the model
        
        Args:
            prompt: The input prompt
            **kwargs: Additional generation parameters
            
        Yields:
            Chunks of generated text
        """
        model_config = self.config.get('model', {})
        
        # Get system message
        system_message = self.config.get('prompts', {}).get('system_message', '')
        
        # Build messages
        messages = []
        if system_message:
            messages.append({
                'role': 'system',
                'content': system_message
            })
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        # Merge default config with kwargs
        options = {
            'temperature': kwargs.get('temperature', model_config.get('temperature', 0.7)),
            'num_predict': kwargs.get('max_tokens', model_config.get('max_tokens', 2048)),
            'top_p': kwargs.get('top_p', model_config.get('top_p', 0.9)),
        }
        
        try:
            # Generate streaming response
            stream = self.client.chat(
                model=self.model_name,
                messages=messages,
                options=options,
                stream=True
            )
            
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    yield chunk['message']['content']
                    
        except Exception as e:
            raise RuntimeError(f"Failed to generate streaming response: {str(e)}")
