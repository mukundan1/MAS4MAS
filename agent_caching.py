# cache/agent_cache.py
from functools import lru_cache
import hashlib
import redis
import json
from typing import Optional, Any

class AgentCache:
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = redis.from_url(redis_url) if redis_url else None
        self.local_cache = {}
    
    def cache_key(self, agent_name: str, input_text: str) -> str:
        """Generate cache key"""
        content = f"{agent_name}:{input_text}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def get(self, agent_name: str, input_text: str) -> Optional[Any]:
        """Get cached result"""
        key = self.cache_key(agent_name, input_text)
        
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Try Redis
        if self.redis_client:
            cached = self.redis_client.get(key)
            if cached:
                return json.loads(cached)
        
        return None
    
    async def set(self, agent_name: str, input_text: str, result: Any, ttl: int = 3600):
        """Cache result"""
        key = self.cache_key(agent_name, input_text)
        
        # Local cache
        self.local_cache[key] = result
        
        # Redis cache
        if self.redis_client:
            self.redis_client.setex(key, ttl, json.dumps(result))