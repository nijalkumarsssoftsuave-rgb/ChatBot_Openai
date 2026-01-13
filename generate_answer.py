from click import prompt

from database import client

def generate_answer(context: str, question: str,chat_history: list) -> str:
    history_text = ""

    for chat in chat_history:
        history_text += f"""
    User: {chat['question']}
    Assistant: {chat['answer']}
    """

    prompt = f"""
You are an assistant answering questions based on an internal document.

Rules:
- Use ONLY the facts explicitly present in the context.
- You MAY rephrase, expand, and explain those facts in a natural, user-friendly way.
- Do NOT add new facts that are not stated or clearly implied.
- If some details are missing, explain them carefully without guessing.
- Do NOT mention the word "context" or explain limitations unless necessary.
- At the emd give some confidence score out of 100

Conversation history (for tone & continuity only):
{history_text}

Document context:
{context}

Current user question:
{question}


Write a clear, professional, human-friendly answer.
"""
    print(prompt)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.3
    )

    return response.output[0].content[0].text
