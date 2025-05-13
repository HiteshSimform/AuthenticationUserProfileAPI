from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_TYPE: str = "postgres"
    POSTGRES_DATABASE_URL: str
    SQLITE_DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
