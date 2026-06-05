# app/core/config.py
"""
Application configuration using Pydantic Settings.
Reads values from the .env file automatically.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    All application settings are read from environment variables.
    Pydantic Settings will look for a .env file automatically.
    """

    # ── Project metadata ──────────────────────────────────────────────────────
    PROJECT_NAME: str = Field(default="Advanced Student Management System")
    API_V1_STR: str = Field(default="/api/v1")

    # ── PostgreSQL connection parts ───────────────────────────────────────────
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_DB: str = Field(default="student_erp")

    # ── Computed sync URL (used by SQLAlchemy engine & Alembic) ───────────────
    @property
    def DATABASE_URL(self) -> str:
        """
        Synchronous PostgreSQL URL.
        Uses psycopg2 driver — required by Alembic (it does NOT support asyncpg).
        """
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        # Tell Pydantic Settings to read from the .env file in the project root
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a single shared instance — import this everywhere
settings = Settings()