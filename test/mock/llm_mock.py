# tests/mocks/llm_mock.py
from typing import Dict, List, Any
import random
import time

class MockLLM:
    def __init__(self, responses: Dict[str, str] = None):
        self.responses = responses or {}
        self.default_responses = [
            "I understand your request.",
            "Here's what I found.",
            "Task completed successfully.",
            "Processing your request."
        ]
        self.call_count = 0
        self.last_prompt = None
    
    def generate(self, prompt: str, **kwargs) -> str:
        self.call_count += 1
        self.last_prompt = prompt
        
        # Simulate processing time
        time.sleep(0.1)
        
        # Check for specific responses
        for key, response in self.responses.items():
            if key in prompt.lower():
                return response
        
        # Return random default response
        return random.choice(self.default_responses)
    
    async def agenerate(self, prompt: str, **kwargs) -> str:
        await asyncio.sleep(0.1)
        return self.generate(prompt, **kwargs)

# Usage in tests
@pytest.fixture
def smart_mock_llm():
    return MockLLM(responses={
        "weather": "It's sunny today with a temperature of 72°F.",
        "calculate": "The result is 42.",
        "error": "Error: Invalid input provided."
    })