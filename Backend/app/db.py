'''
Handles the database connection.

Uses SQLite by default (airiq.db file).

Defines engine, SessionLocal, and Base.

The function get_db() safely opens and closes DB sessions for every request.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

SQLITE_PATH = os.getenv("SQLITE_PATH", "./airiq.db")
DATABASE_URL = f"sqlite:///{SQLITE_PATH}"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
