from datetime import datetime
from sqlmodel import SQLModel, Field


class Base(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
