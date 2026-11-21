from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Conversation]:
        return self.db.query(Conversation).order_by(Conversation.id.desc()).all()

    def get(self, conversation_id: int) -> Conversation | None:
        return self.db.get(Conversation, conversation_id)

    def create(self, data: ConversationCreate) -> Conversation:
        obj = Conversation(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def rename(self, conversation_id: int, title: str) -> Conversation | None:
        obj = self.get(conversation_id)
        if obj is None:
            return None
        obj.title = title
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, conversation_id: int) -> bool:
        obj = self.get(conversation_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True