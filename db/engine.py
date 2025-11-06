from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from .settings import Settings

settings = Settings()
DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
