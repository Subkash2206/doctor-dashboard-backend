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
        print("❌ Missing Hugging Face token.")
        return "⚠️ Prescription unavailable: HF token not set."

    prompt = (
        f"A patient reports the following symptoms: {symptoms}.\n\n"
        f"Write a short prescription with:\n"
        f"- Medication name and dosage (if needed)\n"
        f"- Basic lifestyle advice\n\n"
        f"Output:"
    )

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7
                }
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print("💊 AI prescription response:", data)

            if isinstance(data, list) and "generated_text" in data[0]:
                full_text = data[0]["generated_text"].strip()
                return full_text.split("Output:")[-1].strip()
            return "⚠️ AI returned unexpected format."

        else:
            print(f"❌ HF API Error {response.status_code}: {response.text}")
            return f"⚠️ HF API error: {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        print("❌ AI request timed out.")
        return "⚠️ AI timeout - try again."

    except Exception as e:
        print("❌ Exception while getting prescription:", str(e))
        return f"⚠️ AI failed to generate prescription: {str(e)}"


def suggest_department(symptoms: str) -> str:
    if not HF_TOKEN:
        print("❌ Missing Hugging Face token.")
        return "General Medicine"

    prompt = (
        f"Symptoms: {symptoms}\n\n"
        f"Based on this, which department should the patient be referred to?\n"
        f"Choose exactly one from: Cardiology, Neurology, Dermatology, Psychiatry, Orthopedics, General Medicine.\n"
        f"Answer with just the department name."
    )

    departments = [
        "Cardiology", "Neurology", "Dermatology", "Psychiatry", "Orthopedics", "General Medicine"
    ]
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 50,
                    "temperature": 0.5
                }
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            print("🏥 AI department suggestion response:", data)

            # Try to extract department strictly
            if isinstance(data, list) and "generated_text" in data[0]:
                raw = data[0]["generated_text"].strip()
                print(f"AI raw output: '{raw}'")
                # Check for exact match (case-insensitive, strip extra text)
                for dept in departments:
                    if raw.lower() == dept.lower():
                        return dept
                # Check if department is contained in the response
                for dept in departments:
                    if dept.lower() in raw.lower():
                        return dept
                # Fallback: keyword-based matching from symptoms
                print("⚠️ No department matched in AI output, using keyword fallback.")
                symptom_lower = symptoms.lower()
                if any(word in symptom_lower for word in ["chest", "heart", "angina", "palpitation"]):
                    return "Cardiology"
                if any(word in symptom_lower for word in ["headache", "seizure", "stroke", "paralysis", "neuro"]):
                    return "Neurology"
                if any(word in symptom_lower for word in ["skin", "rash", "itch", "eczema"]):
                    return "Dermatology"
                if any(word in symptom_lower for word in ["anxiety", "depression", "mental", "psych"]):
                    return "Psychiatry"
                if any(word in symptom_lower for word in ["bone", "joint", "fracture", "orthopedic"]):
                    return "Orthopedics"
                # Default fallback
                return "General Medicine"
            return "General Medicine"

        else:
            print(f"❌ HF API Error {response.status_code}: {response.text}")
            return f"General Medicine (AI error: {response.status_code} - {response.text})"

    except requests.exceptions.Timeout:
        print("❌ Department suggestion timed out.")
        return "General Medicine (AI timeout)"

    except Exception as e:
        print("❌ Exception while suggesting department:", str(e))
        return f"General Medicine (AI exception: {str(e)})"

