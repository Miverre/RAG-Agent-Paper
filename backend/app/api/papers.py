from fastapi import APIRouter,File,UploadFile
from pydantic import BaseModel
from backend.app.services.document_loader import load_pdf_text, extract_pdf_text
from backend.app.services.paper_service import save_uploaded_pdf
from backend.app.services.text_splitter import split_text

router = APIRouter(prefix="/papers", tags=["papers"])

class ParsePaperRequest(BaseModel):
    """解析 PDF 的请求参数。"""

    file_path: str

class ChunkPaperRequest(BaseModel):
    """切分 PDF 的请求参数。"""

    file_path: str
    chunk_size: int = 800
    chunk_overlap: int = 100

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

@router.post("/chunk")
def chunk_paper(request: ChunkPaperRequest):
    """
    读取 PDF 并切分文本。
    这里只返回 chunk 预览，不做向量化。
    """
    text = extract_pdf_text(request.file_path)
    chunks = split_text(
        text=text,
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
    )

    return {
        "file_path": request.file_path,
        "chunk_size": request.chunk_size,
        "chunk_overlap": request.chunk_overlap,
        "chunk_count": len(chunks),
        "preview_chunks": chunks[:3],
    }