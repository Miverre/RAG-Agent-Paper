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