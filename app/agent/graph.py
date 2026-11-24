from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agent.tools import get_profile, get_skills, search_projects
from app.core.config import settings

from app.agent.knowledge import search_knowledge

TOOLS = [get_profile, get_skills, search_projects, search_knowledge]

SYSTEM = """你是小王的数字分身，负责介绍他的作品、技能和经历。
规则：
1. 只根据工具返回的数据回答，不要编造
2. 涉及他的笔记/文档内容时，用 search_knowledge 查
3. 回答简洁，不超过 3 句话
4. 不知道就直说"这个我还没有数据"
"""


def build_agent(checkpointer):
    """创建一个带记忆的 ReAct Agent。"""
    llm = ChatOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        model=settings.LLM_MODEL,
    )
    return create_react_agent(
        llm,
        TOOLS,
        prompt=SYSTEM,
        checkpointer=checkpointer,
    )
