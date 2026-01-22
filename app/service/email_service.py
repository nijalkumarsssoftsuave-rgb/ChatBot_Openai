from app.service.pdf_service import generate_seat_pdf
from app.service.pdf_service import generate_no_seat_pdf
from utils.email import send_email

def send_otp_email(email: str, otp: str):
    subject = "Verify your account – OTP"

    body = f"""
Your One-Time Password (OTP) is:

{otp}

This OTP is valid for 5 minutes.

If you did not request this, please ignore this email.
"""

    send_email(
        to_email=email,
        subject=subject,
        body=body
    )


def send_selected_with_seat_email(
    to_email: str,
    name: str,
    seat_number: str,
    tech_stack: str,
):
    subject = "SoftSuave Onboarding – Selection Confirmed"

    body = f"""
Hi {name},

We are pleased to inform you that you have successfully cleared the onboarding criteria.

Your seat allocation details are attached as a PDF.

Seat Number: {seat_number}
Tech Stack: {tech_stack.capitalize()}

We look forward to welcoming you on board.
"""

    pdf_path = generate_seat_pdf(
        name=name,
        seat_number=seat_number,
        tech_stack=tech_stack
    )

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        attachment_path=pdf_path
    )


# def send_selected_no_seat_email(
#     to_email: str,
#     name: str,
#     pdf_path: Optional[str] = None
# ):
#     subject = "SoftSuave Onboarding – Selection Update"
#
#     body = f"""
# Hi {name},
#
# Congratulations on clearing the onboarding process.
#
# Currently, seating for your tech stack is fully occupied.
# Your seat will be assigned on your joining day.
#
# Please find your joining letter attached.
# """
#
#     send_email(to_email, subject, body)


def send_selected_no_seat_email(
    to_email: str,
    name: str
):
    subject = "SoftSuave Onboarding – Selection Update"

    body = f"""
Hi {name},

Congratulations on clearing the onboarding process.

Currently, seating for your tech stack is fully occupied.
Your seat will be assigned on your joining day.

Please find the onboarding details attached.
"""

    pdf_path = generate_no_seat_pdf(name=name)

    send_email(
        to_email=to_email,
        subject=subject,
        body=body,
        attachment_path=pdf_path
    )


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

