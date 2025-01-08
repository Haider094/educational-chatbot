from datetime import datetime, timedelta
from collections import defaultdict

class TokenBlacklist:
    def __init__(self):
        self.blacklist = defaultdict(list)

    def add_token(self, token, expires_in=30, time_unit='days'):
        if time_unit == 'minutes':
            expiration = datetime.utcnow() + timedelta(minutes=expires_in)
        elif time_unit == 'hours':
            expiration = datetime.utcnow() + timedelta(hours=expires_in)
        elif time_unit == 'days':
            expiration = datetime.utcnow() + timedelta(days=expires_in)
        elif time_unit == 'months':
            expiration = datetime.utcnow() + timedelta(days=expires_in * 30)
        elif time_unit == 'years':
            expiration = datetime.utcnow() + timedelta(days=expires_in * 365)
        else:
            raise ValueError("Invalid time unit. Use 'minutes', 'hours', 'days', 'months', or 'years'.")

        self.blacklist[token] = expiration

    def is_token_blacklisted(self, token):
        if token in self.blacklist:
            if datetime.utcnow() < self.blacklist[token]:
                return True
            else:
                del self.blacklist[token]
        return False

token_blacklist = TokenBlacklist()
