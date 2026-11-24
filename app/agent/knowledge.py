from functools import lru_cache

from langchain_core.tools import tool
from pymilvus import MilvusClient
from sqlalchemy import text
from langchain_community.embeddings import DashScopeEmbeddings
from app.core.config import settings
from app.db.session import engine

# 记录"最近一次检索到的引用片段"，供流式接口读取
# 注：模块级变量，单进程单用户够用；多用户并发场景应改为按请求上下文隔离
_LAST_REFS: list[dict] = []


def get_last_refs() -> list[dict]:
    return list(_LAST_REFS)


def _set_last_refs(refs: list[dict]) -> None:
    _LAST_REFS.clear()
    _LAST_REFS.extend(refs)


@lru_cache(maxsize=1)
def get_milvus() -> MilvusClient:
    client = MilvusClient(settings.KNOWLEDGE_DB_PATH)
    client.load_collection("knowledge_children")
    return client


@lru_cache(maxsize=1)
def get_embedding() -> DashScopeEmbeddings:
    return DashScopeEmbeddings(
        model="text-embedding-v4",
        dashscope_api_key=settings.DASHSCOPE_API_KEY,
    )


def retrieve_parents(query: str, k: int = 5, max_parents: int = 3) -> list[dict]:
    """子块检索 → 还原父块。"""
    q = get_embedding().embed_query(query)
    hits = get_milvus().search(
        "knowledge_children", data=[q], limit=k,
        output_fields=["parent_id", "content"],
    )[0]

    parent_ids: list[str] = []
    for h in hits:
        pid = h["entity"]["parent_id"]
        if pid not in parent_ids:
            parent_ids.append(pid)
    parent_ids = parent_ids[:max_parents]

    if not parent_ids:
        return []

    ids_str = ",".join(f"'{i}'" for i in parent_ids)
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT id, title, content, source FROM knowledge_parents WHERE id IN ({ids_str})")
        ).fetchall()

    return [{"id": r[0], "title": r[1], "content": r[2], "source": r[3]} for r in rows]


@tool
def search_knowledge(query: str) -> str:
    """从我的知识库（笔记/文档）中检索相关内容。"""
    parents = retrieve_parents(query)
    if not parents:
        return "没有找到相关资料。"

    # 记录引用片段（供流式接口通过 custom 事件推给前端）
    _set_last_refs([
        {"id": i, "title": p["title"], "source": p["source"]}
        for i, p in enumerate(parents, 1)
    ])

    parts = []
    for i, p in enumerate(parents, 1):
        parts.append(f"[{i}] 《{p['title']}》\n{p['content']}")
    return "\n\n".join(parts)
