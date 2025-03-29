import asyncio
from typing import AsyncGenerator

from infinityai.domain.models import LLMRequestModel
from infinityai.domain.models import LLMHttpRequestModel
from infinityai.infrastructure.huggingface.repositories import LLMClient
from infinityai.infrastructure.openrouter.repositories import LLMHttpRepository


class StreamLLMService:
    def __init__(self):
        self.llm_client = LLMClient()
    
    async def generate_response(self, message: LLMRequestModel):
        try:
            stream = self.llm_client.generate(message=message)
            for chunk in stream:
                yield chunk.choices[0].delta.content
                await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Error generating response: {e}")
            yield "[ERROR] An issue occurred while generating the response."


class LLMHttpStreamService:
    def __init__(self):
        self.llm_client = LLMHttpRepository()
    
    async def generate_response(self, message: LLMHttpRequestModel) -> AsyncGenerator[str, None]:
        try:
            async for chunk in self.llm_client.generate(request=message):
                yield chunk
                await asyncio.sleep(0.01)
        except Exception as e:
            yield "[ERROR] An issue occurred while generating the response."
