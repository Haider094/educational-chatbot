import secrets
import re
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy import Column, String, DateTime
from app.config.database import Base, SessionLocal, engine
from contextlib import contextmanager

class Token(Base):
    __tablename__ = 'tokens'
    
    token = Column(String(64), primary_key=True)
    description = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class TokenStore:
    def _parse_time_period(self, time_period: str) -> timedelta:
        """Convert time period string to timedelta (e.g., '2d', '1m', '1y')"""
        pattern = re.compile(r'^(\d+)([dmy])$')
        match = pattern.match(time_period.lower())
        if not match:
            raise ValueError("Invalid time period format. Use format: <number><d|m|y> (e.g., '2d', '1m', '1y')")
        
        amount, unit = match.groups()
        amount = int(amount)
        
        if unit == 'd':
            return timedelta(days=amount)
        elif unit == 'm':
            return timedelta(days=amount * 30)
        elif unit == 'y':
            return timedelta(days=amount * 365)
        
        raise ValueError("Invalid time unit. Use 'd' for days, 'm' for months, or 'y' for years")

    def create_token(self, description: str, expires_in: str) -> str:
        try:
            expiration_delta = self._parse_time_period(expires_in)
        except ValueError as e:
            raise ValueError(f"Invalid expiration format: {str(e)}")

        token = secrets.token_hex(32)
        expiration_date = datetime.utcnow() + expiration_delta
        
        with get_session() as session:
            token_obj = Token(
                token=token,
                description=description,
                expires_at=expiration_date
            )
            session.add(token_obj)
        
        return token

    def validate_token(self, token: str) -> bool:
        with get_session() as session:
            token_obj = session.query(Token).filter_by(token=token).first()
            if not token_obj:
                return False
            if datetime.utcnow() > token_obj.expires_at:
                self.delete_token(token)
                return False
            return True

    def delete_token(self, token: str) -> bool:
        with get_session() as session:
            result = session.query(Token).filter_by(token=token).delete()
            return bool(result)

    def get_token_info(self, token: str) -> Optional[Dict]:
        with get_session() as session:
            token_obj = session.query(Token).filter_by(token=token).first()
            if token_obj:
                return {
                    'token': token_obj.token,
                    'description': token_obj.description,
                    'created_at': token_obj.created_at.isoformat(),
                    'expires_at': token_obj.expires_at.isoformat()
                }
            return None

    def list_tokens(self) -> Dict[str, Dict]:
        with get_session() as session:
            tokens = session.query(Token).all()
            return {
                token_obj.token: {
                    'description': token_obj.description,
                    'created_at': token_obj.created_at.isoformat(),
                    'expires_at': token_obj.expires_at.isoformat()
                } for token_obj in tokens
            }

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Global token store instance
token_store = TokenStore()
