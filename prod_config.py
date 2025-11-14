# config/production.py
import os
from typing import Optional

class ProductionConfig:
    # API Keys (from environment)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Performance
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "300"))
    MAX_CONCURRENT_AGENTS = int(os.getenv("MAX_CONCURRENT_AGENTS", "10"))
    
    # Security
    ENABLE_CONTENT_FILTERING = os.getenv("ENABLE_CONTENT_FILTERING", "true").lower() == "true"
    ALLOWED_TOOLS = os.getenv("ALLOWED_TOOLS", "").split(",")
    
    # Monitoring
    TELEMETRY_ENABLED = os.getenv("TELEMETRY_ENABLED", "true").lower() == "true"
    TELEMETRY_ENDPOINT = os.getenv("TELEMETRY_ENDPOINT")