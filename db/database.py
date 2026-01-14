import uuid
import chromadb
from ollama import embeddings

from db.embeddings import embed_texts, embed_query

# ✅ Explicit persistent client (disk-only)
chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)
collection = chroma_client.get_or_create_collection(
    name="rag_docs"
)
def store_chunks(chunks: list[str]):
    collection.add(
        documents=chunks,
        embeddings=embed_texts(chunks),
        ids=[f"doc_{uuid.uuid4()}" for _ in chunks]
    )

def retrieve_context(query: str, top_k: int = 3) -> str:
    results = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=top_k
    )
    if not results or not results.get("documents"):
        return ""
    return "\n\n".join(results["documents"][0])

