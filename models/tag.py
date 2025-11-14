from typing import Optional

from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship

from .base import Base
from .genre import Genre


class Tag(Base, table=True):
    name: str = Field(max_length=255)

    genre_id: int | None = Field(default=None, foreign_key="genre.id")
    genre: Optional[Genre] = Relationship(back_populates="tags")
