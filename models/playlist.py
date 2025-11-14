from typing import Dict, Generic, List, TypeVar

from sqlmodel import Field

from .base import Base
from .track import Track


class Playlist(Base):
    name: str = Field(default="")
    tracks: List[Track] = Field(default_factory=list())
