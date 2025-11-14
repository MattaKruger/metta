from typing import Dict, Generic, List, TypeVar, Optional

from sqlmodel import Field, Relationship

from .base import Base
from .track import Track
from .genre import Genre


class Playlist(Base):
    name: str = Field(default="", index=True, max_length=120)

    description: str = Field(default="", max_length=500)
    tracks: List[Track] = Field(default_factory=list())
    genres: Optional[List[Genre]] = Relationship(back_populates="playlists")
