from fastapi import HTTPException
def split_text(text:str,chunk_size:int,chunk_overlap:int)->list:
    """
        把长文本切成多个 chunk。

        chunk_size: 每块最大字符数
        chunk_overlap: 相邻 chunk 重叠字符数
        """
    if not text.strip():
        raise HTTPException(status_code=400, detail="文本不能为空")

    if chunk_size <= 0:
        raise HTTPException(status_code=400, detail="chunk_size 必须大于 0")

    if chunk_overlap < 0:
        raise HTTPException(status_code=400, detail="chunk_overlap 不能小于 0")

    if chunk_overlap >= chunk_size:
        raise HTTPException(
            status_code=400,
            detail="chunk_overlap 必须小于 chunk_size",
        )
    chunks=[]
    start = 0
    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]

        if chunk:
            chunks.append(chunk)

        start+=chunk_size-chunk_overlap

    return chunks


