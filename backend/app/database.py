from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

load_dotenv()

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
