from fastapi import HTTPException
from langchain_core.prompts import ChatPromptTemplate
from backend.app.services.llm_service import get_qwen_llm
from backend.app.services.vector_store import search_similar_chunks

def ask_paper_with_rag(
    question: str,
    collection_name: str = "papers",
    top_k: int = 3,
) -> dict:
    """
    基于 ChromaDB 检索结果进行 RAG 问答。
    """
    if not question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    search_result = search_similar_chunks(
        query=question,
        collection_name=collection_name,
        top_k=top_k,
    )

    matches = search_result["matches"]

    if not matches:
        raise HTTPException(status_code=400, detail="没有检索到相关论文片段")

    context = "\n\n".join(
        f"[片段{i + 1}]\n{match['content']}"
        for i, match in enumerate(matches)
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个研究生科研论文阅读助手。请只根据给定论文片段回答问题，"
                "如果片段中没有答案，就说明无法从当前论文片段判断。",
            ),
            (
                "human",
                "论文片段：\n{context}\n\n问题：{question}",
            ),
        ]
    )

    llm = get_qwen_llm()
    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return {
        "question": question,
        "answer": response.content,
        "references": matches,
    }