from sqlalchemy import String, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class GalleryImage(Base):
    __tablename__ = "gallery_images"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    filename: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(500))
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    order: Mapped[int] = mapped_column(default=0)
    featured: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
