import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv() 

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Falcon model URL
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Assuming you're storing the last interaction in-memory for now (can be swapped for a database or session)
last_interactions = {}

def get_last_interaction(user_id):
    """Get the last query-response pair for a user."""
    return last_interactions.get(user_id, None)

def save_last_interaction(user_id, query, response):
    """Save the last query-response pair for a user."""
    last_interactions[user_id] = {
        "last_query": query,
        "last_response": response
    }

def generate_response(user_id, user_input):
    """Generates a response from the Falcon model using only the latest query and response."""
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Fetch the last interaction
    last_interaction = get_last_interaction(user_id)
    
    # Prepare the context: only use the last query-response pair, if available
    if last_interaction:
        context = f"{last_interaction['last_query']}\n{last_interaction['last_response']}\n{user_input}"
    else:
        context = user_input

    payload = {
        "inputs": f"You are a Educational Chatbot, Answer the following educational question: {context}",
        "options": {
            "use_cache": False
        }
    }
    
    # Send request to Falcon model
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0]['generated_text'].strip()

            # Clean up the response to remove any repeated question part
            answer_start_index = generated_text.lower().find("You are a Educational Chatbot, Answer the following educational question:") + len("You are a Educational Chatbot, Answer the following educational question")
            cleaned_response = generated_text[answer_start_index:].strip()

            # If there's no such phrase, just use the entire generated text as the answer
            if cleaned_response == generated_text:
                cleaned_response = generated_text

            # Save the current query-response pair for future use
            save_last_interaction(user_id, user_input, cleaned_response)

            return cleaned_response
        else:
            return "I'm sorry, I couldn't generate a response."
    else:
        return f"Error: {response.status_code}, {response.text}"
