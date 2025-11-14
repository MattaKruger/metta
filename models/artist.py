from typing import List

from sqlmodel import Field, Relationship, SQLModel
from track import Track

from .base import Base


class Artist(Base, table=True):
    name: str = Field(default="", max_length=120)
    tracks: List[Track] = Relationship(back_populates="artist")
    # What to do about various artist albums?
    #  - Do extra lookup for track/artist/album and store it like that?
    #  - Extra check on various artist album
    # What to do about grouping artists with genres?
