from typing import Optional

from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship

from .genre import Genre


class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)

    genre_id: int | None = Field(default=None, foreign_key="genre.id")
    genre: Optional[Genre] = Relationship(back_populates="tags")
