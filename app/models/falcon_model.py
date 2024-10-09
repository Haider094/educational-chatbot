import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Falcon model URL
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def generate_response(user_input):
    """Generates a response from the Falcon model without including the user input in the final response."""
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": f"You are an Educational Chatbot. Answer the following educational question: {user_input}",
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

            # Remove all text before the first newline character
            cleaned_response = generated_text.split('\n', 1)[-1].strip()

            print("cleaned_response: " + cleaned_response)

            return cleaned_response
        else:
            return "I'm sorry, I couldn't generate a response."
    else:
        return f"Error: {response.status_code}, {response.text}"

