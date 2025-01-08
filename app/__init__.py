from flask import Blueprint, request, jsonify, Flask
from app.utils.auth import verify_token
from app.routes.token_routes import token_bp

app = Flask(__name__)

@token_bp.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    token = data.get('token')
    is_valid, message = verify_token(token)
    status_code = 200 if is_valid else 401
    return jsonify({'message': message}), status_code

# Register the token blueprint
app.register_blueprint(token_bp, url_prefix='/api')