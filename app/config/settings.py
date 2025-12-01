from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    STABILITYAI_API_KEY: str = os.getenv("STABILITYAI_API_KEY", "")
    REPLICATE_API_KEY: str = os.getenv("REPLICATE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    IMAGEKIT_URL_ENDPOINT: str = os.getenv("IMAGEKIT_URL_ENDPOINT", "")
    IMAGEKIT_PRIVATE_TOKEN: str = os.getenv("IMAGEKIT_PRIVATE_TOKEN", "")
    IMAGEKIT_PUBLIC_TOKEN: str = os.getenv("IMAGEKIT_PUBLIC_TOKEN", "")
    HUGGING_FACE_TOKEN: str = os.getenv("HUGGING_FACE_TOKEN", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # class Config:
    #     env_file = ".env"
        
settings = Settings()