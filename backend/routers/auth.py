from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.patient import Patient
from utils.auth import hash_password, verify_password, create_access_token
from config import settings
from datetime import timedelta

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Check for admin login
    if form_data.username == settings.ADMIN_EMAIL and form_data.password == settings.ADMIN_PASSWORD:
        token = create_access_token(
            data={"sub": settings.ADMIN_EMAIL, "role": "admin"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "email": settings.ADMIN_EMAIL,
                "role": "admin",
                "first_name": "Admin"
            }
        }
    
    # Check patient login
    result = await db.execute(select(Patient).where(Patient.email == form_data.username))
    patient = result.scalar_one_or_none()
    
    if not patient or not patient.password_hash:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not verify_password(form_data.password, patient.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    token = create_access_token(
        data={"sub": patient.email, "role": "patient", "id": patient.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": patient.id,
            "email": patient.email,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "role": "patient"
        }
    }

@router.post("/register")
async def register(email: str, password: str, first_name: str, last_name: str, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    result = await db.execute(select(Patient).where(Patient.email == email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
    
    # Create patient
    patient = Patient(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        full_name=f"{first_name} {last_name}",
        patient_code=f"P{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        role="patient"
    )
    
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    # Create token
    token = create_access_token(
        data={"sub": patient.email, "role": "patient", "id": patient.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": patient.id,
            "email": patient.email,
            "first_name": patient.first_name,
            "last_name": patient.last_name,
            "role": "patient"
        }
    }

from datetime import datetime
