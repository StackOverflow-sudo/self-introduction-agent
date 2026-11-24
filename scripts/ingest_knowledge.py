from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from app.agent.knowledge import get_vectorstore
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def main():
    path = r"D:\agent\agent-lab\manual.md"
    text = open(path, encoding="utf-8").read()

    md = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "h1"), ("##", "h2")])
    docs = md.split_text(text)
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)
    for c in chunks:
        c.metadata["source"] = "Linux学习笔记D5-Agent基础"

    ids = get_vectorstore().add_documents(chunks)
    print(f"ingested {len(ids)} chunks into Milvus")


if __name__ == "__main__":
    main()