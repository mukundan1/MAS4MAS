# tests/performance/test_memory.py
import pytest
import psutil
import gc
from praisonaiagents import Agent, Memory

class TestMemoryUsage:
    @pytest.mark.performance
    def test_memory_leak(self):
        """Test for memory leaks in agent execution"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run many agent iterations
        agent = Agent(name="MemTestAgent", instructions="Test memory")
        for i in range(100):
            agent.run(f"Iteration {i}")
            if i % 10 == 0:
                gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100  # Less than 100MB increase
    
    @pytest.mark.performance
    def test_conversation_memory_limit(self):
        """Test conversation memory limits"""
        agent = Agent(
            name="MemoryAgent",
            instructions="Remember conversations",
            memory=Memory(max_messages=10)
        )
        
        # Add many messages
        for i in range(20):
            agent.run(f"Message {i}")
        
        # Check memory is limited
        assert len(agent.memory.messages) <= 10