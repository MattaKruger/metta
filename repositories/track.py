from typing import List

from sqlmodel import Session

from ..models.track import Track
from .base import Repository


class TrackRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, model: Track) -> Track:
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return model

    def create_many(self, model: List[Track]) -> List[int]:
        pass

    def delete(self, model_id: int) -> None:
        self.session.delete(model_id)
        self.session.commit()
