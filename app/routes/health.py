
from flask import Blueprint, jsonify
from app.config.database import engine

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'Service is running normally'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'message': str(e)
        }), 500