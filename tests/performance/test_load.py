# tests/performance/test_load.py
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from praisonaiagents import Agent

class TestPerformance:
    @pytest.mark.performance
    def test_concurrent_agents(self, test_agent):
        """Test multiple agents running concurrently"""
        num_agents = 10
        num_requests = 5
        
        def run_agent(agent_id):
            agent = Agent(
                name=f"Agent{agent_id}",
                instructions="Process request"
            )
            results = []
            for i in range(num_requests):
                start = time.time()
                result = agent.run(f"Request {i}")
                duration = time.time() - start
                results.append(duration)
            return results
        
        with ThreadPoolExecutor(max_workers=num_agents) as executor:
            futures = [executor.submit(run_agent, i) for i in range(num_agents)]
            all_results = []
            
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        avg_time = sum(all_results) / len(all_results)
        assert avg_time < 5  # Average response time under 5 seconds
    
    @pytest.mark.performance
    async def test_async_performance(self):
        """Test async agent performance"""
        num_concurrent = 20
        
        async def process_request(agent, request_id):
            start = time.time()
            await agent.arun(f"Process request {request_id}")
            return time.time() - start
        
        agent = Agent(name="AsyncAgent", instructions="Process quickly")
        
        tasks = [
            process_request(agent, i)
            for i in range(num_concurrent)
        ]
        
        results = await asyncio.gather(*tasks)
        
        avg_time = sum(results) / len(results)
        max_time = max(results)
        
        assert avg_time < 3  # Average under 3 seconds
        assert max_time < 10  # No request over 10 seconds