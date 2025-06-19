# routes/patients.py

from fastapi import APIRouter, HTTPException
from models.patient import Patient
from typing import List
from utils.ai import suggest_department  # ✅ AI-powered department suggestion

router = APIRouter()

# In-memory database simulation
patients_db = []

@router.post("/", response_model=dict)
def create_patient(patient: Patient):
    try:
        # ✅ Use AI to suggest department
        ai_suggestion = suggest_department(patient.symptoms)

        # Handle error responses from AI
        if ai_suggestion.startswith("❌") or "error" in ai_suggestion.lower():
            raise HTTPException(status_code=500, detail="AI failed to assign department.")

        patient_data = patient.dict()
        patient_data["assigned_department"] = ai_suggestion
        patients_db.append(patient_data)

        return {
            "message": f"Patient assigned to: {ai_suggestion}",
            "patient": patient_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/", response_model=List[dict])
def list_patients():
    return patients_db

