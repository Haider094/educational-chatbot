from functools import wraps
from flask_socketio import emit, disconnect
from flask import request, jsonify
from app.models.token_model import token_store

def verify_token(token):
    """Verify if the provided token exists in token store."""
    if not token:
        return False, "Authentication token is missing"
    if token_store.validate_token(token):
        return True, "Token verified"
    return False, "Invalid authentication token"

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_token = request.args.get('token')
        
        if not auth_token and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                auth_token = auth_header.split(' ')[1]
            else:
                auth_token = auth_header  # Handle token without 'Bearer' prefix

        is_valid, message = verify_token(auth_token)
        if not is_valid:
            # Check if it's a Socket.IO request
            if hasattr(request, 'namespace'):
                emit('error', {
                    'status': 401,
                    'message': message,
                    'type': 'AuthenticationError'
                })
                disconnect()
                return False
            # Return JSON response for REST endpoints
            return jsonify({
                'status': 401,
                'message': message,
                'type': 'AuthenticationError'
            }), 401
            
        return f(*args, **kwargs)
    return decorated
