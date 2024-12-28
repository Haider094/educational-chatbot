from flask import Blueprint, request, jsonify
from app.models.token_model import token_store
from app.utils.auth import require_token
import os

token_bp = Blueprint('token', __name__)

@token_bp.route('/tokens', methods=['POST'])
@require_token
def create_token():
    data = request.get_json()
    description = data.get('description', 'No description')
    expires_in = data.get('expires_in', '30d')  # Default to 30 days if not specified
    
    try:
        token = token_store.create_token(description, expires_in)
        return jsonify({
            'token': token,
            'description': description,
            'expires_in': expires_in
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@token_bp.route('/tokens', methods=['GET'])
@require_token
def list_tokens():
    tokens = token_store.list_tokens()
    return jsonify({'tokens': tokens}), 200

@token_bp.route('/tokens/<token>', methods=['DELETE'])
@require_token
def delete_token(token):
    if token_store.delete_token(token):
        return jsonify({'message': 'Token deleted successfully'}), 200
    return jsonify({'error': 'Token not found'}), 404

@token_bp.route('/tokens/<token>', methods=['GET'])
@require_token
def get_token_info(token):
    info = token_store.get_token_info(token)
    if info:
        return jsonify(info), 200
    return jsonify({'error': 'Token not found'}), 404
