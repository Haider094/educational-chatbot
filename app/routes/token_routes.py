from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.models.token import Token, SessionLocal
from datetime import datetime, timedelta

token_bp = Blueprint('token', __name__)

@token_bp.route('/token', methods=['POST'])
def create_token():
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400
    
    db: Session = SessionLocal()
    new_token = Token(token=token)
    db.add(new_token)
    db.commit()
    db.close()
    
    return jsonify({"message": "Token created successfully"}), 201

@token_bp.route('/token/<token>', methods=['DELETE'])
def delete_token(token):
    db: Session = SessionLocal()
    token_to_delete = db.query(Token).filter(Token.token == token).first()
    if not token_to_delete:
        db.close()
        return jsonify({"error": "Token not found"}), 404
    
    db.delete(token_to_delete)
    db.commit()
    db.close()
    
    return jsonify({"message": "Token deleted successfully"}), 200

@token_bp.route('/token/<token>', methods=['GET'])
def check_token(token):
    db: Session = SessionLocal()
    token_exists = db.query(Token).filter(Token.token == token).first()
    db.close()
    
    if not token_exists:
        return jsonify({"error": "Token not found"}), 404
    
    return jsonify({"message": "Token is valid"}), 200

@token_bp.route('/tokens/active', methods=['GET'])
def get_active_tokens():
    db: Session = SessionLocal()
    active_tokens_count = db.query(Token).filter(Token.expires_at > datetime.utcnow()).count()
    db.close()
    
    return jsonify({"active_tokens_count": active_tokens_count}), 200
