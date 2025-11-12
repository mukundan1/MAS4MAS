# health/health_check.py
from typing import Dict, List
import asyncio

class HealthChecker:
    def __init__(self, agents: List[Agent], dependencies: Dict[str, Any]):
        self.agents = agents
        self.dependencies = dependencies
    
    async def check_health(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health_status = {
            "status": "healthy",
            "checks": {}
        }
        
        # Check agents
        for agent in self.agents:
            try:
                await agent.arun("test")
                health_status["checks"][f"agent_{agent.name}"] = "healthy"
            except Exception as e:
                health_status["status"] = "unhealthy"
                health_status["checks"][f"agent_{agent.name}"] = str(e)
        
        # Check dependencies
        for name, dependency in self.dependencies.items():
            try:
                await dependency.ping()
                health_status["checks"][name] = "healthy"
            except Exception as e:
                health_status["status"] = "unhealthy"
                health_status["checks"][name] = str(e)
        
        return health_status