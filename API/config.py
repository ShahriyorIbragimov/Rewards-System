from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///database.db"
    DEBUG: bool = False
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()