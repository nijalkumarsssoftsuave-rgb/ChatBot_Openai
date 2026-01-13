# upload_routes.py
import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException,Query,Depends
from pypdf import PdfReader
from database import retrieve_context
from generate_answer import generate_answer
from database import collection, create_embedding
from app.model.chat_db import save_chat, get_last_chats
from utils.jwt_utils import TokenPayload
from utils.JWT_Token import JWTBearer
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 300):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_id = uuid.uuid4().hex
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(file_path)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    chunks = chunk_text(text)

    for chunk in chunks:
        collection.add(
            documents=[chunk],
            embeddings=[create_embedding(chunk)],
            ids=[f"pdf_{uuid.uuid4()}"]
        )

    return {
        "message": "PDF uploaded and indexed successfully",
        "chunks_stored": len(chunks)
    }

@router.post("/ask")
def ask_question(
    question: str,
    user: TokenPayload = Depends(JWTBearer())
):
    context = retrieve_context(question)

    chat_history = get_last_chats(user.id, limit=10)

    answer = generate_answer(context, question, chat_history)
    save_chat(user.id, question, answer)
    return {"answer": answer}

@router.get("/chats")
def get_chat_history(
    user: TokenPayload = Depends(JWTBearer())
):
    chats = get_last_chats(user.id, limit=10)
    return [
        {
            "question": chat["question"],
            "answer": chat["answer"]
        }
        for chat in chats
    ]
@router.get("/chats")
def get_chats(user: TokenPayload = Depends(JWTBearer())):
    chats = get_last_chats(user.id)

    return [
        {"question": c["question"], "answer": c["answer"]}
        for c in chats
    ]

