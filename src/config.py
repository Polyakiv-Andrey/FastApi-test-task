import os
from datetime import datetime, timedelta
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):

    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")

    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class Settings(BaseSettings):

    db: DBSettings = DBSettings()


settings = Settings()
