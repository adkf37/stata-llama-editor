"""
Stata Llama Editor
A local Stata code editor and assistant bot powered by Llama 3.2
"""

__version__ = "0.1.0"
__author__ = "Stata Llama Editor Contributors"

from .llama_client import LlamaClient
from .stata_helper import StataHelper

__all__ = ["LlamaClient", "StataHelper"]
