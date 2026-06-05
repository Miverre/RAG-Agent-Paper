from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.llm_service import ask_llm

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMTestRequest(BaseModel):
    """大模型测试请求。"""

    question: str


@router.post("/test")
def test_llm(request: LLMTestRequest):
    """
    测试 Qwen 是否可以正常调用。
    """
    answer = ask_llm(request.question)

    return {
        "question": request.question,
        "answer": answer,
    }