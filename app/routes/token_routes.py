from flask import Blueprint, request, jsonify
from app.utils.auth import generate_token, verify_token, require_token
from app.utils.token_blacklist import token_blacklist
import logging

token_bp = Blueprint('token', __name__)  # Define the blueprint first
logger = logging.getLogger(__name__)

@token_bp.route('/token', methods=['POST'])
def create_token():
    token_id = request.json.get('token_id')  # Changed from user_id to token_id
    expires_in = request.json.get('expires_in', 30)  # Default expiration is 30 days
    time_unit = request.json.get('time_unit', 'days')  # Default time unit is days

    if not token_id:
        logger.error("Token ID is required")
        return jsonify({"error": "Token ID is required", "status": "error"}), 400

    try:
        token = generate_token(token_id, expires_in, time_unit)
    except ValueError as e:
        logger.error(str(e))
        return jsonify({"error": str(e), "status": "error"}), 400

    logger.info("Token created successfully")
    return jsonify({
        "status": "success",
        "message": "Token created successfully",
        "token": token,
        "expires_in": expires_in,
        "time_unit": time_unit
    }), 201

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
