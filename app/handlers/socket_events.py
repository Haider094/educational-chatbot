from flask_socketio import emit, disconnect
from app.models.falcon_model import generate_response
from app.models.classifier import classify_prompt  # Import the classification function
from app.utils.auth import require_token, verify_token
import json
from flask import request
import logging
from app.utils.rate_limiter import rate_limiter

# Create a logger instance
logger = logging.getLogger()

# Dictionary to store user sessions and their connection IDs
user_sessions = {}
connection_to_user = {}  # New dictionary to map connection IDs to user_ids

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        auth_token = request.args.get('token')
        user_id = request.args.get('user_id')

        # Verify token first
        if not auth_token:
            emit('error', {
                'status': 401,
                'message': 'Authentication token is missing',
                'type': 'AuthenticationError'
            })
            disconnect()
            return False

        is_valid, token_id = verify_token(auth_token)
        if not is_valid:
            emit('error', {
                'status': 401,
                'message': f'Invalid or expired token: {token_id}',
                'type': 'AuthenticationError'
            })
            disconnect()
            return False
        
        if not user_id:
            emit('error', {
                'status': 400,
                'message': 'User ID is required for connection',
                'type': 'ValidationError'
            })
            disconnect()
            return False

        connection_id = request.sid
        connection_to_user[connection_id] = user_id
        
        logger.info('User connected: %s with connection ID: %s', user_id, connection_id)

        if user_id not in user_sessions:
            user_sessions[user_id] = {
                "history": [],
                "connection_id": connection_id
            }

        emit('connected', {
            'status': 200,
            'message': 'Successfully connected to EduBot!',
            'user_id': user_id,
            'connection_id': connection_id
        })

    @socketio.on('message')
    def handle_message(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)

            message_user_id = data.get('user_id')
            user_input = data.get('message')
            connection_id = request.sid
            original_user_id = connection_to_user.get(connection_id)

            if not message_user_id or not user_input:
                emit('error', {
                    'status': 400,
                    'message': 'Both user_id and message are required in the request',
                    'type': 'ValidationError',
                    'details': {
                        'user_id': 'Missing' if not message_user_id else 'Present',
                        'message': 'Missing' if not user_input else 'Present'
                    }
                })
                return

            if message_user_id != original_user_id:
                emit('error', {
                    'status': 403,
                    'message': 'User ID mismatch detected',
                    'type': 'AuthorizationError',
                    'details': {
                        'provided_user_id': message_user_id,
                        'expected_user_id': original_user_id,
                        'reason': 'User ID must match the ID used during connection'
                    }
                })
                return

            # Check rate limit
            if not rate_limiter.is_allowed(message_user_id):
                emit('error', {
                    'status': 429,
                    'message': 'Rate limit exceeded. Please try again later.',
                    'type': 'RateLimitError'
                })
                return

            # Log the message received from the user
            logger.info('Message received from user %s: %s', message_user_id, user_input)

            # Predefined responses
            predefined_responses = {
                "who are you?": "I am EduBot, your educational assistant.",
                "what are you?": "I am an AI-powered educational assistant here to help with your learning needs.",
                "what can you do?": "I can answer educational questions on a wide range of topics.",
                "what is your name?": "My name is EduBot."
            }

            # Check for predefined responses first
            if user_input.lower() in predefined_responses:
                response = predefined_responses[user_input.lower()]
            else:
                # Classify the user input as educational or non-educational
                classification = classify_prompt(user_input)

                if classification == "educational":
                    # Call the generate_response function to handle educational queries
                    response = generate_response(user_input)
                else:
                    # If the input is non-educational, send an appropriate response
                    response = "Apologies! I can only answer to the educational queries. Please ask me something related to education."

            # Log the response sent to the user
            logger.info('Response sent to user %s: %s', message_user_id, response)

            # Update response format
            emit('response', {
                'status': 200,
                'user_id': message_user_id,
                'data': response,
                'message_type': 'chat_response'
            })

        except json.JSONDecodeError:
            emit('error', {
                'status': 400,
                'message': 'Invalid JSON format',
                'type': 'ValidationError'
            })
        except Exception as e:
            logger.error('Error processing message: %s', str(e), exc_info=True)  # Added exc_info for better logging
            emit('error', {
                'status': 500,
                'message': 'Internal server error',
                'type': 'ServerError',
                'error': str(e) if not isinstance(e, json.JSONDecodeError) else 'Invalid JSON format'
            })

    @socketio.on('disconnect')
    def handle_disconnect():
        connection_id = request.sid
        user_id = connection_to_user.get(connection_id)
        
        # Clean up both dictionaries
        if user_id in user_sessions:
            del user_sessions[user_id]
        if connection_id in connection_to_user:
            del connection_to_user[connection_id]

        logger.info('User disconnected: %s', user_id)
        
        emit('disconnected', {
            'status': 200,
            'message': 'Successfully disconnected from EduBot',
            'user_id': user_id
        })

