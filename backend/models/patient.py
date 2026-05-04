from sqlalchemy import String, Date, Boolean, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime
import enum

class EconomicStatus(str, enum.Enum):
    normal = "normal"
    reduced = "reduced"
    very_limited = "very_limited"

class Patient(Base):
    __tablename__ = "patients"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(200))
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    sex: Mapped[str] = mapped_column(String(10))
    phone: Mapped[str] = mapped_column(String(20))
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_whatsapp: Mapped[bool] = mapped_column(Boolean, default=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    commune: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Medical
    primary_condition: Mapped[str | None] = mapped_column(String(200), nullable=True)
    secondary_condition: Mapped[str | None] = mapped_column(String(200), nullable=True)
    affected_limbs: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    medical_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    referring_doctor: Mapped[str | None] = mapped_column(String(200), nullable=True)
    insurance_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    economic_status: Mapped[EconomicStatus] = mapped_column(
        Enum(EconomicStatus), default=EconomicStatus.normal
    )
    
    # Account
    password_hash: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), default="patient")  # patient, admin
    
    # Clinical notes (admin only)
    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    treatment_progress: Mapped[int | None] = mapped_column(default=0)  # 0-100
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
