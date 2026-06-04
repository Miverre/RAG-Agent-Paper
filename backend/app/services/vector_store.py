from typing import Any
from uuid import uuid4
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# ChromaDB 本地持久化目录
CHROMA_DIR = "chroma_db"
# 使用本地开源 embedding 模型
# 第一次运行会下载模型，可能需要一些时间
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def get_paper_collection(collection_name: str = "papers"):
    """
    获取或创建 ChromaDB collection。
    collection 可以理解成一个向量数据表。
    """
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function,
    )

def add_chunks_to_vector_store(
    chunks: list[str],
    source_file: str,
    collection_name: str = "papers",) -> dict[str, Any]:
    """
    将文本 chunks 写入 ChromaDB。

    每个 chunk 都会生成：
    - id: 唯一编号
    - document: 原始文本
    - metadata: 来源文件和 chunk 序号
    """
    collection = get_paper_collection(collection_name)
    ids = []
    metadatas = []

    for index, _chunk in enumerate(chunks):
        ids.append(str(uuid4()))
        metadatas.append(
            {
                "source_file": source_file,
                "chunk_index": index,
            }
        )

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    return {
        "collection_name": collection_name,
        "added_count": len(chunks),
        "source_file": source_file,
    }

def search_similar_chunks(
    query: str,
    collection_name: str = "papers",
    top_k: int = 3,
) -> dict:
    """
    根据用户问题，从 ChromaDB 中检索最相关的 chunks。
    """
    if not query.strip():
        raise ValueError("query 不能为空")

    collection = get_paper_collection(collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []

    for index, document in enumerate(documents):
        matches.append(
            {
                "content": document,
                "metadata": metadatas[index] if index < len(metadatas) else {},
                "distance": distances[index] if index < len(distances) else None,
            }
        )

    return {
        "query": query,
        "collection_name": collection_name,
        "top_k": top_k,
        "matches": matches,
    }