from fastapi import APIRouter,File,UploadFile
from pydantic import BaseModel
from backend.app.services.document_loader import load_pdf_text, extract_pdf_text
from backend.app.services.paper_service import save_uploaded_pdf
from backend.app.services.text_splitter import split_text
from backend.app.services.vector_store import add_chunks_to_vector_store
from backend.app.services.vector_store import add_chunks_to_vector_store,search_similar_chunks
from backend.app.services.rag_service import ask_paper_with_rag
from backend.app.services.report_service import generate_paper_report
router = APIRouter(prefix="/papers", tags=["papers"])

class ReportPaperRequest(BaseModel):
    """论文分析报告请求参数。"""

    topic: str
    collection_name: str = "papers"
    top_k: int = 6

class AskPaperRequest(BaseModel):
    """论文 RAG 问答请求参数。"""

    question: str
    collection_name: str = "papers"
    top_k: int = 3

class ParsePaperRequest(BaseModel):
    """解析 PDF 的请求参数。"""

    file_path: str

class ChunkPaperRequest(BaseModel):
    """切分 PDF 的请求参数。"""

    file_path: str
    chunk_size: int = 800
    chunk_overlap: int = 100

class IndexPaperRequest(BaseModel):
    """论文入库请求参数。"""

    file_path: str
    collection_name: str = "papers"
    chunk_size: int = 800
    chunk_overlap: int = 100

class SearchPaperRequest(BaseModel):
    """RAG 检索请求参数。"""

    query: str
    collection_name: str = "papers"
    top_k: int = 3

class ReportPaperRequest(BaseModel):
    """论文分析报告请求参数。"""

    topic: str
    collection_name: str = "papers"
    top_k: int = 6

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

@router.post("/index")
def index_paper(request: IndexPaperRequest):
    """
    将 PDF 文本切分后写入 ChromaDB。
    这是 RAG 的入库阶段。
    """
    text = extract_pdf_text(request.file_path)

    chunks = split_text(
        text=text,
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
    )

    result = add_chunks_to_vector_store(
        chunks=chunks,
        source_file=request.file_path,
        collection_name=request.collection_name,
    )

    return {
        **result,
        "chunk_size": request.chunk_size,
        "chunk_overlap": request.chunk_overlap,
    }

@router.post("/search")
def search_paper(request: SearchPaperRequest):
    """
    从 ChromaDB 中检索和问题最相关的论文片段。
    这里只做检索，不调用大模型。
    """
    return search_similar_chunks(
        query=request.query,
        collection_name=request.collection_name,
        top_k=request.top_k,
    )

@router.post("/ask")
def ask_paper(request: AskPaperRequest):
    """
    基于已入库论文进行 RAG 问答。
    """
    return ask_paper_with_rag(
        question=request.question,
        collection_name=request.collection_name,
        top_k=request.top_k,
    )

@router.post("/report")
def create_paper_report(request: ReportPaperRequest):
    """
    基于已入库论文生成 Markdown 分析报告。
    """
    return generate_paper_report(
        topic=request.topic,
        collection_name=request.collection_name,
        top_k=request.top_k,
    )