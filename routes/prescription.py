# routes/prescription.py


from fastapi import APIRouter
from pydantic import BaseModel
from utils.ai import get_prescription, suggest_department

router = APIRouter()

class SymptomsInput(BaseModel):
    symptoms: str

@router.post("/ai")
def generate_ai_prescription(input: SymptomsInput):
    prescription = get_prescription(input.symptoms)
    department = suggest_department(input.symptoms)

    return {
        "symptoms": input.symptoms,
        "suggested_department": department,
        "ai_prescription": prescription
    }

