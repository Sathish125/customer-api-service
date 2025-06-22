import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/customers.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Following Singleton pattern using lru_cache with maxsize=1
@lru_cache(maxsize=1)
def get_db_session():
    return SessionLocal()

def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from models.db_models import Customer
    Base.metadata.create_all(bind=engine)
