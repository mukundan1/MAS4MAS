# tests/unit/test_agent.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from praisonaiagents import Agent

class TestAgent:
    def test_agent_initialization(self):
        """Test agent can be initialized with basic parameters"""
        agent = Agent(
            name="TestAgent",
            instructions="Test instructions",
            llm_model="gpt-4"
        )
        
        assert agent.name == "TestAgent"
        assert agent.instructions == "Test instructions"
        assert agent.llm_model == "gpt-4"
    
    def test_agent_with_tools(self):
        """Test agent initialization with tools"""
        mock_tool = Mock()
        mock_tool.name = "test_tool"
        
        agent = Agent(
            name="ToolAgent",
            instructions="Agent with tools",
            tools=[mock_tool]
        )
        
        assert len(agent.tools) == 1
        assert agent.tools[0].name == "test_tool"
    
    @patch('praisonaiagents.agent.agent.litellm.completion')
    def test_agent_run_sync(self, mock_completion):
        """Test synchronous agent execution"""
        # Setup mock response
        mock_completion.return_value = Mock(
            choices=[Mock(message=Mock(content="Test response"))]
        )
        
        agent = Agent(name="TestAgent", instructions="Test")
        result = agent.run("Test input")
        
        assert result == "Test response"
        mock_completion.assert_called_once()
    
    @patch('praisonaiagents.agent.agent.litellm.acompletion')
    async def test_agent_run_async(self, mock_acompletion):
        """Test asynchronous agent execution"""
        # Setup mock response
        mock_acompletion.return_value = Mock(
            choices=[Mock(message=Mock(content="Async test response"))]
        )
        
        agent = Agent(name="TestAgent", instructions="Test")
        result = await agent.arun("Test input")
        
        assert result == "Async test response"
        mock_acompletion.assert_called_once()
    
    def test_agent_validation(self):
        """Test agent input validation"""
        with pytest.raises(ValueError):
            Agent(name="", instructions="Test")  # Empty name
        
        with pytest.raises(ValueError):
            Agent(name="Test", instructions="")  # Empty instructions
        
        with pytest.raises(ValueError):
            Agent(name="Test", instructions="Test", max_tokens=-1)  # Invalid max_tokens