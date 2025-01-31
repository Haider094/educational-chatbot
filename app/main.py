import logging
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from .handlers.socket_events import register_socket_events
from . import app  # Import the app instance

# Enable CORS for the Flask app
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://api.educhatgpt.softgeeksdigital.com",
            "https://educhatgpt.softgeeksdigital.com"  # Add the client's origin
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})

# Initialize SocketIO with expanded CORS settings
socketio = SocketIO(
    app,
    cors_allowed_origins=[
        "https://api.educhatgpt.softgeeksdigital.com",
        "https://educhatgpt.softgeeksdigital.com"  # Add the client's origin
    ],
    ping_timeout=60,
    ping_interval=25,
    logger=True,
    engineio_logger=True
)

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set logging level
logger = logging.getLogger()

# Register SocketIO events
register_socket_events(socketio)

if __name__ == '__main__':
    # Set debug to True for better error output during development
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)