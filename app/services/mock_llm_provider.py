class MockLLMProvider:
    async def summarize(self, text:str) -> str:
        print("Mock LLM used")

        import asyncio
        await asyncio.sleep(1)

        return (
            "This is Mock AI generated summary."
            "The document discusses backend architecture, API's,"
            "authentication, and system design concepts."
        )