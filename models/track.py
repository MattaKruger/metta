from typing import List, Optional

from sqlalchemy import Index
from sqlmodel import Field, Relationship, SQLModel

from .album import Album
from .artist import Artist
from .audio_features import AudioFeatures
from .base import Base
from .genre import Genre


class Track(Base, table=True):
    name: str = Field(default="", index=True)
    duration: float = Field(default=0.0)
    listen_count: int = Field(default=0)
    skip_count: int = Field(default=0)

    album_position: Optional[int] = Field(default=None)

    musicbrainz_id: Optional[str] = Field(default=None, index=True)

    audio_features_id: Optional[int] = Field(
        default=None, foreign_key="audio_features.id"
    )

    genres: List[Genre] = Relationship(back_populates="tracks")
    album: Optional[Album] = Relationship(back_populates="tracks")
    audio_features: AudioFeatures = Relationship(back_populates="track")
    artists: List[Artist] = Relationship(back_populates="tracks", index=True)


class TrackStructure(Track, table=True):
    pass

# TODO:
# Do i want to track my own listening_history, i can use the listenbrainz/last.fm scrobbler to save my listening history.


track = [
    {'0': 'kick', '1': 'kick', '2': 'kick', '3': 'kick'},
    {'0': ''}
]
