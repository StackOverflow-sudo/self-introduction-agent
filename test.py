from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(model="bge-m3")
vec = emb.embed_query("今天天气真好")
print("维度:", len(vec))
print("前 5 个值:", vec[:5])