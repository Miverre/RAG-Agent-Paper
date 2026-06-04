from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException,UploadFile

#保存目录
UPLOAD_DIR=Path("uploads")

async def save_uploaded_pdf(file: UploadFile)->dict:
    """
       保存上传的 PDF 文件。
       这里只做上传保存，不做 PDF 解析。
       """
    UPLOAD_DIR.mkdir(exist_ok=True)
    if not file.filename:
        raise HTTPException(status_code=400,detail="文件名不能为空")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400,detail="支持上传pdf文件")
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400,detail="文件不能为空")

    saved_filename=f"{uuid4().hex}_{file.filename}"
    saved_path = UPLOAD_DIR / saved_filename
    saved_path.write_bytes(content)
    return {
        "message": "PDF 上传成功",
        "original_filename": file.filename,
        "saved_filename": saved_filename,
        "saved_path": str(saved_path),
        "file_size": len(content),
    }
