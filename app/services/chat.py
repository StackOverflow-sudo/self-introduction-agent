import uuid
from langchain_core.messages import AIMessage, AIMessageChunk

class ChatService:
    def __init__(self, agent):
        self.agent = agent

    def chat(self, message: str, thread_id: str | None = None) -> tuple[str, str]:
        # 没传 thread_id 就新建一个会话
        thread_id = thread_id or str(uuid.uuid4())

        config = {"configurable": {"thread_id": thread_id}}
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config,
        )
        reply = result["messages"][-1].content
        return reply, thread_id
    
    def stream(self, message: str, thread_id: str | None = None):
        """流式返回 token 块。"""
        thread_id = thread_id or str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}

        for chunk in self.agent.stream(
            {"messages": [{"role": "user", "content": message}]},
            config,
            stream_mode="messages",       # ← 逐 token
        ):
            msg, _meta = chunk
            if isinstance(msg, (AIMessage, AIMessageChunk)) and msg.content:
                yield msg.content