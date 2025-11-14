from sqlalchemy.orm.relationships import foreign
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Index

from .base import Base
from .genre import Genre
from .album import Album
from .artist import Artist
from .audio_features import AudioFeatures


class Track(Base, table=True):
    name: str = Field(default="", index=True)
    artists: List[Artist] = Relationship(back_populates="tracks", index=True)
    album: Optional[Album] = Relationship(back_populates="tracks")
    duration: float = Field(default=0.0)

    audio_features_id: Optional[int] = Field(
        default=None, foreign_key="audio_features.id"
    )
    audio_features: AudioFeatures = Relationship(back_populates="tracks")

    genre: Genre = Relationship(back_populates="tracks")
