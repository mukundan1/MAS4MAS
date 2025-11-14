# tests/unit/test_tools.py
import pytest
from unittest.mock import Mock, patch
from praisonaiagents import Tool

class TestTools:
    def test_tool_creation(self):
        """Test tool initialization"""
        def sample_function(x: int) -> int:
            return x * 2
        
        tool = Tool(
            name="multiplier",
            description="Multiplies input by 2",
            function=sample_function
        )
        
        assert tool.name == "multiplier"
        assert tool.function(5) == 10
    
    def test_tool_validation(self):
        """Test tool parameter validation"""
        def typed_function(x: int, y: str) -> str:
            return f"{y}: {x}"
        
        tool = Tool(
            name="typed_tool",
            description="Tool with type hints",
            function=typed_function
        )
        
        # Should work with correct types
        result = tool.execute(x=5, y="Number")
        assert result == "Number: 5"
        
        # Should handle type conversion
        result = tool.execute(x="5", y=10)
        assert result == "10: 5"
    
    def test_async_tool(self):
        """Test asynchronous tool"""
        async def async_function(x: int) -> int:
            return x * 3
        
        tool = Tool(
            name="async_multiplier",
            description="Async multiplier",
            function=async_function
        )
        
        assert tool.is_async
        # Test execution would require async context