import os
import uuid
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(".env")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found")

# OpenAI client (single instance)
client = OpenAI(api_key=API_KEY)

# Persistent ChromaDB
chroma_client = chromadb.Client(
    Settings(persist_directory="./chroma_db")
)

collection = chroma_client.get_or_create_collection(
    name="rag_docs"
)

def create_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap

    return chunks


def store_chunks(chunks: list[str]):
    for chunk in chunks:
        collection.add(
            documents=[chunk],
            embeddings=[create_embedding(chunk)],
            ids=[f"doc_{uuid.uuid4()}"]
        )
    chroma_client.persist()

def retrieve_context(query: str, top_k: int = 3) -> str:
    query_embedding = create_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    if not results["documents"]:
        return ""

    return "\n\n".join(results["documents"][0])
