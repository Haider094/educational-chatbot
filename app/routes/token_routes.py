from flask import Blueprint, request, jsonify
from app.utils.auth import generate_token, verify_token, require_token
from app.utils.token_blacklist import token_blacklist
import logging

token_bp = Blueprint('token', __name__)
logger = logging.getLogger(__name__)

@token_bp.route('/token', methods=['POST'])
def create_token():
    user_id = request.json.get('user_id')
    expires_in = request.json.get('expires_in', 30)  # Default expiration is 30 days

    if not user_id:
        logger.error("User ID is required")
        return jsonify({"error": "User ID is required"}), 400

    token = generate_token(user_id, expires_in)
    logger.info("Token created successfully")
    return jsonify({"token": token}), 201

@token_bp.route('/verify', methods=['POST'])
def verify():
    token = request.json.get('token')
    is_valid, user_id_or_message = verify_token(token)
    status_code = 200 if is_valid else 401
    return jsonify({'message': user_id_or_message}), status_code

@token_bp.route('/revoke', methods=['POST'])
@require_token
def revoke_token():
    token = request.json.get('token')
    token_blacklist.add_token(token)
    return jsonify({'message': 'Token revoked successfully'}), 200

@token_bp.route('/refresh', methods=['POST'])
@require_token
def refresh_token():
    old_token = request.json.get('token')
    is_valid, user_id_or_message = verify_token(old_token)
    if not is_valid:
        return jsonify({'error': user_id_or_message}), 401

    new_token = generate_token(user_id_or_message)
    token_blacklist.add_token(old_token)
    return jsonify({'token': new_token}), 200
