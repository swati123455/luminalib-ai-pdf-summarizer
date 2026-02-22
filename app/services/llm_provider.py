import ollama

class LLMProvider:

    async def summarize(self, text: str) -> str:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "user", "content": text}
            ]
        )

        return response["message"]["content"]
