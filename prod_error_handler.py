# utils/error_handler.py
import logging
import asyncio
from functools import wraps
from typing import Callable, Any
import traceback

logger = logging.getLogger(__name__)

class ProductionError(Exception):
    """Base exception for production errors"""
    pass

def production_error_handler(
    fallback_result: Any = None,
    log_errors: bool = True,
    raise_errors: bool = False
):
    """Decorator for production error handling"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                    logger.debug(traceback.format_exc())
                
                if raise_errors:
                    raise ProductionError(f"Production error in {func.__name__}: {str(e)}")
                
                return fallback_result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                    logger.debug(traceback.format_exc())
                
                if raise_errors:
                    raise ProductionError(f"Production error in {func.__name__}: {str(e)}")
                
                return fallback_result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator