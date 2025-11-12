# logging_config.py
import logging
import json
from pythonjsonlogger import jsonlogger

def setup_production_logging():
    # JSON formatter for structured logs
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logHandler.setFormatter(formatter)
    
    # Configure root logger
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(logHandler)
    
    # Configure specific loggers
    logging.getLogger('praisonaiagents').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)