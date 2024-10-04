from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# falcon_model = "/model_files/falcon_model_files/"
falcon_model = "tiiuae/falcon-7b-instruct"
tokenizer = AutoTokenizer.from_pretrained(falcon_model)
model = AutoModelForCausalLM.from_pretrained(
    falcon_model,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    offload_folder="./OffloadFolder"
)


def generate_response(user_input):
    prompt = f"You (User): {user_input}\nEduBot:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000, do_sample=True, top_k=10)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).split("EduBot:")[-1].strip()
    return response
