from huggingface_hub import ChatCompletionInputMessage

from infinityai.domain.models import LLMRequestModel


class LLMMaper:
    def to_request(self, entity: LLMRequestModel) -> ChatCompletionInputMessage:
        return ChatCompletionInputMessage(
            content=entity.prompt,
            role=entity.role,
        )
