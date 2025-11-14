# tests/conftest.py
import pytest
import os
from unittest.mock import Mock, patch
from praisonaiagents import Agent, Task

# Test configuration
@pytest.fixture(scope="session")
def test_config():
    return {
        "use_mock_llm": os.getenv("USE_MOCK_LLM", "true").lower() == "true",
        "test_api_key": "test-key-123",
        "max_test_duration": 30,  # seconds
        "mock_response_delay": 0.1  # simulate API delay
    }

# Mock LLM for testing
@pytest.fixture
def mock_llm(test_config):
    if not test_config["use_mock_llm"]:
        return None
    
    mock = Mock()
    mock.generate.return_value = "Mocked response"
    mock.agenerate.return_value = "Mocked async response"
    return mock

# Test agent fixture
@pytest.fixture
def test_agent(mock_llm):
    agent = Agent(
        name="TestAgent",
        instructions="You are a test agent",
        llm=mock_llm
    )
    return agent