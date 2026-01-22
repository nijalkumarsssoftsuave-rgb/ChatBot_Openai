import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pypdf import PdfReader

from db.database import store_chunks
from app.model.chat_db import get_last_chats
from utils.admin_guard import admin_required
from utils.jwt_utils import TokenPayload
from utils.JWT_Token import JWTBearer

router = APIRouter()

UPLOAD_DIR = "extract_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    admin=Depends(admin_required)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_id = uuid.uuid4().hex
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(file_path)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No extractable text found")

    # Chunk + store as vectors ONLY
    chunks = chunk_text(text)
    store_chunks(chunks)

    return {
        "message": "PDF uploaded and indexed as vectors",
        "chunks_stored": len(chunks)
    }
@router.get("/chats")
def get_chat_history(
    user: TokenPayload = Depends(JWTBearer())
):
    user_id = int(user.id)

    try:
        chats = get_last_chats(user_id, limit=20)
    except HTTPException:
        raise HTTPException(
            status_code=404,
            detail="No chat history found"
        )

    return {
        "user_id": user_id,
        "history": chats
    }


