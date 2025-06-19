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

        # ❌ Check for AI failure
        if ai_suggestion.startswith("❌") or "error" in ai_suggestion.lower():
            raise HTTPException(status_code=500, detail="AI failed to assign department.")

        # ✅ Correctly placed — only runs if AI is successful
        patient_data = {
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "symptoms": patient.symptoms,
            "diagnosis": patient.diagnosis,
            "history": patient.history,
            "assigned_department": ai_suggestion
        }

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

