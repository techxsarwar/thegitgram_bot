from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    telegram_id = Column(Integer, primary_key=True)
    github_token = Column(String)  # We'll store it as a string for now as per instructions
    username = Column(String)

# Database URL - SQLite for local testing
DATABASE_URL = "sqlite:///./thegitgram.db"

engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)
