from sqlalchemy import String, Date, Time, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime, date, time
import enum

class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"

class AppointmentType(str, enum.Enum):
    first_consultation = "first_consultation"
    follow_up = "follow_up"
    emergency = "emergency"
    measurement = "measurement"
    device_fitting = "device_fitting"

class Appointment(Base):
    __tablename__ = "appointments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    patient_id: Mapped[int | None] = mapped_column(ForeignKey("patients.id"), nullable=True)
    
    # Guest booking (non-registered)
    guest_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    guest_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    guest_email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    guest_condition: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    appointment_date: Mapped[date] = mapped_column(Date, index=True)
    appointment_time: Mapped[time] = mapped_column(Time)
    appointment_type: Mapped[AppointmentType] = mapped_column(Enum(AppointmentType))
    status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.pending)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    patient = relationship("Patient", back_populates="appointments")
