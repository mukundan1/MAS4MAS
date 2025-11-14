# tests/integration/test_tool_integration.py
import pytest
from unittest.mock import Mock, patch
import aiohttp
from praisonaiagents import Agent, Tool

class TestToolIntegration:
    @pytest.mark.integration
    @patch('aiohttp.ClientSession.get')
    async def test_web_search_tool(self, mock_get):
        """Test web search tool integration"""
        # Mock API response
        mock_response = Mock()
        mock_response.json = Mock(return_value={
            "results": [{"title": "Test", "snippet": "Test result"}]
        })
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # Create search tool
        async def web_search(query: str) -> str:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.search.com?q={query}") as response:
                    data = await response.json()
                    return data["results"][0]["snippet"]
        
        search_tool = Tool(
            name="web_search",
            description="Search the web",
            function=web_search
        )
        
        # Test with agent
        agent = Agent(
            name="SearchAgent",
            instructions="Search for information",
            tools=[search_tool]
        )
        
        result = await agent.arun("Search for test")
        assert "Test result" in str(result)
    
    @pytest.mark.integration
    def test_tool_error_handling(self):
        """Test tool error handling"""
        def failing_tool(x: int) -> int:
            raise ValueError("Tool failed")
        
        tool = Tool(
            name="failing_tool",
            description="Tool that fails",
            function=failing_tool
        )
        
        agent = Agent(
            name="TestAgent",
            instructions="Use the tool",
            tools=[tool]
        )
        
        # Agent should handle tool failure gracefully
        with pytest.raises(Exception):
            agent.run("Use failing_tool with x=5")