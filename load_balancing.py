# load_balancer/agent_balancer.py
from typing import List, Optional
import random
from collections import defaultdict

class AgentLoadBalancer:
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.agent_loads = defaultdict(int)
        self.agent_errors = defaultdict(int)
    
    def select_agent(self) -> Optional[Agent]:
        """Select agent with least load"""
        available_agents = [
            agent for agent in self.agents
            if self.agent_errors[agent.name] < 3  # Skip agents with many errors
        ]
        
        if not available_agents:
            return None
        
        # Select agent with minimum load
        return min(available_agents, key=lambda a: self.agent_loads[a.name])
    
    async def execute_with_balancing(self, task: str) -> Any:
        agent = self.select_agent()
        if not agent:
            raise Exception("No available agents")
        
        self.agent_loads[agent.name] += 1
        try:
            result = await agent.arun(task)
            self.agent_errors[agent.name] = 0  # Reset error count on success
            return result
        except Exception as e:
            self.agent_errors[agent.name] += 1
            raise
        finally:
            self.agent_loads[agent.name] -= 1