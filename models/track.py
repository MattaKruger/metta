from sqlmodel import Field, SQLModel


class Track(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(default="")
    artist: str = Field(default="")
    duration: float = Field(default=0.0)
    genre: str = Field(default="")
