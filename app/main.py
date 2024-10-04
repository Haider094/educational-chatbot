from flask import Flask
from flask_socketio import SocketIO
from .handlers.socket_events import register_socket_events

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=60, ping_interval=25)  

# Register SocketIO events
register_socket_events(socketio)

# if __name__ == '__main__':
    # Set debug to True for better error output during development
    # socketio.run(app, host='0.0.0.0', port=8080, debug=False)
