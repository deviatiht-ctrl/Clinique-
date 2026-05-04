from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    value: Mapped[str] = mapped_column(String(500))
