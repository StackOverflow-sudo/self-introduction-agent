"""主图：意图识别 → 路由到子图（ReAct / 兜底）。"""

from typing import Literal

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel

from app.agent.graph import build_agent
from app.core.config import settings


class Intent(BaseModel):
    intent: Literal["greeting", "skills", "portfolio", "knowledge", "contact", "other"]


class MainState(MessagesState):
    intent: str


def _llm() -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    )


def classify_node(state: MainState):
    """用结构化输出做意图分类。"""
    clf = _llm().with_structured_output(Intent, method="function_calling")
    last = state["messages"][-1].content
    r = clf.invoke(f"判断这句话属于哪类意图：{last}")
    return {"intent": r.intent}


def route(state: MainState) -> str:
    intent = state.get("intent", "other")
    # 前五类都交给 ReAct 子图（它带工具和人设），other 走兜底
    if intent in ("greeting", "skills", "portfolio", "contact", "knowledge"):
        return "react"
    return "fallback"


def fallback_node(state: MainState):
    return {
        "messages": [
            ("ai", "这个问题我还没有数据，可以问我技能、作品或笔记相关的内容～")
        ]
    }


def build_main_agent(checkpointer):
    """主图：classify → (react | fallback) → END。"""
    react_agent = build_agent(checkpointer)

    g = StateGraph(MainState)
    g.add_node("classify", classify_node)
    g.add_node("react", react_agent)          # 子图直接作为节点
    g.add_node("fallback", fallback_node)

    g.add_edge(START, "classify")
    g.add_conditional_edges(
        "classify", route, {"react": "react", "fallback": "fallback"}
    )
    g.add_edge("react", END)
    g.add_edge("fallback", END)

    return g.compile(checkpointer=checkpointer)
