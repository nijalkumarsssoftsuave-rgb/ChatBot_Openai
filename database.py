# database.py
import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI

# Load env ONCE
load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found")

# Create ONE client
client = OpenAI(api_key=API_KEY)

# ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="rag_docs")


def create_embedding(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def load_and_chunk(file_path: str, chunk_size: int = 300):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def store_documents(file_path: str):
    chunks = load_and_chunk(file_path)

    for idx, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            embeddings=[create_embedding(chunk)],
            ids=[f"doc_{idx}"]
        )

    print("✅ Documents stored in ChromaDB")


def retrieve_context(query: str, top_k: int = 3):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return "\n".join(results["documents"][0])
