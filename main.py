from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from .extract_features import (
    extract_audio_features,
    extract_features_from_directory,
)
from .models.audio_features import AudioFeatures
from .routes import last_fm_router
from .settings import Settings

settings = Settings()

DATABASE_URL = "sqlite:///./audio_features.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


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


@app.post("/extract-features/upload")
async def upload_and_extract(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
    """
    Upload an audio file and extract its features.

    Supported formats: .wav, .mp3, .flac, .m4a, .ogg

    Returns the extracted features saved to the database.
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Read the uploaded file
        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(status_code=400, detail="File is empty")

        # Extract features
        features = extract_audio_features(audio_bytes, file.filename)

        # Save to database
        session.add(features)
        session.commit()
        session.refresh(features)

        return {
            "status": "success",
            "message": f"Features extracted from {file.filename}",
            "data": features,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing audio file: {str(e)}"
        )


@app.post("/extract-features/file")
def extract_from_file(filepath: str, session: Session = Depends(get_session)):
    """
    Extract features from an audio file at a given file path.

    Args:
        filepath: Absolute or relative path to the audio file

    Returns the extracted features saved to the database.
    """
    try:
        # Extract features
        features = extract_audio_features(filepath)

        # Save to database
        session.add(features)
        session.commit()
        session.refresh(features)

        return {
            "status": "success",
            "message": f"Features extracted from {filepath}",
            "data": features,
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing audio file: {str(e)}"
        )


@app.post("/extract-features/directory")
def extract_from_directory(directory: str, session: Session = Depends(get_session)):
    """
    Extract features from all audio files in a directory.

    Args:
        directory: Path to directory containing audio files

    Returns list of extracted features, all saved to the database.
    """
    try:
        # Extract features from all files in directory
        all_features = extract_features_from_directory(directory)

        if not all_features:
            raise HTTPException(
                status_code=400,
                detail=f"No audio files found in directory: {directory}",
            )

        # Save all to database
        for features in all_features:
            session.add(features)

        session.commit()

        # Refresh all entries
        for features in all_features:
            session.refresh(features)

        return {
            "status": "success",
            "message": f"Extracted features from {len(all_features)} files",
            "count": len(all_features),
            "data": all_features,
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing directory: {str(e)}"
        )


@app.get("/features")
def get_all_features(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Get all extracted audio features with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
    """
    features = session.query(AudioFeatures).offset(skip).limit(limit).all()
    total = session.query(AudioFeatures).count()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "count": len(features),
        "data": features,
    }


@app.get("/features/{feature_id}")
def get_feature_by_id(feature_id: int, session: Session = Depends(get_session)):
    """
    Get audio features by ID.

    Args:
        feature_id: The ID of the audio features record
    """
    features = (
        session.query(AudioFeatures).filter(AudioFeatures.id == feature_id).first()
    )

    if not features:
        raise HTTPException(status_code=404, detail="Features not found")

    return features


@app.get("/features/filename/{filename}")
def get_features_by_filename(filename: str, session: Session = Depends(get_session)):
    """
    Get audio features by filename.

    Args:
        filename: The filename to search for
    """
    features = (
        session.query(AudioFeatures).filter(AudioFeatures.filename == filename).all()
    )

    if not features:
        raise HTTPException(
            status_code=404, detail=f"No features found for filename: {filename}"
        )

    return {"count": len(features), "data": features}
