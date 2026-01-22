from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(
    question: str,
    chat_history: list,
    context: str
) -> str:

    print(context)

    history_text = ""
    for chat in chat_history:
        history_text += f"""
User: {chat['question']}
Assistant: {chat['answer']}
"""

    prompt = f"""
You are an assistant answering questions based on an internal document.

Rules:
- Use ONLY the facts explicitly present in the document.
- You MAY rephrase, expand, and explain those facts in a natural, user-friendly way.
- Do NOT add new facts that are not stated or clearly implied.
- If some details are missing, explain them carefully without guessing.
- Do NOT mention the word "context" or explain limitations unless necessary.

Conversation history:
{history_text}

Document:
{context}

Question:
{question}

Write a clear, professional answer.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.3
    )

    return response.output_text.strip() if response.output_text else "No answer generated."
