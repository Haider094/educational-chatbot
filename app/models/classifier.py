from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("haider0941/distilbert-base-educationl")
model = AutoModelForSequenceClassification.from_pretrained("haider0941/distilbert-base-educationl")


def classify_prompt(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    prediction = logits.argmax().item()
    return "educational" if prediction == 1 else "noneducational"
