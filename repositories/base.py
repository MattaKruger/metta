from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic, List

from sqlmodel import SQLModel
from pydantic import BaseModel

T = TypeVar("T", BaseModel | SQLModel)


class Repository(ABC):
    @abstractmethod
    def create(self, model: T) -> T:
        pass

    @abstractmethod
    def create_many(self, model: List[T]) -> List[T]:
        pass

    @abstractmethod
    def delete(self, model_id: int) -> None:
        pass
