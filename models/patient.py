# models/patient.py

from pydantic import BaseModel, Field
from typing import Optional

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    symptoms: str
    diagnosis: str
    history: Optional[str] = Field(default="", description="Previous medical history")

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 45,
                "gender": "Male",
                "symptoms": "Chest pain, shortness of breath",
                "diagnosis": "Suspected angina",
                "history": "Hypertension, Smoker"
            }
        }
