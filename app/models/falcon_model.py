import requests
import os
from dotenv import load_dotenv

HF_API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"  # Falcon model URL
HF_API_TOKEN = os.getenv("HF_API_TOKEN") 

def generate_response(user_input):
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": f"You are an AI assistant. Answer the following question: {user_input}",
        "options": {
            "use_cache": False
        }
    }
    
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        output = response.json()
        # print("Raw output:", output)  # Print entire response for debugging
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0]['generated_text'].strip()
            answer_start_index = generated_text.lower().find("answer the following question:") + len("answer the following question:")
            answer = generated_text[answer_start_index:].strip()
            return answer
        else:
            return "I'm sorry, I couldn't generate a response."
    else:
        return f"Error: {response.status_code}, {response.text}"

