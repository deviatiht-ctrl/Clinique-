from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.team import TeamMember
from utils.auth import require_admin

router = APIRouter()

@router.get("/")
async def list_team_members(
    featured_only: bool = False,
    db: AsyncSession = Depends(get_db)
):
    query = select(TeamMember)
    
    if featured_only:
        query = query.where(TeamMember.featured == True)
    
    query = query.order_by(TeamMember.order, TeamMember.id)
    result = await db.execute(query)
    members = result.scalars().all()
    
    return [
        {
            "id": m.id,
            "full_name": m.full_name,
            "role": m.role,
            "title": m.title,
            "bio": m.bio,
            "photo_url": m.photo_url,
            "certification": m.certification,
            "experience_years": m.experience_years,
            "featured": m.featured,
            "phone": m.phone,
            "email": m.email
        }
        for m in members
    ]

@router.get("/{member_id}")
async def get_team_member(member_id: int, db: AsyncSession = Depends(get_db)):
    member = await db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(404, "Membre non trouvé")
    
    return {
        "id": member.id,
        "full_name": member.full_name,
        "role": member.role,
        "title": member.title,
        "bio": member.bio,
        "photo_url": member.photo_url,
        "certification": member.certification,
        "experience_years": member.experience_years,
        "featured": member.featured,
        "phone": member.phone,
        "email": member.email
    }

@router.post("/")
async def create_team_member(
    full_name: str,
    role: str,
    title: str | None = None,
    bio: str | None = None,
    photo_url: str | None = None,
    certification: str | None = None,
    experience_years: int | None = None,
    featured: bool = False,
    phone: str | None = None,
    email: str | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    member = TeamMember(
        full_name=full_name,
        role=role,
        title=title,
        bio=bio,
        photo_url=photo_url,
        certification=certification,
        experience_years=experience_years,
        featured=featured,
        phone=phone,
        email=email
    )
    
    db.add(member)
    await db.commit()
    await db.refresh(member)
    
    return {"id": member.id, "message": "Membre ajouté avec succès"}

@router.patch("/{member_id}")
async def update_team_member(
    member_id: int,
    full_name: str | None = None,
    role: str | None = None,
    title: str | None = None,
    bio: str | None = None,
    photo_url: str | None = None,
    certification: str | None = None,
    experience_years: int | None = None,
    featured: bool | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    member = await db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(404, "Membre non trouvé")
    
    if full_name is not None:
        member.full_name = full_name
    if role is not None:
        member.role = role
    if title is not None:
        member.title = title
    if bio is not None:
        member.bio = bio
    if photo_url is not None:
        member.photo_url = photo_url
    if certification is not None:
        member.certification = certification
    if experience_years is not None:
        member.experience_years = experience_years
    if featured is not None:
        member.featured = featured
    
    await db.commit()
    
    return {"message": "Membre mis à jour avec succès"}

@router.delete("/{member_id}")
async def delete_team_member(
    member_id: int,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    member = await db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(404, "Membre non trouvé")
    
    await db.delete(member)
    await db.commit()
    
    return {"message": "Membre supprimé avec succès"}
