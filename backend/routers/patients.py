from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.patient import Patient, EconomicStatus
from models.appointment import Appointment
from utils.auth import get_current_user, require_admin
from datetime import datetime

router = APIRouter()

@router.post("/")
async def create_patient(
    full_name: str,
    phone: str,
    email: str | None = None,
    date_of_birth: str | None = None,
    sex: str = "",
    whatsapp: str | None = None,
    department: str | None = None,
    commune: str | None = None,
    address: str | None = None,
    primary_condition: str | None = None,
    insurance_type: str | None = None,
    economic_status: EconomicStatus = EconomicStatus.normal,
    db: AsyncSession = Depends(get_db)
):
    # Generate patient code
    patient_code = f"P{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    patient = Patient(
        patient_code=patient_code,
        full_name=full_name,
        phone=phone,
        email=email,
        date_of_birth=date_of_birth,
        sex=sex,
        whatsapp=whatsapp or phone,
        department=department,
        commune=commune,
        address=address,
        primary_condition=primary_condition,
        insurance_type=insurance_type,
        economic_status=economic_status
    )
    
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    
    return {
        "id": patient.id,
        "patient_code": patient.patient_code,
        "message": "Patient enregistré avec succès"
    }

@router.get("/")
async def list_patients(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(Patient).where(Patient.role == "patient")
    
    if search:
        query = query.where(
            Patient.full_name.ilike(f"%{search}%") |
            Patient.email.ilike(f"%{search}%") |
            Patient.patient_code.ilike(f"%{search}%")
        )
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    patients = result.scalars().all()
    
    return [
        {
            "id": p.id,
            "patient_code": p.patient_code,
            "full_name": p.full_name,
            "phone": p.phone,
            "email": p.email,
            "primary_condition": p.primary_condition,
            "economic_status": p.economic_status.value,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in patients
    ]

@router.get("/{patient_id}")
async def get_patient(
    patient_id: int,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient non trouvé")
    
    # Get patient appointments
    result = await db.execute(
        select(Appointment).where(Appointment.patient_id == patient_id)
        .order_by(Appointment.appointment_date.desc())
    )
    appointments = result.scalars().all()
    
    return {
        "id": patient.id,
        "patient_code": patient.patient_code,
        "full_name": patient.full_name,
        "first_name": patient.first_name,
        "last_name": patient.last_name,
        "date_of_birth": patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        "sex": patient.sex,
        "phone": patient.phone,
        "whatsapp": patient.whatsapp,
        "email": patient.email,
        "department": patient.department,
        "commune": patient.commune,
        "address": patient.address,
        "primary_condition": patient.primary_condition,
        "secondary_condition": patient.secondary_condition,
        "affected_limbs": patient.affected_limbs,
        "medical_history": patient.medical_history,
        "insurance_type": patient.insurance_type,
        "economic_status": patient.economic_status.value,
        "clinical_notes": patient.clinical_notes,
        "treatment_progress": patient.treatment_progress,
        "appointments": [
            {
                "id": a.id,
                "booking_code": a.booking_code,
                "appointment_date": a.appointment_date.isoformat(),
                "appointment_time": str(a.appointment_time)[:5],
                "status": a.status.value
            }
            for a in appointments
        ]
    }

@router.patch("/{patient_id}")
async def update_patient(
    patient_id: int,
    clinical_notes: str | None = None,
    treatment_progress: int | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient non trouvé")
    
    if clinical_notes is not None:
        patient.clinical_notes = clinical_notes
    if treatment_progress is not None:
        patient.treatment_progress = treatment_progress
    
    await db.commit()
    
    return {"message": "Patient mis à jour avec succès"}

@router.get("/me")
async def get_current_patient(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.get("role") != "patient":
        raise HTTPException(403, "Accès réservé aux patients")
    
    result = await db.execute(
        select(Patient).where(Patient.id == current_user.get("id"))
    )
    patient = result.scalar_one_or_none()
    
    if not patient:
        raise HTTPException(404, "Patient non trouvé")
    
    return {
        "id": patient.id,
        "patient_code": patient.patient_code,
        "full_name": patient.full_name,
        "email": patient.email,
        "phone": patient.phone
    }
