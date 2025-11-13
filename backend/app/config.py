
"""
Configuration settings for the SOaC Framework API
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://soac_user:soac_password@postgres:5432/soac_db"
    
    # JWT
    SECRET_KEY: str = "soac-framework-secret-key-2025-phase2a-development"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
