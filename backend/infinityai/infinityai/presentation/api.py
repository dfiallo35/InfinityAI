import asyncio
from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from fastapi.responses import StreamingResponse

from infinityai.application.services import StreamLLMService
from infinityai.application.services import LLMHttpStreamService
from infinityai.presentation.serializers import LLMInput
from infinityai.presentation.serializers import LLMHttpRequestInput
from infinityai.presentation.serializers import LLMMapper
from infinityai.presentation.serializers import LLMHttpRequestMapper

router = APIRouter()


@router.post("/huggingface/generate")
async def sse_huggingface_generate(
    model_in: LLMInput,
    service: StreamLLMService = Depends(),
    mapper: LLMMapper = Depends()
):
    llm_request_entity = mapper.to_entity(entity=model_in)
    return StreamingResponse(service.generate_response(llm_request_entity), media_type="text/event-stream")


@router.post("/openrouter/generate")
async def sse_openrouter_generate(
    model_in: LLMHttpRequestInput,
    service: LLMHttpStreamService = Depends(),
    mapper: LLMHttpRequestMapper = Depends()
):
    llm_request_entity = mapper.to_entity(entity=model_in)
    return StreamingResponse(service.generate_response(llm_request_entity), media_type="text/event-stream")


# WS
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    service: StreamLLMService = Depends(),
    mapper: LLMMapper = Depends()
):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()

            llm_request = mapper.to_entity(entity=LLMInput(prompt=data))
            
            async for chunk in service.generate_response(llm_request):
                await websocket.send_text(chunk)  # Stream response
                await asyncio.sleep(0.01)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket Error: {e}")
