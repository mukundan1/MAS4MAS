# tests/utils.py
import asyncio
import time
from typing import Any, Callable, Optional
from contextlib import contextmanager

class TestMetrics:
    def __init__(self):
        self.execution_times = []
        self.token_usage = []
        self.error_count = 0
    
    def record_execution(self, duration: float, tokens: int = 0):
        self.execution_times.append(duration)
        self.token_usage.append(tokens)
    
    def record_error(self):
        self.error_count += 1
    
    def get_stats(self):
        return {
            "avg_execution_time": sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0,
            "total_tokens": sum(self.token_usage),
            "error_rate": self.error_count / (len(self.execution_times) + self.error_count) if self.execution_times else 0
        }

@contextmanager
def measure_performance():
    """Context manager to measure execution time"""
    start = time.time()
    yield
    duration = time.time() - start
    return duration

def async_test(coro):
    """Decorator to run async tests"""
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper