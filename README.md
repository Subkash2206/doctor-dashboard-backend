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

📍 [https://doctor-dashboard-backend.onrender.com](https://doctor-dashboard-backend.onrender.com)

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
LLM used: mistralai/Mixtral-8x7B-Instruct-v0.1
Accessed via Hugging Face API with HF_TOKEN.

All requests are connected to:
https://doctor-dashboard-backend.onrender.com

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

Set these in Render → Environment → Environment Variables.

