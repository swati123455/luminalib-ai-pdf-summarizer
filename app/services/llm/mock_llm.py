import asyncio
from .base import LLMInterface

class MockLLM(LLMInterface):
    async def summarize(self, text:str) -> str:
        await asyncio.sleep(3)

        return f"Auto Summary: {text[:120]}..."