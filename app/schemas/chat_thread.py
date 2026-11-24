from pydantic import BaseModel


class ThreadSummary(BaseModel):
    thread_id: str
    checkpoint_count: int


class ThreadMessage(BaseModel):
    role: str
    content: str


class ThreadDetail(BaseModel):
    thread_id: str
    messages: list[ThreadMessage]