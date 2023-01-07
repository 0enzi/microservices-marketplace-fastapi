import secrets
from pydantic import BaseSettings

# Security
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "IeloroSearchAPI"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    

    class Config:
        env_file = ".env"


settings = Settings()
