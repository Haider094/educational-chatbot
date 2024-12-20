from functools import wraps
from flask_socketio import disconnect
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

def verify_token(token):
    """Verify if the provided token matches the API token."""
    return token and token == API_TOKEN

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = None
        
        # Check token in query parameters
        auth_token = request.args.get('token')
        
        # Check token in headers (for REST endpoints if needed)
        if not auth_token and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                auth_token = auth_header.split(' ')[1]

        if not verify_token(auth_token):
            disconnect()
            return False
        return f(*args, **kwargs)
    return decorated
