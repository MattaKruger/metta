from sqlmodel import Field, SQLModel

from .base import Base
from .genre import Genre


class Track(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="")
    artist: str = Field(default="")
    duration: float = Field(default=0.0)
    genre: Genre
