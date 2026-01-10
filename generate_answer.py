# generate_answer.py
from openai import OpenAI
from database import retrieve_context, client  # reuse same client

def generate_answer(context: str, question: str):
    prompt = f"""
You are a helpful assistant.
Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0
    )

    return response.output_text


if __name__ == "__main__":
    print("🤖 RAG Chatbot (type 'exit' to stop)\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break

        context = retrieve_context(query)
        answer = generate_answer(context, query)

        print("\nBot:", answer)
