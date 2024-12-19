import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_token(user_id):
    secret_key = os.getenv('SECRET_KEY')
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validate_token(token):
    try:
        secret_key = os.getenv('SECRET_KEY')
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return None
