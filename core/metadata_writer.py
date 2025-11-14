from pathlib import Path
from typing import Dict, Generic, List, TypeVar

from mutagen.flac import FLAC
from pydantic import BaseModel

from ..logging_config import logger

K = TypeVar("K", str)
V = TypeVar("V", str, float)


class Characteristics(BaseModel, Generic[K, V]):
    key: K
    value: V


class Features(BaseModel):
    characteristics: List[Characteristics]
    genres: List[str]
    key: str


class Metadata(BaseModel):
    title: str
    artist: str
    album: str
    year: int
    track_number: int
    duration: float


class MetadataWriter:
    def __init__(self, filepath: str):
        library = Path(filepath)

        logger.info(
            f"initializing metadata writer for {library} \n, loading {len(library.resolve())}"
        )

    def get_audio_features(self, filepath: str, key: str):
        audio = FLAC(filepath)
        logger.info(f"getting info for {audio.filename}, info {audio.info}")

        return Metadata(
            title=audio["title"].text[0],
            artist=audio["artist"].text[0],
            album=audio["album"].text[0],
            year=int(audio["date"].text[0]),
            track_number=int(audio["tracknumber"].text[0]),
            duration=audio.info.length,
        )

    def set_audio_features(self, filepath: str, features: Features):
        audio = FLAC(filepath)
        audio["characteristics"] = features.characteristics
        audio["genres"] = features.genres

        audio.save()

        logger.info(f"saved metadata for {audio.filename} ")
