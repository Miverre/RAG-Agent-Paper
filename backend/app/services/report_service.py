from fastapi import HTTPException
from langchain_core.prompts import ChatPromptTemplate
from backend.app.services.llm_service import get_qwen_llm
from backend.app.services.vector_store import search_similar_chunks

def generate_paper_report(
    topic: str,
    collection_name: str = "papers",
    top_k: int = 6,
) -> dict:
    """
    基于论文检索结果生成 Markdown 分析报告。
    """
    if not topic.strip():
        raise HTTPException(status_code=400, detail="分析主题不能为空")

    search_result = search_similar_chunks(
        query=topic,
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
                "你是一个研究生科研论文分析助手。"
                "请严格基于给定论文片段生成 Markdown 报告，"
                "不要编造片段中没有的信息。",
            ),
            (
                "human",
                """
论文片段：
{context}

分析主题：
{topic}

请生成一份 Markdown 格式的论文分析报告，包含以下部分：

# 论文分析报告

## 1. 研究问题
说明论文主要解决什么问题。

## 2. 方法概述
概括论文使用的方法或模型。

## 3. 创新点
总结可能的创新点。如果片段不足以判断，请明确说明。

## 4. 实验与结果
总结实验设置、指标或结果。如果片段不足以判断，请明确说明。

## 5. 局限与改进方向
分析可能的不足，并提出后续改进方向。

## 6. 参考片段
列出你主要依据了哪些片段编号。
""",
            ),
        ]
    )

    llm = get_qwen_llm()
    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "topic": topic,
        }
    )

    return {
        "topic": topic,
        "markdown_report": response.content,
        "references": matches,
    }