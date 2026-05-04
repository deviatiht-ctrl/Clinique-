from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.gallery import GalleryImage
from utils.auth import require_admin
import os
import shutil
from config import settings

router = APIRouter()

@router.get("/")
async def list_images(
    category: str | None = None,
    featured_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    query = select(GalleryImage)
    
    if category:
        query = query.where(GalleryImage.category == category)
    if featured_only:
        query = query.where(GalleryImage.featured == True)
    
    query = query.order_by(GalleryImage.order, GalleryImage.created_at.desc())
    result = await db.execute(query)
    images = result.scalars().all()
    
    return [
        {
            "id": img.id,
            "title": img.title,
            "caption": img.caption,
            "url": img.url,
            "category": img.category,
            "featured": img.featured,
            "order": img.order
        }
        for img in images
    ]

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    title: str | None = None,
    caption: str | None = None,
    category: str | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    # Validate file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(400, "Fichier trop grand (max 5MB)")
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Create database record
    image = GalleryImage(
        title=title,
        caption=caption,
        filename=filename,
        url=f"/uploads/{filename}",
        category=category
    )
    
    db.add(image)
    await db.commit()
    await db.refresh(image)
    
    return {
        "id": image.id,
        "url": image.url,
        "message": "Image téléchargée avec succès"
    }

@router.patch("/{image_id}")
async def update_image(
    image_id: int,
    title: str | None = None,
    caption: str | None = None,
    category: str | None = None,
    order: int | None = None,
    featured: bool | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    image = await db.get(GalleryImage, image_id)
    if not image:
        raise HTTPException(404, "Image non trouvée")
    
    if title is not None:
        image.title = title
    if caption is not None:
        image.caption = caption
    if category is not None:
        image.category = category
    if order is not None:
        image.order = order
    if featured is not None:
        image.featured = featured
    
    await db.commit()
    
    return {"message": "Image mise à jour avec succès"}

@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    image = await db.get(GalleryImage, image_id)
    if not image:
        raise HTTPException(404, "Image non trouvée")
    
    # Delete file
    file_path = os.path.join(settings.UPLOAD_DIR, image.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    await db.delete(image)
    await db.commit()
    
    return {"message": "Image supprimée avec succès"}

from datetime import datetime
