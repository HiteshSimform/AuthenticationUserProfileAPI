from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


# This Python class defines settings for a web application, including database URLs, secret key, email
# configuration, and Redis settings.
class Settings(BaseSettings):
    DATABASE_TYPE: str = "postgres"
    POSTGRES_DATABASE_URL: str
    SQLITE_DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = True
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_SENDER_ADDRESS: str
    EMAIL_SENDER_PASSWORD: str
    REDIS_BROKER_URL: str
    REDIS_RESULT_BACKEND: str

    class Config:
        env_file = ".env"


settings = Settings()
