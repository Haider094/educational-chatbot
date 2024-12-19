import logging
from flask import Flask
from flask_socketio import SocketIO
from .handlers.socket_events import register_socket_events
import os

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=60, ping_interval=25)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

# Load secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Register SocketIO events
register_socket_events(socketio)

# if __name__ == '__main__':
    # Set debug to True for better error output during development
    # socketio.run(app, host='0.0.0.0', port=8080, debug=False)
