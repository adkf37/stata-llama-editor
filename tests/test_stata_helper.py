"""
Tests for Stata Helper module
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from stata_helper import StataHelper


class TestStataHelper:
    """Test suite for StataHelper class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.helper = StataHelper()
    
    def test_initialization(self):
        """Test helper initializes correctly"""
        assert self.helper is not None
        assert len(self.helper.common_commands) > 0
        assert self.helper.stata_context != ""
    
    def test_contains_code_detection(self):
        """Test Stata code detection"""
        # Should detect Stata code
        assert self.helper._contains_code("regress y x1 x2")
        assert self.helper._contains_code("summarize myvar")
        assert self.helper._contains_code("generate newvar = oldvar * 2")
        
        # Should not detect regular text
        assert not self.helper._contains_code("Hello world")
        assert not self.helper._contains_code("How do I analyze data?")
    
    def test_extract_code_blocks(self):
        """Test code block extraction"""
        text = """
Here is some code:
```stata
regress y x
```
And inline: `summarize var`
        """
        blocks = self.helper.extract_code_blocks(text)
        assert len(blocks) == 2
        assert "regress y x" in blocks[0]
        assert "summarize var" in blocks[1]
    
    def test_validate_syntax_balanced_braces(self):
        """Test syntax validation for balanced braces"""
        valid_code = "foreach var of varlist x1 x2 { \n summarize `var' \n }"
        is_valid, error = self.helper.validate_syntax(valid_code)
        assert is_valid
        assert error is None
        
        invalid_code = "foreach var of varlist x1 x2 { \n summarize `var'"
        is_valid, error = self.helper.validate_syntax(invalid_code)
        assert not is_valid
        assert "braces" in error.lower()
    
    def test_validate_syntax_quotes(self):
        """Test syntax validation for quotes"""
        valid_code = 'display "Hello world"'
        is_valid, error = self.helper.validate_syntax(valid_code)
        assert is_valid
        
        invalid_code = 'display "Hello world'
        is_valid, error = self.helper.validate_syntax(invalid_code)
        assert not is_valid
        assert "quote" in error.lower()
    
    def test_enhance_prompt(self):
        """Test prompt enhancement"""
        user_prompt = "How do I run a regression?"
        enhanced = self.helper.enhance_prompt(user_prompt)
        
        assert user_prompt in enhanced
        assert "Stata" in enhanced
        assert len(enhanced) > len(user_prompt)
    
    def test_format_code(self):
        """Test code formatting"""
        unformatted = "foreach var in x1 x2 {\nsummarize `var'\n}"
        formatted = self.helper.format_code(unformatted)
        
        assert "    summarize" in formatted  # Should be indented
        lines = formatted.split('\n')
        assert len(lines) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
