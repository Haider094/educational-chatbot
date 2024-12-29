from datetime import datetime, timedelta
from collections import defaultdict
import threading

class RateLimiter:
    def __init__(self, max_requests=60, time_window=60):  # 60 requests per minute by default
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, user_id: str) -> bool:
        with self.lock:
            current_time = datetime.now()
            # Remove old requests
            self.requests[user_id] = [
                req_time for req_time in self.requests[user_id]
                if current_time - req_time < timedelta(seconds=self.time_window)
            ]
            
            # Check if user has exceeded rate limit
            if len(self.requests[user_id]) >= self.max_requests:
                return False
            
            # Add new request
            self.requests[user_id].append(current_time)
            return True

rate_limiter = RateLimiter()
