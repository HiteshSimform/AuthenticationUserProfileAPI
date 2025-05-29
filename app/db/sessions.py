from config.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# This code snippet is setting up database connections using SQLAlchemy in Python. Here's a breakdown
# of what each part does:
postgres_engine = create_engine(
    settings.POSTGRES_DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
)

sqlite_engine = create_engine(
    settings.SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.SQLALCHEMY_ECHO,
)

PostgresSessionLocal = sessionmaker(bind=postgres_engine, autoflush=False, autocommit=False)
SQLiteSessionLocal = sessionmaker(bind=sqlite_engine, autoflush=False, autocommit=False)
