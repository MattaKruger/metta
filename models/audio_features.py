from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class AudioFeatures(SQLModel, table=True):
    """
    SQLModel for storing extracted audio features.

    This model corresponds to the features extracted by extract_features.py,
    including spectral features, MFCCs, temporal characteristics, and more.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic metadata
    filename: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Basic audio info
    duration_seconds: float
    sample_rate_hz: int

    # Spectral features
    spectral_centroid_hz: float
    spectral_rolloff_hz: float

    # Temporal features
    zero_crossing_rate: float
    rms_energy: float

    # Tempo
    tempo_bpm: float

    # Chroma features
    chroma_energy: float

    # MFCC coefficients (13 coefficients)
    mfcc_0: float
    mfcc_1: float
    mfcc_2: float
    mfcc_3: float
    mfcc_4: float
    mfcc_5: float
    mfcc_6: float
    mfcc_7: float
    mfcc_8: float
    mfcc_9: float
    mfcc_10: float
    mfcc_11: float
    mfcc_12: float

    class Config:
        """SQLModel configuration."""

        json_schema_extra = {
            "example": {
                "filename": "sample_audio.wav",
                "duration_seconds": 30.5,
                "sample_rate_hz": 22050,
                "spectral_centroid_hz": 2500.0,
                "spectral_rolloff_hz": 5000.0,
                "zero_crossing_rate": 0.05,
                "rms_energy": 0.1,
                "tempo_bpm": 120.0,
                "chroma_energy": 0.8,
                "mfcc_0": 10.5,
                "mfcc_1": 5.2,
                "mfcc_2": 3.1,
            }
        }
