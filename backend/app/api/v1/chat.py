from http.client import HTTPException
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.responses import StreamingResponse
from app.api.deps import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import LLMError, ChatService
import json

router = APIRouter(tags=['chat'])


@router.post('/chat')
def chat(req: ChatRequest, service: ChatService = Depends(get_chat_service)):
    try:
        result = service.answer(req.message)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=f'LLM error: {e}')
    return ChatResponse(
        answer=result.answer,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
    )


@router.post('/chat/stream')
def chat_stream(req: ChatRequest, service: ChatService = Depends(get_chat_service)):
    def events():
        for text in service.stream_answer(req.message):
            yield f'data: {json.dumps({"text": text})}\n\n'
        yield 'data: [DONE]\n\n'

    return StreamingResponse(events(), media_type='text/event-stream')
