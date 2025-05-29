from config.config import settings
from db.base import Base
from db.sessions import postgres_engine, sqlite_engine


def get_active_engine():
    """
    The function `get_active_engine` returns either a PostgreSQL engine or a SQLite engine based on the
    value of `settings.DATABASE_TYPE`.
    :return: The function `get_active_engine()` is returning either the `postgres_engine` or
    `sqlite_engine` based on the condition `settings.DATABASE_TYPE == "postgres"`.
    """
    return postgres_engine if settings.DATABASE_TYPE == "postgres" else sqlite_engine


def create_all_tables():
    """
    The function `create_all_tables` creates all tables defined in the metadata using the active engine.
    """
    engine = get_active_engine()
    Base.metadata.create_all(bind=engine)
