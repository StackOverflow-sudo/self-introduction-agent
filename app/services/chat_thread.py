def normalize_content(content) -> str:
    """把 messages.content 统一转成字符串（兼容 str / list / dict）。"""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(item.get("text") or item.get("content") or "")
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


class ChatThreadService:
    def __init__(self, agent):
        self.agent = agent

    def list_threads(self) -> list[dict]:
        counts: dict[str, int] = {}
        for cpt in self.agent.checkpointer.list(None):
            tid = cpt.config["configurable"]["thread_id"]
            counts[tid] = counts.get(tid, 0) + 1
        return [
            {"thread_id": tid, "checkpoint_count": n}
            for tid, n in counts.items()
        ]

    def get_thread(self, thread_id: str) -> list[dict]:
        config = {"configurable": {"thread_id": thread_id}}
        state = self.agent.get_state(config)
        messages = state.values.get("messages", [])

        result = []
        for m in messages:
            role = "user" if type(m).__name__ == "HumanMessage" else "assistant"
            result.append({"role": role, "content": normalize_content(m.content)})
        return result

    def delete_thread(self, thread_id: str) -> bool:
        config = {"configurable": {"thread_id": thread_id}}
        state = self.agent.get_state(config)
        if not state.values:
            return False
        self.agent.checkpointer.delete_thread(thread_id)
        return True