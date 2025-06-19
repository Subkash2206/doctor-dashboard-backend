# doctor-dashboard-backend/main.py

from fastapi import FastAPI
from routes import auth, patients, prescription

app = FastAPI(title="AI-Powered Doctor Dashboard Backend")

# Include API route groups
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(prescription.router, prefix="/prescription", tags=["Prescription"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Doctor Dashboard API!"}
