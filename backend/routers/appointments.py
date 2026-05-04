from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from models.appointment import Appointment, AppointmentStatus, AppointmentType
from models.patient import Patient
from utils.auth import get_current_user, require_admin
from datetime import date, time, timedelta
import random
import string

router = APIRouter()

def generate_booking_code():
    return "HRC-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

@router.get("/slots")
async def get_available_slots(
    appointment_date: date = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Return available time slots for a given date"""
    all_slots = [
        "08:00", "09:00", "10:00", "11:00", 
        "13:00", "14:00"
    ]
    
    # Get booked slots for this date
    result = await db.execute(
        select(Appointment.appointment_time).where(
            Appointment.appointment_date == appointment_date,
            Appointment.status.in_([AppointmentStatus.pending, AppointmentStatus.confirmed])
        )
    )
    booked_times = {str(t)[:5] for t in result.scalars().all()}
    
    return {
        "date": appointment_date.isoformat(),
        "slots": [
            {"time": slot, "available": slot not in booked_times}
            for slot in all_slots
        ]
    }

@router.post("/")
async def create_appointment(
    appointment_type: AppointmentType,
    appointment_date: date,
    appointment_time: str,
    guest_name: str,
    guest_phone: str,
    guest_email: str | None = None,
    guest_condition: str | None = None,
    notes: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    # Check slot not already taken
    hour, minute = map(int, appointment_time.split(':'))
    time_obj = time(hour, minute)
    
    existing = await db.scalar(
        select(Appointment).where(
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == time_obj,
            Appointment.status.in_([AppointmentStatus.pending, AppointmentStatus.confirmed])
        )
    )
    if existing:
        raise HTTPException(status_code=409, detail="Ce créneau n'est plus disponible")
    
    appointment = Appointment(
        appointment_type=appointment_type,
        appointment_date=appointment_date,
        appointment_time=time_obj,
        guest_name=guest_name,
        guest_phone=guest_phone,
        guest_email=guest_email,
        guest_condition=guest_condition,
        notes=notes,
        booking_code=generate_booking_code(),
        status=AppointmentStatus.pending
    )
    
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    
    return {
        "id": appointment.id,
        "booking_code": appointment.booking_code,
        "status": appointment.status.value,
        "message": "Rendez-vous créé avec succès"
    }

@router.get("/")
async def list_appointments(
    status: AppointmentStatus | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(Appointment)
    if status:
        query = query.where(Appointment.status == status)
    if date_from:
        query = query.where(Appointment.appointment_date >= date_from)
    if date_to:
        query = query.where(Appointment.appointment_date <= date_to)
    query = query.order_by(Appointment.appointment_date, Appointment.appointment_time)
    result = await db.execute(query)
    appointments = result.scalars().all()
    
    return [
        {
            "id": a.id,
            "booking_code": a.booking_code,
            "guest_name": a.guest_name,
            "guest_phone": a.guest_phone,
            "appointment_date": a.appointment_date.isoformat(),
            "appointment_time": str(a.appointment_time)[:5],
            "appointment_type": a.appointment_type.value,
            "status": a.status.value,
            "notes": a.notes
        }
        for a in appointments
    ]

@router.patch("/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    appointment = await db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(404, "Rendez-vous non trouvé")
    
    appointment.status = status
    await db.commit()
    
    return {"status": "updated", "new_status": status.value}

@router.get("/today")
async def get_today_appointments(
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    today = date.today()
    result = await db.execute(
        select(Appointment).where(
            Appointment.appointment_date == today
        ).order_by(Appointment.appointment_time)
    )
    appointments = result.scalars().all()
    
    return [
        {
            "id": a.id,
            "booking_code": a.booking_code,
            "guest_name": a.guest_name,
            "guest_phone": a.guest_phone,
            "appointment_time": str(a.appointment_time)[:5],
            "appointment_type": a.appointment_type.value,
            "status": a.status.value
        }
        for a in appointments
    ]
