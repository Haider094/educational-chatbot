from functools import wraps
from flask_socketio import emit, disconnect
from flask import request
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.token import Token, SessionLocal
from datetime import datetime

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

def verify_token(token):
    """Verify if the provided token exists in the database."""
    if not token:
        return False, "Authentication token is missing"
    
    db: Session = SessionLocal()
    token_record = db.query(Token).filter(Token.token == token).first()
    db.close()
    
    if not token_record:
        return False, "Invalid authentication token"
    
    return True, "Token verified"

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.args.get('token')
        
        if not auth_token and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                auth_token = auth_header.split(' ')[1]

        is_valid, message = verify_token(auth_token)
        if not is_valid:
            emit('error', {
                'status': 401,
                'message': message,
                'type': 'AuthenticationError'
            })
            disconnect()
            return False
        return f(*args, **kwargs)
    return decorated
