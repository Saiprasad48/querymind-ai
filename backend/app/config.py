import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    APP_NAME: str = "QueryMind AI"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/querymind"
    )
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
settings = Settings()