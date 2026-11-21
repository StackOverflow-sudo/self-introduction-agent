from datetime import datetime

from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
    title: str = Field(default="新会话", max_length=100)


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)


class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}