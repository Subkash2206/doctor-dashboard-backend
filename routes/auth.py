# routes/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# Simulate in-memory login store
active_logins = {}

class DoctorLogin(BaseModel):
    doctor_id: str
    otp: str = "1234"  # Simulated fixed OTP for prototype

@router.post("/login")
def login(data: DoctorLogin):
    # ✅ No prefix restriction
    if data.otp != "1234":
        raise HTTPException(status_code=401, detail="Invalid OTP")

    # Simulate session
    active_logins[data.doctor_id] = {
        "login_time": datetime.now().isoformat(),
        "session_active": True
    }

    return {
        "message": "Login successful",
        "doctor_id": data.doctor_id,
        "session": active_logins[data.doctor_id]
    }

@router.get("/status/{doctor_id}")
def check_status(doctor_id: str):
    session = active_logins.get(doctor_id)
    if not session:
        return {"logged_in": False}
    return {"logged_in": True, "session": session}

