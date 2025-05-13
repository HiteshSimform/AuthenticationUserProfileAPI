from db.sessions import sqlite_engine, postgres_engine
from db.base import Base
from config.config import settings


def get_active_engine():
    return postgres_engine if settings.DATABASE_TYPE == "postgres" else sqlite_engine


def create_all_tables():
    engine = get_active_engine()
    Base.metadata.create_all(bind=engine)
