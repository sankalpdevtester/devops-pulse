"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./devops_pulse.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Monitoring
    CHECK_INTERVAL_SECONDS: int = 60
    REQUEST_TIMEOUT_SECONDS: int = 10
    MAX_RETRIES: int = 3
    
    # Alerts
    ALERT_EMAIL_ENABLED: bool = False
    ALERT_SLACK_ENABLED: bool = False
    SLACK_WEBHOOK_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
