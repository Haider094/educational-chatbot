from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# Define the cache directory
cache_dir = "./cache"

# Create the cache directory if it doesn't exist
os.makedirs(cache_dir, exist_ok=True)

falcon_model = "tiiuae/falcon-7b-instruct"

# Load the tokenizer and model with the cache directory
tokenizer = AutoTokenizer.from_pretrained(falcon_model, cache_dir=cache_dir)
model = AutoModelForCausalLM.from_pretrained(
    falcon_model,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    offload_folder="./OffloadFolder",
    cache_dir=cache_dir  # Use cache directory
)

def generate_response(user_input):
    prompt = f"You (User): {user_input}\nEduBot:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000, do_sample=True, top_k=10)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).split("EduBot:")[-1].strip()
    return response
