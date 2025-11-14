# security/key_manager.py
import os
from cryptography.fernet import Fernet
import boto3
from typing import Optional

class SecureKeyManager:
    def __init__(self, use_aws_secrets: bool = False):
        self.use_aws_secrets = use_aws_secrets
        self.fernet = Fernet(os.getenv("ENCRYPTION_KEY", Fernet.generate_key()))
        
        if use_aws_secrets:
            self.secrets_client = boto3.client('secretsmanager')
    
    def get_api_key(self, key_name: str) -> Optional[str]:
        """Securely retrieve API key"""
        if self.use_aws_secrets:
            try:
                response = self.secrets_client.get_secret_value(SecretId=key_name)
                return response['SecretString']
            except Exception as e:
                logger.error(f"Failed to retrieve secret: {e}")
                return None
        else:
            # Get from environment and decrypt
            encrypted = os.getenv(key_name)
            if encrypted:
                return self.fernet.decrypt(encrypted.encode()).decode()
            return None