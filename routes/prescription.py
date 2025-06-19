# routes/prescription.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.ai import get_prescription, suggest_department

router = APIRouter()

class SymptomsInput(BaseModel):
    symptoms: str

@router.post("/ai")
def generate_ai_prescription(input: SymptomsInput):
    try:
        prescription = get_prescription(input.symptoms)
        department = suggest_department(input.symptoms)

        # Handle potential AI errors
        if any(msg in prescription.lower() for msg in ["error", "❌"]) or not prescription.strip():
            raise HTTPException(status_code=500, detail="AI failed to generate prescription.")

        if any(msg in department.lower() for msg in ["error", "❌"]) or not department.strip():
            raise HTTPException(status_code=500, detail="AI failed to suggest department.")

        return {
            "symptoms": input.symptoms,
            "suggested_department": department,
            "ai_prescription": prescription
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

