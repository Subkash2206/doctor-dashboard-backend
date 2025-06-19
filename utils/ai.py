def suggest_department(symptoms: str) -> str:
    if not HF_TOKEN:
        print("❌ HF_TOKEN missing")
        return "General Medicine"

    prompt = (
        f"Symptoms: {symptoms}\n\n"
        f"Based on this, which department should the patient be referred to?\n"
        f"Choose exactly one of: Cardiology, Neurology, Dermatology, Psychiatry, Orthopedics, General Medicine.\n"
        f"Answer with just the department name."
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
            print("🔍 AI response:", data)  # Optional: debug logging

            if isinstance(data, list) and "generated_text" in data[0]:
                text = data[0]["generated_text"].strip()
                # Extract department
                for dept in ["Cardiology", "Neurology", "Dermatology", "Psychiatry", "Orthopedics", "General Medicine"]:
                    if dept.lower() in text.lower():
                        return dept
                print("⚠️ Department not matched, fallback used.")
                return "General Medicine"
            return "General Medicine"

        else:
            print(f"❌ AI error {response.status_code}: {response.text}")
            return "General Medicine"

    except requests.exceptions.Timeout:
        print("❌ AI timeout")
        return "General Medicine"

    except Exception as e:
        print(f"❌ AI exception: {str(e)}")
        return "General Medicine"
