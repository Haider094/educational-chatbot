from flask import Flask
from app.routes.token_routes import token_bp

app = Flask(__name__)

# Register the token blueprint
app.register_blueprint(token_bp, url_prefix='/api')