from flask_socketio import emit, disconnect
from app.models.falcon_model import generate_response
from app.models.classifier import classify_prompt
from app.utils.token import validate_token
import json
from flask import request
import logging

# Create a logger instance
logger = logging.getLogger()

# Dictionary to store user sessions
user_sessions = {}

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        try:
            token = request.args.get('token')
            user_id = request.args.get('user_id')

            logger.info(f"Connection attempt - Token: {token}, User ID: {user_id}, Args: {request.args}")
            
            if not token:
                logger.warning('No token provided in request args')
                return False

            decoded_token = validate_token(token)
            logger.info(f"Decoded token: {decoded_token}")

            if not decoded_token:
                logger.warning('Invalid token')
                return False

            logger.info('User connected successfully: %s', user_id)
            
            if user_id not in user_sessions:
                user_sessions[user_id] = {
                    "history": [],
                }

            emit('message', {'data': 'Connected to EduBot!'})
            return True
            
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    @socketio.on('message')
    def handle_message(data):
        try:
            logger.info(f"Received message: {data}")
            
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    emit('error', {'data': 'Invalid JSON format'})
                    return

            user_id = data.get('user_id')
            user_input = data.get('message')

            if not user_id or not user_input:
                emit('error', {'data': 'Missing user_id or message'})
                return

            logger.info(f'Message from user {user_id}: {user_input}')

            # Predefined responses
            predefined_responses = {
                "who are you?": "I am EduBot, your educational assistant.",
                "what are you?": "I am an AI-powered educational assistant here to help with your learning needs.",
                "what can you do?": "I can answer educational questions on a wide range of topics.",
                "what is your name?": "My name is EduBot."
            }

            # Process the message and send response
            if user_input.lower() in predefined_responses:
                response = predefined_responses[user_input.lower()]
            else:
                classification = classify_prompt(user_input)
                if classification == "educational":
                    response = generate_response(user_input)
                else:
                    response = "Please ask an educational question."

            logger.info(f'Response to user {user_id}: {response}')
            emit('response', {'user_id': user_id, 'data': response})

        except Exception as e:
            logger.error(f"Message handling error: {str(e)}")
            emit('error', {'data': 'Internal server error'})

    @socketio.on('disconnect')
    def handle_disconnect():
        try:
            user_id = request.sid
            logger.info(f'User disconnected: {user_id}')
            if user_id in user_sessions:
                del user_sessions[user_id]
        except Exception as e:
            logger.error(f"Disconnect error: {str(e)}")

