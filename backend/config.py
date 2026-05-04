from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./haiti_rehcare.db"
    SECRET_KEY: str = "your-secret-key-change-in-production-minimum-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    ADMIN_EMAIL: str = "admin@haiti-rehcare.org"
    ADMIN_PASSWORD: str = "ChangeThisPassword123!"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5_000_000  # 5MB
    
    class Config:
        env_file = ".env"

settings = Settings()
