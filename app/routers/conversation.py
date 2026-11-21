from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.conversation import ConversationCreate, ConversationOut, ConversationUpdate
from app.services.conversation import ConversationService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


def get_service(db: Session = Depends(get_db)) -> ConversationService:
    return ConversationService(db)


@router.get("", response_model=list[ConversationOut])
def list_conversations(svc: ConversationService = Depends(get_service)):
    return svc.list()


@router.post("", response_model=ConversationOut, status_code=status.HTTP_201_CREATED)
def create_conversation(
    data: ConversationCreate,
    svc: ConversationService = Depends(get_service),
):
    return svc.create(data)


@router.put("/{conversation_id}", response_model=ConversationOut)
def rename_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    svc: ConversationService = Depends(get_service),
):
    obj = svc.rename(conversation_id, data.title)
    if obj is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return obj


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    svc: ConversationService = Depends(get_service),
):
    if not svc.delete(conversation_id):
        raise HTTPException(status_code=404, detail="conversation not found")