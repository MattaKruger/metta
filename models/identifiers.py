from typing import Optional
from sqlmodel import Field

from .base import Base


class Identifiers(Base, table=False):
    musicbrainz_id: Optional[str] = Field(default=None, max_length=40)
