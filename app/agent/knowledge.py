from functools import lru_cache

from langchain_core.tools import tool
from langchain_milvus import Milvus
from langchain_ollama import OllamaEmbeddings

from app.core.config import settings


@lru_cache(maxsize=1)
def get_vectorstore() -> Milvus:
    """向量库只创建一次（复用）。"""
    return Milvus(
        embedding_function=OllamaEmbeddings(model="bge-m3"),
        connection_args={"uri": settings.KNOWLEDGE_DB_PATH},
        collection_name="knowledge",
    )


@tool
def search_knowledge(query: str) -> str:
    """从我的知识库（笔记/文档）中检索相关内容。"""
    vs = get_vectorstore()
    docs = vs.similarity_search(query, k=3)
    if not docs:
        return "没有找到相关资料。"

    parts = []
    for i, d in enumerate(docs, 1):
        source = d.metadata.get("source") or d.metadata.get("h1") or "未知来源"
        parts.append(f"[{i}] 来源：{source}\n{d.page_content}")
    return "\n\n".join(parts)