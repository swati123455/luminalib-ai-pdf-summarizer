from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    async def save(self, file, filename: str) -> str:
        pass