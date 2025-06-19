# routes/patients.py

from fastapi import APIRouter, HTTPException
from models.patient import Patient
from typing import List

router = APIRouter()

# In-memory database simulation
patients_db = []

# Helper: Simple specialization assignment logic
def assign_specialist(symptoms: str) -> str:
    symptoms_lower = symptoms.lower()
    if "chest" in symptoms_lower or "breath" in symptoms_lower:
        return "CARD"  # Cardiology
    elif "skin" in symptoms_lower or "rash" in symptoms_lower:
        return "DERM"  # Dermatology
    elif "headache" in symptoms_lower:
        return "NEURO"  # Neurology
    else:
        return "GEN"  # General Physician

@router.post("/", response_model=dict)
def create_patient(patient: Patient):
    assigned_dept = assign_specialist(patient.symptoms)
    patient_data = patient.dict()
    patient_data["assigned_department"] = assigned_dept
    patients_db.append(patient_data)
    return {"message": f"Patient assigned to {assigned_dept}", "patient": patient_data}

@router.get("/", response_model=List[dict])
def list_patients():
    return patients_db
