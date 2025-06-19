# utils/ai.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def get_prescription(symptoms: str) -> str:
    if not HF_TOKEN:
        return "❌ Hugging Face API token not set in environment."

    prompt = (
        f"Patient symptoms: {symptoms}\n"
        f"Suggest a brief prescription and basic lifestyle advice:"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 100}},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                generated = data[0]["generated_text"]
                return generated.replace(prompt, "").strip()
            return "⚠️ AI returned an unexpected response format."
        else:
            return f"❌ AI error {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "❌ AI request timed out. Try again later."

    except requests.exceptions.RequestException as e:
        return f"❌ AI request failed: {str(e)}"


def suggest_department(symptoms: str) -> str:
    if not HF_TOKEN:
        return "General Medicine"  # fallback if token is missing

    prompt = (
        f"Patient symptoms: {symptoms}\n"
        f"Which medical department should the patient visit? "
        f"(Examples: Cardiology, Neurology, Orthopedics, General Medicine, etc.)"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                output = data[0]["generated_text"].lower()

                # Very basic keyword check
                if "cardiology, heart" in output:
                    return "Cardiology"
                elif "neuro, nerve, brain" in output:
                    return "Neurology"
                elif "ortho, leg, foot, fracture" in output:
                    return "Orthopedics"
                elif "dermatology, skin, rash, burn" in output or "skin" in output:
                    return "Dermatology"
                else:
                    return "General Medicine"
            return "General Medicine"
        else:
            return "General Medicine"

    except Exception:
        return "General Medicine"


