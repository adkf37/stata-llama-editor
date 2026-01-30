"""
Unit tests for Stata Editor components
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llama_client import LlamaClient
from stata_helper import StataHelper


class TestLlamaClient:
    """Test LlamaClient functionality"""
    
    def test_client_initialization(self):
        """Test that client initializes properly"""
        client = LlamaClient()
        assert client is not None
        assert client.model_name is not None
        assert client.ollama_host is not None
    
    def test_basic_generation(self):
        """Test basic text generation"""
        client = LlamaClient()
        response = client.generate("Say hello", max_tokens=50)
        assert response is not None
        assert len(response) > 0
        assert isinstance(response, str)
    
    def test_streaming_generation(self):
        """Test streaming generation"""
        client = LlamaClient()
        chunks = list(client.stream_generate("Count to 3", max_tokens=50))
        assert len(chunks) > 0
        full_response = ''.join(chunks)
        assert len(full_response) > 0
    
    def test_empty_prompt(self):
        """Test handling of empty prompt"""
        client = LlamaClient()
        response = client.generate("")
        # Should handle gracefully (not crash)
        assert response is not None


class TestStataHelper:
    """Test StataHelper functionality"""
    
    def test_helper_initialization(self):
        """Test helper initializes with common commands"""
        helper = StataHelper()
        assert helper is not None
        assert len(helper.common_commands) > 0
        assert 'regress' in helper.common_commands
    
    def test_contains_code_detection(self):
        """Test detection of Stata code in text"""
        helper = StataHelper()
        
        # Should detect code
        assert helper._contains_code("regress y x1 x2")
        assert helper._contains_code("summarize price")
        assert helper._contains_code("foreach var of varlist")
        
        # Should not detect in plain questions
        assert not helper._contains_code("What is statistics?")
        assert not helper._contains_code("Hello world")
    
    def test_enhance_prompt(self):
        """Test prompt enhancement"""
        helper = StataHelper()
        
        original = "Explain regression"
        enhanced = helper.enhance_prompt(original)
        
        assert len(enhanced) > len(original)
        assert original in enhanced
        assert 'Stata' in enhanced
    
    def test_common_commands_coverage(self):
        """Test that common Stata commands are included"""
        helper = StataHelper()
        expected_commands = ['regress', 'summarize', 'generate', 'merge', 'tabulate']
        
        for cmd in expected_commands:
            assert cmd in helper.common_commands


class TestIntegration:
    """Integration tests for the full system"""
    
    def test_stata_question_flow(self):
        """Test full flow of asking a Stata question"""
        client = LlamaClient()
        helper = StataHelper()
        
        question = "What does the regress command do?"
        enhanced = helper.enhance_prompt(question)
        response = client.generate(enhanced, max_tokens=100)
        
        assert response is not None
        assert len(response) > 0
        # Should mention regression-related concepts
        response_lower = response.lower()
        assert any(word in response_lower for word in ['regress', 'regression', 'linear'])
    
    def test_code_explanation_flow(self):
        """Test explaining Stata code"""
        client = LlamaClient()
        helper = StataHelper()
        
        code = "summarize price, detail"
        prompt = f"Explain this Stata code: {code}"
        enhanced = helper.enhance_prompt(prompt)
        response = client.generate(enhanced, max_tokens=150)
        
        assert response is not None
        response_lower = response.lower()
        assert any(word in response_lower for word in ['summary', 'statistics', 'detail'])


def run_tests():
    """Run all tests"""
    print("🧪 Running Unit Tests\n")
    pytest.main([__file__, '-v'])


if __name__ == '__main__':
    run_tests()
