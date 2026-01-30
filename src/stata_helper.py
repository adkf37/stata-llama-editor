"""
Stata Helper Module
Provides utilities for Stata code analysis and prompt enhancement
"""

from typing import List, Dict, Optional
import re


class StataHelper:
    """Helper class for Stata-specific operations"""
    
    def __init__(self):
        """Initialize Stata helper with common commands and patterns"""
        self.common_commands = self._load_common_commands()
        self.stata_context = self._load_stata_context()
    
    def _load_common_commands(self) -> Dict[str, str]:
        """Load common Stata commands and their descriptions"""
        return {
            'regress': 'Linear regression',
            'summarize': 'Summary statistics',
            'tabulate': 'Frequency tables',
            'generate': 'Create new variables',
            'replace': 'Replace variable values',
            'drop': 'Drop variables or observations',
            'keep': 'Keep variables or observations',
            'merge': 'Merge datasets',
            'append': 'Append datasets',
            'collapse': 'Make dataset of summary statistics',
            'reshape': 'Convert data from wide to long or vice versa',
            'foreach': 'Loop over items',
            'forvalues': 'Loop over consecutive values',
            'if': 'Conditional execution',
            'egen': 'Extensions to generate',
            'bysort': 'Sort and process by groups',
        }
    
    def _load_stata_context(self) -> str:
        """Load Stata programming context for prompts"""
        return """
You are a Stata programming assistant. Stata is a statistical software package 
used for data analysis, data management, and graphics. When helping with Stata code:

1. Use proper Stata syntax and conventions
2. Consider data management best practices
3. Be aware of common Stata commands and their options
4. Provide clear, efficient, and well-commented code
5. Consider memory efficiency and performance
6. Follow Stata's naming conventions (lowercase for variables and commands)
7. Use appropriate data types and formats
8. Consider using -preserve- and -restore- when making temporary changes
        """.strip()
    
    def enhance_prompt(self, user_prompt: str) -> str:
        """
        Enhance user prompt with Stata-specific context
        
        Args:
            user_prompt: Original user prompt
            
        Returns:
            Enhanced prompt with Stata context
        """
        # Add Stata context to prompt
        enhanced = f"{self.stata_context}\n\n"
        
        # Detect if code is present
        if self._contains_code(user_prompt):
            enhanced += "Here is the Stata code to analyze:\n\n"
        
        enhanced += user_prompt
        
        return enhanced
    
    def _contains_code(self, text: str) -> bool:
        """Check if text contains Stata code"""
        # Look for common Stata patterns
        stata_patterns = [
            r'\bregress\b',
            r'\bsummarize\b',
            r'\bgenerate\b',
            r'\btabulate\b',
            r'\bforeach\b',
            r'\bforvalues\b',
            r'\bif\b.*\bthen\b',
            r'\bdi\b|\bdisplay\b',
            r'[a-z_]+\s*=\s*',  # Variable assignment
            r'\*\s*[A-Za-z]',  # Comments
        ]
        
        for pattern in stata_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def extract_code_blocks(self, text: str) -> List[str]:
        """
        Extract code blocks from text
        
        Args:
            text: Text potentially containing code blocks
            
        Returns:
            List of extracted code blocks
        """
        # Look for code in backticks or indented blocks
        code_blocks = []
        
        # Markdown code blocks
        markdown_pattern = r'```(?:stata|do)?\n(.*?)```'
        code_blocks.extend(re.findall(markdown_pattern, text, re.DOTALL))
        
        # Inline code
        inline_pattern = r'`([^`]+)`'
        code_blocks.extend(re.findall(inline_pattern, text))
        
        return [block.strip() for block in code_blocks if block.strip()]
    
    def format_code(self, code: str) -> str:
        """
        Format Stata code for better readability
        
        Args:
            code: Raw Stata code
            
        Returns:
            Formatted code
        """
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Decrease indent for closing braces
            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
            
            # Add indentation
            if stripped:
                formatted_lines.append('    ' * indent_level + stripped)
            else:
                formatted_lines.append('')
            
            # Increase indent for opening braces or foreach/forvalues
            if stripped.endswith('{') or stripped.startswith(('foreach', 'forvalues')):
                indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    def validate_syntax(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Basic syntax validation for Stata code
        
        Args:
            code: Stata code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for balanced braces
        open_braces = code.count('{')
        close_braces = code.count('}')
        
        if open_braces != close_braces:
            return False, "Unbalanced braces: {} opening, {} closing".format(
                open_braces, close_braces
            )
        
        # Check for common syntax errors
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for unclosed quotes
            if stripped.count('"') % 2 != 0:
                return False, f"Unclosed quote on line {i}"
            
            if stripped.count("'") % 2 != 0:
                return False, f"Unclosed quote on line {i}"
        
        return True, None
