from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Application
    APP_NAME: str = "Bookstore AI System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Enable debug mode") 
    
    # API Configuration
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/bookstore_db"
    
    # Vector Database
    VECTOR_DB_TYPE: str = "chromadb"  # chromadb, pinecone
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8001
    
    # Pinecone (alternative)
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # Data Processing
    BATCH_SIZE: int = 1000
    MAX_WORKERS: int = 4
    
    # Caching
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json, text
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour

# Global settings instance
settings = Settings()