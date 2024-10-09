import requests
from dotenv import load_dotenv
import os

load_dotenv() 

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Falcon model URL
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

def generate_response(user_input):
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": f"Answer the following educational question directly without repeating the question: {user_input}",
        "options": {
            "use_cache": False
        }
    }
    
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    print(response)
    if response.status_code == 200:
        output = response.json()
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0]['generated_text'].strip()

            # Find and clean up any leftover question text
            answer_start_index = generated_text.lower().find("answer the following question:") + len("answer the following question:")
            answer = generated_text[answer_start_index:].strip()

            # If there's no "answer the following" phrase, just return the response directly
            if answer == generated_text:
                return generated_text

            print(answer)
            return answer
        else:
            return "I'm sorry, I couldn't generate a response."
    else:
        return f"Error: {response.status_code}, {response.text}"

