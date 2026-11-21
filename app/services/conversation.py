from sqlalchemy.orm import Session

from app.repositories.conversation import ConversationRepository
from app.schemas.conversation import ConversationCreate


class ConversationService:
    def __init__(self, db: Session):
        self.repo = ConversationRepository(db)

    def list(self):
        return self.repo.list()

    def get(self, conversation_id: int):
        return self.repo.get(conversation_id)

    def create(self, data: ConversationCreate):
        return self.repo.create(data)

    def rename(self, conversation_id: int, title: str):
        return self.repo.rename(conversation_id, title)

    def delete(self, conversation_id: int):
        return self.repo.delete(conversation_id)