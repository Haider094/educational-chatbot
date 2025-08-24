import requests
from dotenv import load_dotenv
import os
from requests.exceptions import RequestException, Timeout

# Load environment variables
load_dotenv()

HF_API_URL = "https://api-inference.huggingface.co/models/openai/gpt-oss-20b"  # Falcon model URL
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def generate_response(user_input):
    """Generates a response from the Falcon model with improved error handling."""
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
    
    try:
        # Changed timeout to 120 seconds (2 minutes)
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0]['generated_text'].strip()
            cleaned_response = generated_text.split('\n', 1)[-1].strip()
            return cleaned_response
        
        return "I'm sorry, I couldn't generate a response."
        
    except Timeout:
        return "I'm sorry, the request timed out. Please try again."
    except RequestException as e:
        return f"An error occurred while processing your request: {str(e)}"
    except Exception as e:
        return "I apologize, but I encountered an unexpected error."

