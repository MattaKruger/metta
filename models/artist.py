from sqlmodel import SQLModel


class Artist(SQLModel):
    id: int
    name: str
