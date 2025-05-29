from typing import Generator

from config.config import settings
from db.sessions import PostgresSessionLocal, SQLiteSessionLocal
from sqlalchemy.orm import Session


def get_db_session() -> Generator[Session, None, None]:
    """
    This function returns a database session using either a Postgres or SQLite connection based on the
    settings.
    """
    SessionLocal = PostgresSessionLocal if settings.DATABASE_TYPE == "postgres" else SQLiteSessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
