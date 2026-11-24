from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.chat_thread import ThreadDetail, ThreadSummary
from app.services.chat_thread import ChatThreadService

router = APIRouter(prefix="/api/chat/threads", tags=["chat-threads"])


def get_thread_service(request: Request) -> ChatThreadService:
    return ChatThreadService(request.app.state.agent)


@router.get("", response_model=list[ThreadSummary])
def list_threads(svc: ChatThreadService = Depends(get_thread_service)):
    return svc.list_threads()


@router.get("/{thread_id}", response_model=ThreadDetail)
def get_thread(thread_id: str, svc: ChatThreadService = Depends(get_thread_service)):
    return {"thread_id": thread_id, "messages": svc.get_thread(thread_id)}


@router.delete("/{thread_id}")
def delete_thread(thread_id: str, svc: ChatThreadService = Depends(get_thread_service)):
    if not svc.delete_thread(thread_id):
        raise HTTPException(status_code=404, detail="thread not found")
    return {"ok": True}