"""
Configuration settings for the chatbot
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    
    # API Settings
    API_TITLE: str = "Gemma Chatbot API"
    API_VERSION: str = "1.0.0"
    
    # Model Settings
    MODEL_NAME: str = "google/gemma-3-1b-it"
    MODEL_DEVICE: str = "cpu"  # "cuda" for GPU, "cpu" for CPU
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 512
    TOP_P: float = 0.9
    
    # Session Settings
    MAX_HISTORY_LENGTH: int = 10  # Keep last N message pairs
    
    # Model Loading
    USE_OLLAMA: bool = False  # If True, use Ollama instead of HuggingFace
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Optional API Keys (for future use with cloud models)
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()