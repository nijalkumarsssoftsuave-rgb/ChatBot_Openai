# import smtplib
# from email.message import EmailMessage
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# EMAIL_USERNAME = os.getenv("EMAIL")
# EMAIL_PASSWORD = os.getenv("PASSWORD")
#
# SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 587
#
# def send_email(to_email: str, subject: str, body: str):
#     if not EMAIL_USERNAME or not EMAIL_PASSWORD:
#         raise RuntimeError("Email credentials not found in environment")
#
#     msg = EmailMessage()
#     msg["From"] = EMAIL_USERNAME
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.set_content(body)
#
#     with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#         server.starttls()
#         server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
#         server.send_message(msg)
#

import smtplib
from email.message import EmailMessage
import os
import mimetypes
from dotenv import load_dotenv

load_dotenv()

EMAIL_USERNAME = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("PASSWORD")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str | None = None
):
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        raise RuntimeError("Email credentials not found in environment")

    msg = EmailMessage()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # ✅ Attachment support (PDF, etc.)
    if attachment_path:
        mime_type, _ = mimetypes.guess_type(attachment_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        maintype, subtype = mime_type.split("/")

        with open(attachment_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype=maintype,
                subtype=subtype,
                filename=os.path.basename(attachment_path)
            )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
