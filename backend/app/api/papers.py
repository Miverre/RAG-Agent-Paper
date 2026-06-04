from fastapi import APIRouter,File,UploadFile
from backend.app.services.paper_service import save_uploaded_pdf
router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/upload")
async def upload_paper(paper_file: UploadFile = File(...)):
    """
        上传论文 PDF 接口。
        接口层只负责接收文件和返回结果。
        """
    return await save_uploaded_pdf(paper_file)