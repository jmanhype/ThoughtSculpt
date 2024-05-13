# config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    database_url: str = "postgresql://username:password@localhost/thoughtsculpt"
    openai_api_base: str = "https://api.openai.com/v1"
    anthropic_api_base: str = "https://api.anthropic.com/v1"
    groq_api_base: str = "https://api.groq.com/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()