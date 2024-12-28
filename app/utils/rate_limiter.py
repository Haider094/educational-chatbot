from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=100, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = defaultdict(list)

    def is_allowed(self, token):
        current_time = time.time()
        
        # Remove old requests
        self.requests[token] = [
            req_time for req_time in self.requests[token]
            if current_time - req_time < self.time_window
        ]

        # Check if under limit
        if len(self.requests[token]) < self.max_requests:
            self.requests[token].append(current_time)
            return True
        return False

rate_limiter = RateLimiter()

def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not rate_limiter.is_allowed(token):
            return jsonify({
                'status': 429,
                'message': 'Too many requests. Please try again later.',
                'type': 'RateLimitError'
            }), 429
            
        return f(*args, **kwargs)
    return decorated
