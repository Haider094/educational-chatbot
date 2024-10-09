from flask_socketio import emit
from app.models.classifier import classify_prompt
from app.models.falcon_model import generate_response
import json
from datetime import datetime, timedelta
from flask import request
import logging

# Create a logger instance
logger = logging.getLogger()

# Dictionary to store user states
user_sessions = {}
SESSION_TIMEOUT = timedelta(minutes=20)  # Set session timeout to 20 minutes

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        user_id = request.sid  # Use session ID as a unique user ID
        logger.info('User connected: %s', user_id)  # Log user connection
        
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

        # Initialize user session if not already present
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                "history": [],  # Store only the last query and response
                "last_activity": datetime.utcnow()  # Track last activity time
            }
        else:
            # Check if the session has expired
            if datetime.utcnow() - user_sessions[user_id]["last_activity"] > SESSION_TIMEOUT:
                user_sessions[user_id]["history"] = []  # Clear the history if session expired
                logger.info("Session for user %s has expired. History cleared.", user_id)

        # Update last activity time
        user_sessions[user_id]["last_activity"] = datetime.utcnow()

        # Predefined responses for common questions
        predefined_responses = {
            "who are you?": "I am EduBot, your educational assistant.",
            "what are you?": "I am an AI-powered educational assistant here to help with your learning needs.",
            "what can you do?": "I can answer educational questions on a wide range of topics.",
            "what is your name?": "My name is EduBot."
        }

        # Handle predefined responses
        if user_input.lower() in predefined_responses:
            response = predefined_responses[user_input.lower()]
        else:
            # Retrieve the last query-response pair, if available
            last_interaction = user_sessions[user_id]["history"][-2:] if len(user_sessions[user_id]["history"]) >= 2 else []
            context = " ".join(last_interaction)  # Combine last query and response

            # Call Falcon model with only the latest query
            response = generate_response(user_id, user_input)

        # Save only the last query-response pair in the session
        user_sessions[user_id]["history"] = [user_input, response]  # Store only the current query and response

        # Log the response sent to the user
        logger.info('Response sent to user %s: %s', user_id, response)

        # Send the response back to the specific user
        emit('response', {'user_id': user_id, 'data': response})

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = request.sid  # Use session ID to identify the user
        logger.info('User disconnected: %s', user_id)  # Log user disconnection

        # Clean up session data upon disconnection
        if user_id in user_sessions:
            del user_sessions[user_id]  # Remove the user's session entirely

        # Send response back when the user disconnects
        emit('response', {'data': 'User disconnected from EduBot!'})
