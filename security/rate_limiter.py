
# security/rate_limiter.py
from collections import defaultdict
import time#, typing
from typing import Dict, Tuple, Optional, List

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, Optional[float]]:
        """Check if request is allowed"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            # Calculate wait time
            oldest_request = min(self.requests[client_id])
            wait_time = 60 - (now - oldest_request)
            return False, wait_time
        
        self.requests[client_id].append(now)
        return True, None