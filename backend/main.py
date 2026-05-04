from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import engine
import models
from routers import auth, patients, appointments, blog, gallery, team, donations, settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(
    title="Haiti Reh-Care API",
    description="Backend for Haiti Reh-Care rehabilitation center",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
app.include_router(blog.router, prefix="/blog", tags=["blog"])
app.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(donations.router, prefix="/donations", tags=["donations"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])

@app.get("/")
async def root():
    return {"message": "Haiti Reh-Care API", "status": "operational"}

@app.get("/stats")
async def get_stats():
    # Return public stats for homepage
    return {
        "patients": 500,
        "appointments_completed": 800,
        "years": 10,
        "experts": 3
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
