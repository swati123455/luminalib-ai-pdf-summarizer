from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    async def summarize(self, text:str) -> str:
        pass
