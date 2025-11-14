from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel
from track import Track

from .album import Album
from .base import Base
from .genre import Genre


class ArtistType(Enum, str):
    PERSON = "person"
    GROUP = "group"


class Artist(Base, table=True):
    name: str = Field(default="", max_length=120, index=True)
    artist_type: ArtistType = Field(default=ArtistType.PERSON, index=True)
    country: Optional[str] = Field(default=None, max_length=50, index=True)

    musicbrainz_id: Optional[str] = Field(default=None, max_length=50, index=True)

    # Relationships
    tracks: List[Track] = Relationship(
        back_populates="artists", sa_relationship_kwargs={"lazy": "selectin"}
    )
    albums: List[Album] = Relationship(
        back_populates="artists", sa_relationship_kwargs={"lazy": "selectin"}
    )
    genres: List[Genre] = Relationship(
        back_populates="artists", link_model="ArtistGenre"
    )
