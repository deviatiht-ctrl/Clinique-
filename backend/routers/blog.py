from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.blog import BlogPost
from utils.auth import require_admin
from datetime import datetime

router = APIRouter()

@router.get("/")
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    published_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    query = select(BlogPost)
    
    if published_only:
        query = query.where(BlogPost.published == True)
    if category:
        query = query.where(BlogPost.category == category)
    
    query = query.order_by(BlogPost.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    posts = result.scalars().all()
    
    return [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "category": p.category,
            "excerpt": p.excerpt or p.content[:200] + "...",
            "cover_image": p.cover_image,
            "author": p.author,
            "published": p.published,
            "views": p.views,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in posts
    ]

@router.get("/{slug}")
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(404, "Article non trouvé")
    
    # Increment views
    post.views += 1
    await db.commit()
    
    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "category": post.category,
        "content": post.content,
        "cover_image": post.cover_image,
        "author": post.author,
        "published": post.published,
        "views": post.views,
        "created_at": post.created_at.isoformat() if post.created_at else None
    }

@router.post("/")
async def create_post(
    title: str,
    slug: str,
    category: str,
    content: str,
    excerpt: str | None = None,
    cover_image: str | None = None,
    author: str | None = None,
    published: bool = False,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    # Check if slug exists
    result = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
    if result.scalar_one_or_none():
        raise HTTPException(400, "Un article avec ce slug existe déjà")
    
    post = BlogPost(
        title=title,
        slug=slug,
        category=category,
        content=content,
        excerpt=excerpt,
        cover_image=cover_image,
        author=author,
        published=published,
        published_at=datetime.utcnow() if published else None
    )
    
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    return {"id": post.id, "message": "Article créé avec succès"}

@router.patch("/{post_id}")
async def update_post(
    post_id: int,
    title: str | None = None,
    content: str | None = None,
    excerpt: str | None = None,
    cover_image: str | None = None,
    published: bool | None = None,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    post = await db.get(BlogPost, post_id)
    if not post:
        raise HTTPException(404, "Article non trouvé")
    
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    if excerpt is not None:
        post.excerpt = excerpt
    if cover_image is not None:
        post.cover_image = cover_image
    if published is not None:
        post.published = published
        if published and not post.published_at:
            post.published_at = datetime.utcnow()
    
    await db.commit()
    
    return {"message": "Article mis à jour avec succès"}

@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    post = await db.get(BlogPost, post_id)
    if not post:
        raise HTTPException(404, "Article non trouvé")
    
    await db.delete(post)
    await db.commit()
    
    return {"message": "Article supprimé avec succès"}
