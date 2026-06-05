import os
from dotenv import load_dotenv
from fastapi import HTTPException
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

def get_qwen_llm():
    """
        创建 Qwen 聊天模型。
        后续如果要换模型，只改这个函数。
        """
    api_key = os.getenv("DASHSCOPE_API_KEY")
    model_name=os.getenv("DASHSCOPE_MODEL")

    if not api_key:
        raise HTTPException(status_code=500,detail="DASHSCOPE_API_KEY not set")

    return ChatOpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model=model_name,
    )

def ask_llm(question:str)->str:
    """
       调用 Qwen 回答一个简单问题。
       当前只做连通性测试，不接 RAG。
       """
    if not question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")

    llm = get_qwen_llm()
    response = llm.invoke([HumanMessage(content=question)])
    return response.content