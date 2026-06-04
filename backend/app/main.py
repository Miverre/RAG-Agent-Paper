from fastapi import FastAPI
# 创建 FastAPI 应用实例
# title 和 version 会显示在自动生成的接口文档里
app=FastAPI(
    title="RAG智能体文献管理总结",
    version="0.1.0",
)
@app.get("/")
def read_root():
    """
        根路径接口。
        用来快速确认后端服务是否启动成功。
        """
    return {"message": "RAG Agent Paper backend is running"}

@app.get("/health")
def health_check():
    """
    健康检查接口。
    后续可以用它判断服务是否正常。
    """
    return {"status": "ok"}