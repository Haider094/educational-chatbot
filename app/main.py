import logging
from flask import Flask
from flask_socketio import SocketIO
from .handlers.socket_events import register_socket_events
from . import app  # Import the app instance

# Initialize Flask and SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=60, ping_interval=25)  

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set logging level
logger = logging.getLogger()

# Register SocketIO events
register_socket_events(socketio)

if __name__ == '__main__':
    # Set debug to True for better error output during development
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
