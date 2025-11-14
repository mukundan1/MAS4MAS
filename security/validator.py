# security/validator.py
from typing import List, Dict, Any
import re

class SecurityValidator:
    def __init__(self, config: ProductionConfig):
        self.config = config
        self.blocked_patterns = [
            r"(api_key|password|secret)",
            r"(eval|exec|__import__)",
            r"(system|popen|subprocess)"
        ]
    
    def validate_input(self, input_text: str) -> bool:
        """Validate user input for security threats"""
        # Check for injection attempts
        for pattern in self.blocked_patterns:
            if re.search(pattern, input_text, re.IGNORECASE):
                return False
        
        # Check input length
        if len(input_text) > 10000:  # 10KB limit
            return False
        
        return True
    
    def sanitize_output(self, output: str) -> str:
        """Remove sensitive information from output"""
        # Remove potential secrets
        output = re.sub(r'(sk-|api_key=)[a-zA-Z0-9]+', '[REDACTED]', output)
        return output