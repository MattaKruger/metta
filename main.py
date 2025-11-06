from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session, SQLModel

from .db import engine, get_session

from .routes import last_fm_router, audio_features_router
from .settings import Settings


settings = Settings()


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()

    yield

    print("Shutting down...")


app = FastAPI(
    title="Audio Features API",
    description="Extract and store audio features using librosa",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(last_fm_router)
app.include_router(audio_features_router)


@app.get("/")
def get_root():
    """Root endpoint."""
    return {
        "message": "Welcome to Audio Features API",
        "status": "API is running",
    }


@app.get("/health")
def health_check():
    """Health check endpoint to verify database connection."""
    try:
        with Session(engine) as session:
            session.exec("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
