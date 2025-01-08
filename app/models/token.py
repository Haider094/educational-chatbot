from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'
    token = Column(String, primary_key=True)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))  # Set default expiration to 30 days

DATABASE_URL = "sqlite:///./tokens.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def create_token(token_str):
    db: Session = SessionLocal()
    new_token = Token(token=token_str)
    db.add(new_token)
    db.commit()
    db.close()
