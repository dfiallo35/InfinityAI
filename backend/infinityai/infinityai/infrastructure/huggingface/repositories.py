from typing import Iterable

from huggingface_hub import InferenceClient
from huggingface_hub import ChatCompletionStreamOutput

from infinityai.domain.models import LLMRequestModel
from infinityai.infrastructure.huggingface.mappers import LLMMaper
from infinityai.settings import settings


MODEL = "meta-llama/Llama-3.2-11B-Vision-Instruct"
HUGGINGFACE_TOKEN = settings.HUGGINGFACE_TOKEN


class LLMClient:
    def __init__(self):
        self.setup_client()

    def setup_client(self):
        self.client = InferenceClient(
            api_key=HUGGINGFACE_TOKEN,
        )

    def generate(self, message: LLMRequestModel) -> Iterable[ChatCompletionStreamOutput]:
        message_request = LLMMaper().to_request(message)
        if not isinstance(message_request, list):
            message_request = [message_request]

        stream = self.client.chat.completions.create(
            model=MODEL,
            messages=message_request,
            max_tokens=500,
            stream=True,
        )
        return stream
