from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load your fine-tuned model for classification
model_path = './model_files'

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)


def classify_prompt(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = logits.argmax().item()
    return "educational" if prediction == 1 else "noneducational"
