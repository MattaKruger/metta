from sqlmodel import Field, SQLModel


class TagTracks(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    tag_id: int = Field(foreign_key="tag.id")
    track_id: int = Field(foreign_key="track.id")
