from pathlib import Path
from fastapi import HTTPException
from pypdf import PdfReader

def load_pdf_text(file_path:str)->dict:
    """
       读取 PDF 文本。

       当前阶段只做最小解析：
       - 检查文件是否存在
       - 检查是否是 PDF
       - 提取文本
       - 返回页数、字符数、预览
       """
    path = Path(file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF 文件不存在")

    if path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="只支持解析 PDF 文件")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"PDF 读取失败: {exc}")

    page_texts=[]
    for page_idnex, page in enumerate(reader.pages,start=1):
        text = page.extract_text() or ""
        if text.strip():
            page_texts.append({"text": text, "page_id": page_idnex})
    full_text="\n\n".join(item["text"] for item in page_texts).strip()

    if not full_text:
        raise HTTPException(status_code=400,detail="未读取到文本")

    return {
        "file_path": str(path),
        "page_count": len(reader.pages),
        "text_page_count": len(page_texts),
        "char_count": len(full_text),
        "preview": full_text[:500],
        "full_text": full_text,
    }

def extract_pdf_text(file_path: str) -> str:
    """
    提取 PDF 完整文本。
    后续 chunk、embedding、RAG 都会复用这个函数。
    """
    result = load_pdf_text(file_path)
    return result["full_text"]