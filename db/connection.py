from abc import ABC, abstractmethod


class DatabaseConnection(ABC):
    """Interface for database/chromadb connections"""

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        pass
