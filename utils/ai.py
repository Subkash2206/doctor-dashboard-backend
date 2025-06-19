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
        f"Patient presents with the following symptoms: {symptoms}.\n"
        f"Give a brief, clear prescription including medication (if needed) and lifestyle advice.\n"
        f"Example format:\n"
        f"- Medication: Paracetamol 500mg twice daily\n"
        f"- Advice: Drink plenty of fluids, rest for 3 days\n\n"
        f"Prescription:"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 100}},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                output = data[0]["generated_text"]
                lines = output.split("\n")
                # Extract lines after "Prescription:"
                if "Prescription:" in lines[0]:
                    lines = lines[1:]
                return "\n".join(line.strip() for line in lines if line.strip())
            return "⚠️ AI returned unexpected response format."
        else:
            return f"❌ AI error {response.status_code}: {response.text}"

    except requests.exceptions.Timeout:
        return "❌ AI request timed out. Try again later."
    except requests.exceptions.RequestException as e:
        return f"❌ AI request failed: {str(e)}"


def suggest_department(symptoms: str) -> str:
    if not HF_TOKEN:
        return "General Medicine"  # fallback for demo

    prompt = (
        f"Based on the following patient symptoms:\n"
        f"{symptoms}\n\n"
        f"Which department should the patient be referred to?\n"
        f"Choose from: Cardiology, Neurology, Dermatology, Psychiatry, Orthopedics, General Medicine\n\n"
        f"Answer with only the department name."
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
                raw = data[0]["generated_text"].strip()

                # Look for a valid department in the response
                for dept in ["Cardiology", "Neurology", "Dermatology", "Psychiatry", "Orthopedics", "General Medicine"]:
                    if dept.lower() in raw.lower():
                        return dept

        # If something goes wrong or unexpected, fallback
        return "General Medicine"

    except Exception:
        return "General Medicine"

