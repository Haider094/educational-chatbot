import logging
from flask import Flask
from flask_socketio import SocketIO
from app.handlers.socket_events import register_socket_events
from app.routes.token_routes import token_bp
from app.routes.health import health_bp
from app.models.token_model import token_store
import secrets

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=60, ping_interval=25)  

# Set up logging
logging.basicConfig(level=logging.INFO)  # Set logging level
logger = logging.getLogger()

# Register the token management blueprint
app.register_blueprint(token_bp, url_prefix='/api')
app.register_blueprint(health_bp)

# Create initial token if no tokens exist
@app.before_first_request
def create_initial_token():
    with app.app_context():
        tokens = token_store.list_tokens()
        if not tokens:
            initial_token = token_store.create_token(
                description="Initial admin token",
                expires_in="365d"
            )
            print(f"\n\nInitial Admin Token Created: {initial_token}\n"
                  f"Please save this token securely!\n\n")

# Register SocketIO events
register_socket_events(socketio)

if __name__ == '__main__':
    # Set debug to True for better error output during development
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
