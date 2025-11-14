from typing import Any, Dict, List, Optional

from sqlalchemy import JSON
from sqlmodel import Field
from sqlmodel.main import Relationship

from .base import Base
from .tag import Tag
from .playlist import Playlist


class Genre(Base, table=True):
    name: str = Field(..., min_length=1, max_length=100, index=True)
    description: Optional[str] = Field(default=None, max_length=500)

    tags: List["Tag"] = Relationship(back_populates="genre")
    sub_genres: List["SubGenre"] = Relationship(back_populates="genre")
    playlists: List["Playlist"] = Relationship(back_populates="genres")
    is_active: bool = Field(default=True)

    def has_sub_genres(self):
        return len(self.sub_genres) > 0


class SubGenre(Base, table=True):
    name: str = Field(..., min_length=1, max_length=100, index=True)
    description: Optional[str] = Field(default=None, max_length=500)

    genre_id: int | None = Field(default=None, foreign_key="genre.id")
    genre: Optional[Genre] = Relationship(back_populates="sub_genres")

    parent_subgenre_id: Optional[int] = Field(default=None, foreign_key="subgenre.id")

    # Textual characteristics
    characteristics: List[str] = Field(
        default_factory=list, sa_column_kwargs={"type_": JSON}
    )
    # TODO: figure out how to generate relevant characteristics, last.fm api might be a good start.
    # - Store main genre in vorbis comments. Use musicbrainzID to query the last.fm api to get user generated tags.
    # - Store genres and weights, should be Dict[str, float]

    audio_features: Dict[str, Any] = Field(
        default_factory=dict, sa_column_kwargs={"type_": JSON}
    )

    is_active: bool = Field(default=True)
    order: int = Field(default=0)
