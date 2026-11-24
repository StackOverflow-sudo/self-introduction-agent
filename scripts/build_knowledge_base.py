import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import glob
import os

from app.agent.knowledge import get_embedding
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from pymilvus import DataType, MilvusClient

from app.core.config import settings
import glob
import os

# 要入库的笔记（排除进度/问答/目录树）
EXCLUDE = {"README.md", "学习进度.md", "学习提问记录.md"}
MD_FILES = [
    f for f in sorted(glob.glob(r"D:\agent\*.md"))
    if os.path.basename(f) not in EXCLUDE
]


def main():
    print("docs:", len(MD_FILES))

    client = MilvusClient(settings.KNOWLEDGE_DB_PATH)
    if "knowledge_children" in client.list_collections():
        client.drop_collection("knowledge_children")

    schema = client.create_schema(auto_id=False)
    schema.add_field("id", DataType.VARCHAR, is_primary=True, max_length=128)
    schema.add_field("parent_id", DataType.VARCHAR, max_length=128)
    schema.add_field("content", DataType.VARCHAR, max_length=8000)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=1024)
    ip = client.prepare_index_params()
    ip.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")
    client.create_collection("knowledge_children", schema=schema, index_params=ip)

    emb = get_embedding()  
    md_split = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "h1"), ("##", "h2")])
    child_split = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

    parents, children = [], []
    for path in MD_FILES:
        slug = os.path.splitext(os.path.basename(path))[0]
        text = open(path, encoding="utf-8").read()
        for pi, p in enumerate(md_split.split_text(text)):
            pid = f"{slug}-p{pi}"
            title = p.metadata.get("h2") or p.metadata.get("h1") or slug
            parents.append({
                "id": pid,
                "content": p.page_content,
                "source": os.path.basename(path),
                "title": title,
            })
            for ci, ctext in enumerate(child_split.split_text(p.page_content)):
                children.append({"id": f"{pid}-c{ci}", "parent_id": pid, "content": ctext})

    print("parents:", len(parents), "children:", len(children))

    vecs = emb.embed_documents([c["content"] for c in children])
    data = [
        {"id": c["id"], "parent_id": c["parent_id"], "content": c["content"], "vector": v}
        for c, v in zip(children, vecs)
    ]
    res = client.insert("knowledge_children", data)
    print("inserted children:", res["insert_count"])

    # 父块先存成 json（下一步入 MariaDB）
    import json
    out = r"D:\agent\agent-lab\parents.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(parents, f, ensure_ascii=False, indent=2)
    print("parents saved:", out)


if __name__ == "__main__":
    main()