from contextlib import contextmanager
import os

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from .exception import InvalidDatabaseConfiguration

if DB_DRIVER := os.getenv("DB_DRIVER", "sqlite"):
    CONNECTION_STRING = "sqlite:///sample.db"
else:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    if not DB_USER or not DB_PASSWORD or not DB_HOST or not DB_PORT or not DB_NAME:
        raise InvalidDatabaseConfiguration()

    CONNECTION_STRING = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
engine = create_engine(
        CONNECTION_STRING, 
        pool_size=300,           # Increased number of pooled connections
        max_overflow=200,        # Additional connections to handle spikes
        pool_timeout=30,         # Wait up to 30 seconds for a connection
        pool_recycle=1800,       # Recycle connections every 30 minutes
        pool_pre_ping=True       # Enable pre-ping to check the connection before use
    )
DBSession = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=False)

@contextmanager
def SessionManager():
    session = DBSession()
    try:
        yield session
    finally:
        session.close()