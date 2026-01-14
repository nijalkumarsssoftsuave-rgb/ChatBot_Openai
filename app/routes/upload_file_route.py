import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pypdf import PdfReader

from db.database import store_chunks, retrieve_context
from db.rag_openai import generate_answer
from app.model.chat_db import save_chat, get_last_chats

from utils.jwt_utils import TokenPayload
from utils.JWT_Token import JWTBearer

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Helpers ----------

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

# ---------- Routes ----------

@router.post("/upload/pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    user: TokenPayload = Depends(JWTBearer())
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


@router.post("/ask")
def ask_question(
    question: str,
    user: TokenPayload = Depends(JWTBearer())
):
    # Retrieve relevant vector context
    context = retrieve_context(question)

    # Load chat history from SQLite
    chat_history = get_last_chats(int(user.id), limit=10)

    # Generate answer (RAG)
    answer = generate_answer(question, chat_history)

    # Store chat in SQLite
    save_chat(int(user.id), question, answer)

    return {"answer": answer}


@router.get("/chats")
def get_chat_history(
    user: TokenPayload = Depends(JWTBearer())
):
    return get_last_chats(int(user.id), limit=10)
