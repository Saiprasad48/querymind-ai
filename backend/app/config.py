import os
from dotenv import load_dotenv

load_dotenv()

def get_allowed_origins() -> list[str]:
    raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
    return [
        origin.strip()
        for origin in raw_origins.split(",")
        if origin.strip()
    ]
class Settings:
    APP_NAME: str = "QueryMind AI"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/querymind"
    )
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    ALLOWED_ORIGINS: list[str] = get_allowed_origins()
settings = Settings()