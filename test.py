from app.agent.knowledge import search_knowledge
print(search_knowledge.invoke({"query": "你的笔记里 LangChain 是什么"})[:400])