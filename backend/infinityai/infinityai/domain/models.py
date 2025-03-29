from enum import Enum
from pydantic import BaseModel


class LLMModelEnum(str, Enum):
    DEEPSEEK_R1 = "deepseek/deepseek-r1"


class LLMRequestModel(BaseModel):
    role: str
    prompt: str


class LLMHttpRequestMessageModel(BaseModel):
    role: str
    content: str


class LLMHttpRequestDataModel(BaseModel):
    model: LLMModelEnum
    messages: list[LLMHttpRequestMessageModel]
    stream: bool = True


class LLMHttpRequestModel(BaseModel):
    data: LLMHttpRequestDataModel
    stream: bool = True
