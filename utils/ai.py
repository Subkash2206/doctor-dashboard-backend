import requests
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistral-community/Mistral-7B-Instruct-v0.1")
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}


def get_prescription(symptoms: str) -> str:
    if not HF_TOKEN:
        return "❌ HF_TOKEN missing in environment"

    prompt = (
        f"A patient reports the following symptoms: {symptoms}\n\n"
        f"Write a short prescription with:\n"
        f"- Medication name and dosage\n"
        f"- Lifestyle advice\n\n"
        f"Output:"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 150}},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                output = data[0]["generated_text"].strip()
                return output.split("Output:")[-1].strip()
            return "⚠️ AI returned unexpected format."
        else:
            return f"❌ AI error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ AI request failed: {str(e)}"


def suggest_department(symptoms: str) -> str:
    if not HF_TOKEN:
        return "❌ HF_TOKEN missing"

    prompt = (
        f"Symptoms: {symptoms}\n"
        f"Based on this, which department should the patient be referred to?\n"
        f"Answer with **one** of the following exactly: Cardiology, Neurology, Dermatology, Psychiatry, Orthopedics, General Medicine."
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 50}},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                raw = data[0]["generated_text"]
                for dept in ["Cardiology", "Neurology", "Dermatology", "Psychiatry", "Orthopedics", "General Medicine"]:
                    if dept.lower() in raw.lower():
                        return dept
                return "❌ AI did not suggest a valid department."
            return "⚠️ AI returned unexpected format."
        else:
            return f"❌ AI error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ AI request failed: {str(e)}"

