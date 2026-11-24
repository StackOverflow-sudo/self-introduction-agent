from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.agent.knowledge import search_knowledge
from app.agent.tools import get_profile, get_skills, search_projects
from app.core.config import settings

TOOLS = [get_profile, get_skills, search_projects, search_knowledge]

SYSTEM = """你是小王的数字分身，负责介绍他的作品、技能和经历。
规则：
1. 只根据工具返回的数据回答，不要编造
2. 涉及他的笔记/文档内容时，用 search_knowledge 查
3. 回答简洁，不超过 3 句话
4. 不知道就直说"这个我还没有数据"
5. 用到 search_knowledge 的资料时，在相应句子末尾用 [1][2] 标注引用编号（编号见资料里的 [n]）
"""


def build_agent(checkpointer):
    """手写 LangGraph：模型节点 + 工具节点 + 条件边（等价于 create_react_agent）。"""
    llm = ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    ).bind_tools(TOOLS)

    def call_model(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM), *state["messages"]]
        resp = llm.invoke(messages)
        return {"messages": [resp]}

    graph = StateGraph(MessagesState)
    graph.add_node("model", call_model)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.add_edge(START, "model")
    # 条件边：模型要调工具 → tools；否则 → END
    graph.add_conditional_edges("model", tools_condition, {"tools": "tools", END: END})
    # 工具执行完 → 回到模型（工具循环）
    graph.add_edge("tools", "model")

    return graph.compile(checkpointer=checkpointer)
