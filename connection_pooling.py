# utils/connection_pool.py
import asyncio
from typing import Dict, Any
import aiohttp

class ConnectionPool:
    def __init__(self, max_connections: int = 100):
        self.connector = aiohttp.TCPConnector(
            limit=max_connections,
            limit_per_host=30,
            ttl_dns_cache=300
        )
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=self.connector)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        async with self.session.request(method, url, **kwargs) as response:
            return await response.json()