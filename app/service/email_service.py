import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USERNAME = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("PASSWORD")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email: str, subject: str, body: str):
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        raise RuntimeError("Email credentials not found in environment")

    msg = EmailMessage()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
