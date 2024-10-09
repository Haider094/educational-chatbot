from flask_socketio import emit
from app.models.falcon_model import generate_response
import json
from flask import request
import logging

# Create a logger instance
logger = logging.getLogger()

# Dictionary to store user sessions
user_sessions = {}

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect(user_id):
        user_id = request.args.get('user_id')  # Get user ID from the connection request
        logger.info('User connected: %s', user_id)  # Log user connection

        # Initialize a session for the user if not already present
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                "history": [],  # You can keep this if needed
                # You can add more session data if needed
            }

        # Send response back when connection is established
        emit('message', {'data': 'Connected to EduBot!'})

    @socketio.on('message')
    def handle_message(data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                emit('response', {'data': 'Invalid data format. Expected JSON.'})
                return

        user_id = data.get('user_id')
        user_input = data.get('message')

        # Log the message received from the user
        logger.info('Message received from user %s: %s', user_id, user_input)

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
            # Call the generate_response function and pass the user ID
            response = generate_response(user_input)

        # Log the response sent to the user
        logger.info('Response sent to user %s: %s', user_id, response)

        # Send response back to the specific user
        emit('response', {'user_id': user_id, 'data': response})

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = request.sid  # Assuming `request.sid` identifies the user
        logger.info('User disconnected: %s', user_id)  # Log user disconnection

        # You may want to clean up user session here if needed
        if user_id in user_sessions:
            del user_sessions[user_id]  # Clean up user session data

        # Send response back when the user disconnects
        emit('response', {'data': 'User disconnected from EduBot!'})
