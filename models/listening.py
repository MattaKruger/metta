from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship

from .base import Base
from .tag import Tag
from .track import Track


class ScrobbleSource(Enum, str):
    LAST_FM = "lastfm"
    LISTEN_BRAINZ = "listenbrainz"
    NONE = "none"


class ListeningEvent(Base, table=True):
    track_id: int = Field(foreign_key="tracks.id")

    timestamp: int = Field(default=0)
    duration: float = Field(default=0.0)
    skip_timestamp: Optional[datetime] = Field(default=None)

    loved: bool = Field(default=False)
    skipped: bool = Field(default=False)

    skipped_reason: Optional[str] = Field(default=None)

    source_url: Optional[str] = Field(default=None)
    scrobble_source: Optional[ScrobbleSource] = Field(default=None)

    # Relationships
    track: Track = Relationship(back_populates="event")

    def full_duration(self) -> bool:
        # have to adjust for scrobble delay, getting the new scrobble takes a few seconds
        return self.duration_played == self.track.duration

    def remainder(self) -> Optional[int]:
        return self.timestamp - self.skip_timestamp if self.skip_timestamp is not None else None

# TODO,
# figure out how to store scrobbling history efficiently.
#   - hourly/daily/weekly?
#

class ListeningSession(Base, table=True):
    listening_events: List[ListeningEvent] = Relationship(back_populates="session")

    start_time: int = Field()
    end_time: int = Field()

    tags: List[Tag] = Relationship(back_populates="session")
