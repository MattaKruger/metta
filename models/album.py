from typing import Optional, List
from sqlmodel import Relationship, Field

from .base import Base
from .track import Track
from .artist import Artist


class Album(Base, table=True):
    description: str = Field(default="", max_length=500)
    tracks: List[Track] = Relationship(back_populates="album")
    artists: List[Artist] = Relationship(back_populates="album")

    def get_duration(self) -> int:
        return sum(track.duration for track in self.tracks)

    def get_artists(self) -> str:
        return ", ".join(artist.name for artist in self.artists)
