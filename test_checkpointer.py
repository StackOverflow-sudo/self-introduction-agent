from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent

from app.core.config import settings

llm = ChatOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
    model=settings.LLM_MODEL,
)

with PostgresSaver.from_conn_string(settings.PG_DSN) as checkpointer:
    checkpointer.setup()

    agent = create_react_agent(llm, tools=[], checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "test-1"}}

    agent.invoke({"messages": [{"role": "user", "content": "我叫小明，请记住"}]}, config)
    r = agent.invoke({"messages": [{"role": "user", "content": "我叫什么名字？"}]}, config)

    print("reply:", r["messages"][-1].content)