from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500, description="用户消息")
    thread_id: str | None = Field(default=None, description="会话ID，不传则新建")


class ChatResponse(BaseModel):
    reply: str
    thread_id: str

