# routes/patients.py

from fastapi import APIRouter, HTTPException, Body, Path
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

        # Fallback to General Medicine if AI fails
        if ai_suggestion.startswith("❌") or "error" in ai_suggestion.lower():
            ai_suggestion = "General Medicine"

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


@router.post("/suggest-department", response_model=dict)
def suggest_department_api(symptoms: str = Body(..., embed=True)):
    try:
        ai_suggestion = suggest_department(symptoms)
        # Fallback to General Medicine if AI fails
        if ai_suggestion.startswith("❌") or "error" in ai_suggestion.lower():
            ai_suggestion = "General Medicine"
        return {"suggested_department": ai_suggestion}
    except Exception as e:
        return {"suggested_department": "General Medicine"}


@router.delete("/{patient_id}", response_model=dict)
def delete_patient(patient_id: int = Path(..., description="Index of the patient to delete")):
    try:
        if 0 <= patient_id < len(patients_db):
            removed = patients_db.pop(patient_id)
            return {"message": "Patient deleted", "patient": removed}
        else:
            raise HTTPException(status_code=404, detail="Patient not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

