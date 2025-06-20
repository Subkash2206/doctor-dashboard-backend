# 🏥 AI-Powered Doctor Dashboard — Backend

This is the **FastAPI backend** for the AI-Powered Doctor Dashboard — a system that allows doctors to:
- View and manage patient records
- Use AI to generate prescriptions based on symptoms
- Route patients to relevant departments

Hosted on **Render**, connected to a React frontend.

---

## 🚀 Features

- 🔐 Doctor login with mock OTP
- 🗂️ Patient management (add/view)
- 🤖 AI-generated prescriptions via Hugging Face
- 🔌 RESTful API structure
- 🧪 Swagger UI at `/docs`

---

## 🔧 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **Hugging Face Inference API**
- **Render** for deployment

---

## 🌐 Live API

[Render Deployment](https://doctor-dashboard-backend-6853.onrender.com)


You can test APIs interactively at:

📄 `/docs` 

---

## ⚙️ How to Run Locally

```bash
# Clone and enter project
git clone https://github.com/Subkash2206/doctor-dashboard-backend.git
cd doctor-dashboard-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your Hugging Face token
echo 'HF_TOKEN=your_token_here' > .env
# Optionally, set HF_MODEL to override the default model (see below)

# Run the server
uvicorn main:app --reload
```
```bash
\.
├── main.py
├── routes/
├── models/
├── utils/
└── requirements.txt
```
🧠 Model Info
LLM used: mistralai/Mixtral-8x7B-Instruct-v0.1 (default)
Accessed via Hugging Face API with HF_TOKEN.
You can override the model by setting HF_MODEL in your .env file.

If HF_TOKEN is missing, the backend will fall back to basic keyword-based logic for department suggestion and will not generate AI prescriptions.

## 🔍 AI Health Check Endpoint

You can check if the AI service is available by calling:

```
GET /ai-health
```

This returns `{ "ai_available": true/false, ... }` so the frontend or monitoring tools can detect AI outages.

All requests are connected to:
https://doctor-dashboard-backend-6853.onrender.com

Deployment
Platform: Render
Python: 3.13
Start Command:
```bash
uvicorn main:app --host=0.0.0.0 --port=8000
```

🔒 Environment Variables
Key	Description
HF_TOKEN	Hugging Face access token
HF_MODEL	(Optional) Hugging Face model name (default: mistral-community/Mistral-7B-Instruct-v0.1)

Set these in Render → Environment → Environment Variables.

🛠 Hosting & Deployment
Frontend: React app (planned for Vercel/Netlify or hosted locally)

Backend: FastAPI server deployed on Render

Includes support for AI endpoints using Hugging Face Inference API

Optional: Include the actual Render URL, if it's public:

markdown
Copy
Edit
🔗 Backend API: https://doctor-dashboard-backend.onrender.com
You can put this under a Hosting & Deployment section in your README, or as part of the Tech Stack section like:

Front-End Link: [https://doctor-dashboard-frontend.vercel.app/]
Swagger UI: [https://doctor-dashboard-backend-6853.onrender.com/docs#/]


🔧 Functionality
The AI-Powered Doctor Dashboard streamlines patient management and assists doctors with AI-generated recommendations. Key features include:

👤 Doctor Login
Simple OTP-based login (for prototype/demo purposes).

Simulates doctor session without complex auth systems.

🧾 Add & View Patients
Doctors can add new patients with:

Name, age, gender

Symptoms, diagnosis, and history

Patients are auto-assigned to a medical department using an AI model (based on symptoms).

📋 Dashboard
Displays all patients with essential information.

Click into each patient for full details and AI features.

🧠 AI-Powered Prescription Generator
Uses Hugging Face's Mistral-7B-Instruct model to generate a treatment or prescription based on symptoms.

Available via a separate page or directly in the patient profile.

Sorted based off the department and severity.
