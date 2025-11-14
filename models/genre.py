from typing import Any, Dict, List, Optional

from sqlalchemy import JSON
from sqlmodel import Field
from sqlmodel.main import Relationship

from .base import Base
from .tag import Tag


class Genre(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    tags: List["Tag"] = Relationship(back_populates="genre")
    sub_genres: List["SubGenre"] = Relationship(back_populates="genre")


class SubGenre(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    genre_id: int | None = Field(default=None, foreign_key="genre.id")
    genre: Optional[Genre] = Relationship(back_populates="sub_genres")

    parent_subgenre_id: Optional[int] = Field(
        default=None, foreign_key="subgenre.id"
    )

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
