from typing import Optional
from app.service.email_service import send_email

def send_selected_with_seat_email(
    to_email: str,
    name: str,
    seat_number: str,
    tech_stack: str,
    pdf_path: Optional[str] = None
):
    subject = "SoftSuave Onboarding – Selection Confirmed"

    body = f"""
Hi {name},

We are pleased to inform you that you have successfully cleared the onboarding criteria.

Your joining details are attached in the PDF.

Seat Allocation:
Seat Number: {seat_number}
Tech Stack: {tech_stack.capitalize()}

We look forward to welcoming you on board.
"""

    send_email(to_email, subject, body)


def send_selected_no_seat_email(
    to_email: str,
    name: str,
    pdf_path: Optional[str] = None
):
    subject = "SoftSuave Onboarding – Selection Update"

    body = f"""
Hi {name},

Congratulations on clearing the onboarding process.

Currently, seating for your tech stack is fully occupied.
Your seat will be assigned on your joining day.

Please find your joining letter attached.
"""

    send_email(to_email, subject, body)


def send_rejection_email(
    to_email: str,
    name: str
):
    subject = "SoftSuave Onboarding – Application Update"

    body = f"""
Hi {name},

Thank you for your interest in joining our organization.

After careful review, we regret to inform you that we will not be able to proceed further at this time.
This decision does not reflect your potential, and we encourage you to apply again in the future.

We wish you the very best in your career journey.
"""

    send_email(to_email, subject, body)


# ----------------------------------------------------------------
# Internal email sender (replace with SMTP later)
# ----------------------------------------------------------------
def _send_email(to_email: str, subject: str, body: str, pdf_path: Optional[str]):
    """
    This is a placeholder.
    Replace with SMTP / SendGrid / SES later.
    """

    print("===================================")
    print("TO:", to_email)
    print("SUBJECT:", subject)
    print("BODY:", body)
    print("ATTACHMENT:", pdf_path)
    print("===================================")
