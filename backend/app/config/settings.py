from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # database_url: str = "postgresql+asyncpg://user:password@db:5432/mydatabase"

    class Config:
        extra = "allow"


settings = Settings()
