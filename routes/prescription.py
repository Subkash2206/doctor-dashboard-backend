# routes/prescription.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.ai import get_prescription, suggest_department

router = APIRouter()

class SymptomsInput(BaseModel):
    symptoms: str

@router.post("/ai", response_model=dict)
def generate_ai_prescription(input: SymptomsInput):
    try:
        # Validate symptoms input
        if not input.symptoms.strip():
            raise HTTPException(status_code=400, detail="Symptoms cannot be empty.")

        # Get AI-generated prescription
        prescription = get_prescription(input.symptoms)
        if prescription.startswith("❌") or "error" in prescription.lower():
            raise HTTPException(status_code=500, detail="Failed to generate prescription from AI.")

        # Get AI-suggested department
        department = suggest_department(input.symptoms)
        if department.startswith("❌") or "error" in department.lower():
            raise HTTPException(status_code=500, detail="Failed to suggest department from AI.")

        return {
            "symptoms": input.symptoms,
            "suggested_department": department,
            "ai_prescription": prescription
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

