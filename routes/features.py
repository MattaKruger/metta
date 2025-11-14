from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session

from ..db import get_session
from ..extract_features import (
    extract_audio_features,
    extract_features_from_directory,
)
from ..models.audio_features import AudioFeatures

router = APIRouter(
    prefix="/features",
    tags=["features"],
    dependencies=[Depends(get_session)],
    responses={
        404: {"Description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Oopsie"},
    },
)


@router.post("/extract-features/upload")
async def upload_and_extract(
    file: UploadFile = File(...), session: Session = Depends(get_session)
):
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


@router.post("/extract-features/file")
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


@router.post("/extract-features/directory")
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


@router.get("/features")
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


@router.get("/features/{feature_id}")
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


@router.get("/features/filename/{filename}")
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
            status_code=404,
            detail=f"No features found for filename: {filename}",
        )

    return {"count": len(features), "data": features}
