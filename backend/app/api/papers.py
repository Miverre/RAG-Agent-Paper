from fastapi import APIRouter,File,UploadFile
from pydantic import BaseModel
from backend.app.services.document_loader import load_pdf_text
from backend.app.services.paper_service import save_uploaded_pdf

router = APIRouter(prefix="/papers", tags=["papers"])

class ParsePaperRequest(BaseModel):
    """解析 PDF 的请求参数。"""

    file_path: str

@router.post("/upload")
async def upload_paper(paper_file: UploadFile = File(...)):
    """
        上传论文 PDF 接口。
        接口层只负责接收文件和返回结果。
        """
    return await save_uploaded_pdf(paper_file)

@router.post("/parse")
def parse_paper(request: ParsePaperRequest):
    """
       解析已上传的 PDF。
       这里只返回文本预览，不做切分和向量化。
       """
    return load_pdf_text(request.file_path)