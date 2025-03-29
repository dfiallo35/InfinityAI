from infinityai.domain.models import LLMHttpRequestModel


class LLMHttpRequestMapper:
    def to_request(self, entity: LLMHttpRequestModel) -> dict:
        return {
            "data": entity.data.model_dump_json(),
            "stream": entity.stream,
        }
