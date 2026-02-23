from ollama import Client

class LLMProvider:
    def __init__(self):
        self.client = Client(host="http://ollama:11434")

    async def summarize(self, text: str):

        response = self.client.chat(
            model="tinyllama",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following:\n{text}"
                }
            ],
        )

        return response["message"]["content"]
