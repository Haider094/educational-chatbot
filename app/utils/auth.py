import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
from .token_blacklist import token_blacklist

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

def generate_token(user_id, expires_in=30):
    """Generate a JWT token."""
    expiration = datetime.utcnow() + timedelta(days=expires_in)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    """Verify the provided JWT token."""
    if token_blacklist.is_token_blacklisted(token):
        return False, "Token has been revoked"
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True, payload['user_id']
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.args.get('token')
        
        if not auth_token and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                auth_token = auth_header.split(' ')[1]

        is_valid, user_id_or_message = verify_token(auth_token)
        if not is_valid:
            return jsonify({'error': user_id_or_message}), 401
        return f(*args, **kwargs)
    return decorated
