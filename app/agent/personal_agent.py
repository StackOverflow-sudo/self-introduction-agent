from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

from app.agent.tools import get_profile, get_skills, search_projects
from app.core.config import settings

TOOLS = [get_profile, get_skills, search_projects]
TOOLS_MAP = {t.name: t for t in TOOLS}

SYSTEM = "你是小王的数字分身，负责介绍他的作品、技能和经历。回答要简洁、真诚，不要编造。"


def build_llm():
    return ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    ).bind_tools(TOOLS)


def chat(question: str, history: list[dict] | None = None) -> str:
    llm = build_llm()

    messages = [{"role": "system", "content": SYSTEM}]
    if history:
        messages.extend(history)          # 历史：[{"role":"user","content":...}, ...]
    messages.append({"role": "user", "content": question})

    ai = llm.invoke(messages)
    while ai.tool_calls:
        messages.append(ai)
        for tc in ai.tool_calls:
            result = TOOLS_MAP[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        ai = llm.invoke(messages)
    return ai.content