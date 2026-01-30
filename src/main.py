#!/usr/bin/env python3
"""
Stata Llama Editor - Main Application
A local Stata code editor and assistant bot powered by Llama 3.2
"""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from llama_client import LlamaClient
from stata_helper import StataHelper


console = Console()


class StataLlamaEditor:
    """Main application class for Stata Llama Editor"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the editor with configuration"""
        self.config_path = config_path or "config.yaml"
        self.llama_client = LlamaClient(self.config_path)
        self.stata_helper = StataHelper()
        self.session = PromptSession(
            history=FileHistory('.stata_llama_history')
        )
        
    def print_welcome(self):
        """Print welcome message"""
        welcome_text = """
# Stata Llama Editor

Welcome to the Stata code assistant powered by Llama 3.2!

**Available Commands:**
- `/help` - Show this help message
- `/explain <code>` - Explain Stata code
- `/fix <code>` - Debug and fix Stata code
- `/optimize <code>` - Suggest optimizations
- `/exit` or `/quit` - Exit the application

Type your Stata code or questions to get started!
        """
        console.print(Panel(Markdown(welcome_text), title="[bold green]Welcome[/bold green]"))
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands
        Returns True if command was handled, False if should be sent to LLM
        """
        if user_input.startswith('/'):
            command = user_input.lower().split()[0]
            
            if command in ['/exit', '/quit']:
                console.print("\n[yellow]Goodbye![/yellow]")
                sys.exit(0)
            
            elif command == '/help':
                self.print_welcome()
                return True
            
            elif command == '/explain':
                code = user_input[len('/explain'):].strip()
                if code:
                    prompt = f"Please explain this Stata code:\n\n{code}"
                    return self.process_query(prompt)
                else:
                    console.print("[red]Error: No code provided[/red]")
                    return True
            
            elif command == '/fix':
                code = user_input[len('/fix'):].strip()
                if code:
                    prompt = f"Please debug and fix this Stata code:\n\n{code}"
                    return self.process_query(prompt)
                else:
                    console.print("[red]Error: No code provided[/red]")
                    return True
            
            elif command == '/optimize':
                code = user_input[len('/optimize'):].strip()
                if code:
                    prompt = f"Please suggest optimizations for this Stata code:\n\n{code}"
                    return self.process_query(prompt)
                else:
                    console.print("[red]Error: No code provided[/red]")
                    return True
            
            else:
                console.print(f"[red]Unknown command: {command}[/red]")
                return True
        
        return False
    
    def process_query(self, query: str) -> bool:
        """Process a user query with the LLM"""
        try:
            # Add Stata context to the query
            enhanced_query = self.stata_helper.enhance_prompt(query)
            
            # Get response from Llama
            with console.status("[bold green]Thinking...[/bold green]"):
                response = self.llama_client.generate(enhanced_query)
            
            # Display response
            console.print("\n[bold cyan]Response:[/bold cyan]")
            console.print(Panel(Markdown(response)))
            console.print()
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return True
    
    def run(self):
        """Main application loop"""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = self.session.prompt('\n> ').strip()
                
                if not user_input:
                    continue
                
                # Handle commands or process query
                if not self.handle_command(user_input):
                    self.process_query(user_input)
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use /exit to quit[/yellow]")
                continue
            except EOFError:
                console.print("\n[yellow]Goodbye![/yellow]")
                break


@click.command()
@click.option('--config', '-c', default='config.yaml', 
              help='Path to configuration file')
@click.option('--model-path', '-m', default=None,
              help='Override model path from config')
def main(config: str, model_path: Optional[str]):
    """
    Stata Llama Editor - Local Stata code assistant powered by Llama 3.2
    """
    try:
        editor = StataLlamaEditor(config_path=config)
        
        # Override model path if provided
        if model_path:
            editor.llama_client.model_path = model_path
            
        editor.run()
        
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
