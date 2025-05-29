from config.config import settings
from db.base import Base
from db.sessions import postgres_engine, sqlite_engine


def get_active_engine():
    return postgres_engine if settings.DATABASE_TYPE == "postgres" else sqlite_engine


def create_all_tables():
    engine = get_active_engine()
    Base.metadata.create_all(bind=engine)
