from sqlalchemy import Column, String, BigInteger, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    github_token = Column(String)
    username = Column(String)

import os

# Database URL - Fallback to SQLite if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./thegitgram.db")

# 1. Fix the 'postgres://' vs 'postgresql://' issue for SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Add 'pool_pre_ping' and 'pool_recycle' for pooling (PgBouncer friendly)
# Note: SQLite doesn't support pooling in the same way, but it's safe to keep these args
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True, 
    pool_recycle=300
)

def init_db():
    Base.metadata.create_all(bind=engine)
