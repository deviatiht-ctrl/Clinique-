from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class TeamMember(Base):
    __tablename__ = "team_members"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    role: Mapped[str] = mapped_column(String(200))
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    certification: Mapped[str | None] = mapped_column(String(200), nullable=True)
    experience_years: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order: Mapped[int] = mapped_column(default=0)
    featured: Mapped[bool] = mapped_column(default=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
