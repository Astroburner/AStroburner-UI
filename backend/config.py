from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"
    OUTPUTS_DIR: Path = BASE_DIR / "outputs"
    DB_PATH: Path = BASE_DIR / "ai_studio.db"
    
    # API
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    
    # Generation Defaults
    DEFAULT_WIDTH: int = 512
    DEFAULT_HEIGHT: int = 512
    DEFAULT_STEPS: int = 30
    DEFAULT_GUIDANCE: float = 7.5
    MAX_BATCH_SIZE: int = 4
    
    # GPU
    DEVICE: str = "cuda"  # cuda, cpu, or mps (for Mac)
    ENABLE_XFORMERS: bool = True
    ENABLE_ATTENTION_SLICING: bool = True
    VAE_SLICING: bool = True
    
    # Models
    DEFAULT_MODEL: str = "stabilityai/stable-diffusion-xl-base-1.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories
        self.MODELS_DIR.mkdir(exist_ok=True, parents=True)
        self.OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)

settings = Settings()
