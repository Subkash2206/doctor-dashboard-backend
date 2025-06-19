# routes/prescription.py

from fastapi import APIRouter
from pydantic import BaseModel
from utils.ai import get_prescription

router = APIRouter()

class SymptomsInput(BaseModel):
    symptoms: str

@router.post("/ai")
def generate_ai_prescription(input: SymptomsInput):
    result = get_prescription(input.symptoms)
    return {
        "symptoms": input.symptoms,
        "ai_prescription": result
    }
