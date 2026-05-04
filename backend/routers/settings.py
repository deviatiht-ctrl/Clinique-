from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.settings import SiteSettings
from utils.auth import require_admin

router = APIRouter()

@router.get("/")
async def get_settings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SiteSettings))
    settings_list = result.scalars().all()
    
    return {s.key: s.value for s in settings_list}

@router.put("/")
async def update_settings(
    settings_dict: dict,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    for key, value in settings_dict.items():
        result = await db.execute(select(SiteSettings).where(SiteSettings.key == key))
        setting = result.scalar_one_or_none()
        
        if setting:
            setting.value = str(value)
        else:
            setting = SiteSettings(key=key, value=str(value))
            db.add(setting)
    
    await db.commit()
    
    return {"message": "Paramètres mis à jour avec succès"}
