import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional


SECRET_KEY = "your-secret-key-change-this-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Simple in-memory token storage (use database in production)
active_tokens = {}


class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create simple access token"""
        token = str(uuid.uuid4())
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Store token with expiration and user data
        active_tokens[token] = {
            "data": data,
            "expires": expire
        }
        
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify access token"""
        if token not in active_tokens:
            return None
            
        token_data = active_tokens[token]
        
        # Check if token has expired
        if datetime.now(timezone.utc) > token_data["expires"]:
            del active_tokens[token]  # Remove expired token
            return None
            
        return token_data["data"]


# Default users for demo
DEFAULT_USERS = [
    {
        "email": "admin@example.com",
        "password": "admin123",
        "name": "Admin User"
    },
    {
        "email": "support@example.com", 
        "password": "support123",
        "name": "Support Agent"
    },
    {
        "email": "user@example.com",
        "password": "user123", 
        "name": "Test User"
    }
]