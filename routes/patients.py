# routes/patients.py

from fastapi import APIRouter, HTTPException
from models.patient import Patient
from typing import List
from utils.ai import suggest_department  # ✅ AI-powered suggestion

router = APIRouter()

# In-memory database simulation
patients_db = []

@router.post("/", response_model=dict)
def create_patient(patient: Patient):
    # ✅ Use AI model to suggest department
    ai_suggestion = suggest_department(patient.symptoms)

    patient_data = patient.dict()
    patient_data["assigned_department"] = ai_suggestion
    patients_db.append(patient_data)

    return {
        "message": f"Patient assigned to: {ai_suggestion}",
        "patient": patient_data
    }

@router.get("/", response_model=List[dict])
def list_patients():
    return patients_db

