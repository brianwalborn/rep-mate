from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

def _load_env_file() -> None:
    # In Docker we usually get env vars directly; avoid failing startup if .env can't be read.
    if os.getenv("DATABASE_URL"):
        return

    try:
        load_dotenv(dotenv_path=".env")
    except OSError:
        pass

_load_env_file()

DATABASE_URL = os.getenv("DATABASE_URL")

pool_recycle_seconds = int(os.getenv("DB_POOL_RECYCLE_SECONDS", "1800"))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=pool_recycle_seconds,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
