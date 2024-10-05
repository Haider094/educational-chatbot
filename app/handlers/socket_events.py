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
        emit('message', {'data': 'Connected to EduBot! Ask me any educational question.'})

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
                "history": [],
                "last_activity": datetime.utcnow()  # Track last activity time
            }
        else:
            # Check if the session has expired
            if datetime.utcnow() - user_sessions[user_id]["last_activity"] > SESSION_TIMEOUT:
                # Clear history if session has expired
                user_sessions[user_id]["history"] = []
                logger.info("Session for user %s has expired. History cleared.", user_id)

        # Update last activity time
        user_sessions[user_id]["last_activity"] = datetime.utcnow()

        predefined_responses = {
            "who are you?": "I am EduBot, your educational assistant.",
            "what are you?": "I am an AI-powered educational assistant here to help with your learning needs.",
            "what can you do?": "I can answer educational questions on a wide range of topics.",
            "what is your name?": "My name is EduBot."
        }

        if user_input.lower() in predefined_responses:
            response = predefined_responses[user_input.lower()]
        else:
            classification = classify_prompt(user_input)
            if classification == "noneducational":
                response = "Apologies, but I am here to assist with educational inquiries only."
            else:
                # Include the history in the prompt
                history = user_sessions[user_id]["history"]
                context = " ".join(history)
                response = generate_response(f"{context} {user_input}")

        # Save the new message and response to the history
        user_sessions[user_id]["history"].append(user_input)
        user_sessions[user_id]["history"].append(response)

        # Optional: Limit the history size to prevent overflow
        if len(user_sessions[user_id]["history"]) > 10:  # Arbitrary limit
            user_sessions[user_id]["history"] = user_sessions[user_id]["history"][-10:]

        # Log the response sent to the user
        logger.info('Response sent to user %s: %s', user_id, response)

        # Send response back to the specific user
        emit('response', {'user_id': user_id, 'data': response})

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = request.sid  # Assuming `request.sid` identifies the user
        logger.info('User disconnected: %s', user_id)  # Log user disconnection
        if user_id in user_sessions:
            del user_sessions[user_id]["history"]
