import json
import requests
from typing import AsyncGenerator

from infinityai.domain.models import LLMHttpRequestModel
from infinityai.infrastructure.openrouter.mappers import LLMHttpRequestMapper
from infinityai.settings import settings


OPENROUTER_URL = settings.OPENROUTER_URL
OPENROUTER_API_KEY = settings.OPENROUTER_API_KEY


class LLMHttpRepository:
    async def generate(self, request: LLMHttpRequestModel) -> AsyncGenerator[str, None]:
        mapper = LLMHttpRequestMapper()
        request_dict = mapper.to_request(entity=request)
        try:
            response = requests.post(
                **request_dict,
                url=OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code != 200:
                raise Exception(f"Error generating response: {response.status_code}")
            

            for line in response.iter_lines():
                if not line:
                    continue

                decoded_line = line.decode("utf-8")
                if decoded_line == 'data: [DONE]':
                    break
                if decoded_line.startswith(":"):
                    continue
                if decoded_line.startswith("data:"):
                    decoded_line = decoded_line[5:]

                data = json.loads(decoded_line)
                if data.get("choices", None):
                    delta_content = data["choices"][0]["delta"].get("content", "")
                    if delta_content:
                        yield delta_content

        except Exception as e:
            raise e
