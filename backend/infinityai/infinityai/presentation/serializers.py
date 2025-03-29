from pydantic import BaseModel

from infinityai.domain.models import LLMRequestModel
from infinityai.domain.models import LLMHttpRequestModel
from infinityai.domain.models import LLMHttpRequestDataModel
from infinityai.domain.models import LLMHttpRequestMessageModel
from infinityai.domain.models import LLMModelEnum


class LLMInput(BaseModel):
    role: str = "user"
    prompt: str


class LLMMapper:
    def to_entity(self, entity: LLMInput) -> LLMRequestModel:
        return LLMRequestModel(**entity.model_dump())


class LLMHttpRequestInput(BaseModel):
    content: str
    model: LLMModelEnum = LLMModelEnum.DEEPSEEK_R1


class LLMHttpRequestMapper:
    def to_entity(self, entity: LLMHttpRequestInput) -> LLMHttpRequestModel:
        return LLMHttpRequestModel(
            data=LLMHttpRequestDataModel(
                model=entity.model,
                messages=[
                    LLMHttpRequestMessageModel(
                        role="user",
                        content=entity.content,
                    )
                ],
            )
        )
