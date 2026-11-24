import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.agent.knowledge import get_last_refs
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_chat_service(request: Request) -> ChatService:
    # 从 app.state 拿全局 agent（lifespan 创建）
    return ChatService(request.app.state.agent)


@router.post("", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest, svc: ChatService = Depends(get_chat_service)):
    reply, thread_id = svc.chat(req.message, req.thread_id)
    return ChatResponse(reply=reply, thread_id=thread_id)


@router.post("/stream")
def chat_stream(req: ChatRequest, svc: ChatService = Depends(get_chat_service)):
    def gen():
        try:
            for text in svc.stream(req.message, req.thread_id):
                yield f"data: {json.dumps({'text': text}, ensure_ascii=False)}\n\n"

            # 引用溯源：把检索到的父块片段以 custom 事件推给前端
            refs = get_last_refs()
            if refs:
                yield f"event: references\ndata: {json.dumps(refs, ensure_ascii=False)}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
