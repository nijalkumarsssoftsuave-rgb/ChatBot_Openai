from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTENTS = {
    "onboarding_start",
    "onboarding_continue",
    "onboarding_cancel",
    "normal_chat"
}
def detect_intent(message: str, session_mode: str | None) -> str:
    """
    Uses OpenAI to classify user intent.
    session_mode helps disambiguate mid-onboarding replies.
    """

    prompt = f"""
You are an intent classifier for a chatbot.

Decide the user's intent and return ONLY one label from this list:
- onboarding_start
- onboarding_continue
- onboarding_cancel
- normal_chat

Guidelines:
- onboarding_start: user shows interest in jobs, joining, careers, HR, application
- onboarding_continue: user is answering questions or providing details
- onboarding_cancel: user wants to stop, cancel, pause, do later
- normal_chat: anything else

Current session mode: {session_mode or "none"}

User message:
"{message}"

Return ONLY the intent label.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0.3
    )

    intent = response.output_text.strip().lower()
    return intent if intent in INTENTS else "normal_chat"
