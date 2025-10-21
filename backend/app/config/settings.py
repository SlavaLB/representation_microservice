import os

from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()

DB_CONNECTOR = os.environ.get("DB_CONNECTOR")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")


class Settings(BaseSettings):

    database_url: str = f"{DB_CONNECTOR}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    base_url_math_model: str = "http://math_model:8002"
    base_url_plc_model: str = "http://plc_service:8003"

    class Config:
        extra = "allow"


settings = Settings()
