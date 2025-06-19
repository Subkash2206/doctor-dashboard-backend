# utils/ai.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def get_prescription(symptoms: str) -> str:
    prompt = f"Patient symptoms: {symptoms}\nSuggested prescription and lifestyle advice:"
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except (IndexError, KeyError):
            return "AI returned an unexpected format."
    else:
        return f"AI error: {response.status_code} - {response.text}"
