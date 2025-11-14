
"""
Configuration settings for the SOaC Framework API
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://soac_user:soac_password@postgres:5432/soac_db"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # JWT
    SECRET_KEY: str = "soac-framework-secret-key-2025-phase2a-development"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS - Support multiple origins for Railway deployment
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: Optional[str] = None
    
    @property
    def cors_origins(self) -> List[str]:
        """Get list of allowed CORS origins"""
        origins = [
            self.FRONTEND_URL,
            "http://localhost:3000",
            "http://localhost:5173",
        ]
        
        # Add backend URL if provided (for Railway)
        if self.BACKEND_URL:
            origins.append(self.BACKEND_URL)
        
        # In production, parse additional origins from env
        additional_origins = os.getenv("ADDITIONAL_CORS_ORIGINS", "")
        if additional_origins:
            origins.extend([o.strip() for o in additional_origins.split(",")])
        
        return list(set(origins))  # Remove duplicates
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_SQL_QUERIES: bool = False
    
    # Security
    RATE_LIMIT: int = 100  # Requests per minute per IP
    ENABLE_REQUEST_LOGGING: bool = True
    REQUEST_TIMEOUT: int = 60  # seconds
    
    # Feature Flags
    ENABLE_PLAYBOOK_EXECUTION: bool = True
    ENABLE_AUTOMATED_RESPONSE: bool = True
    ENABLE_THREAT_INTELLIGENCE: bool = True
    
    # Event Collection (Phase 3A)
    MOCK_MODE: bool = True
    ENABLE_BACKGROUND_COLLECTION: bool = True
    EVENT_COLLECTION_INTERVAL: int = 300  # seconds (5 minutes)
    
    # Device Integration (Optional - can be configured via UI)
    PALOALTO_API_URL: Optional[str] = None
    PALOALTO_API_KEY: Optional[str] = None
    PALOALTO_VERIFY_SSL: bool = True
    
    ENTRAID_TENANT_ID: Optional[str] = None
    ENTRAID_CLIENT_ID: Optional[str] = None
    ENTRAID_CLIENT_SECRET: Optional[str] = None
    ENTRAID_GRAPH_API_URL: str = "https://graph.microsoft.com/v1.0"
    
    SIEM_TYPE: Optional[str] = None  # splunk, elastic
    SIEM_API_URL: Optional[str] = None
    SIEM_USERNAME: Optional[str] = None
    SIEM_PASSWORD: Optional[str] = None
    SIEM_VERIFY_SSL: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
