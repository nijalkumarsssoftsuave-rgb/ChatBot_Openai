from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import tempfile
from datetime import datetime

BASE_PDF_DIR = "uploads/onboarding_pdfs"

def generate_seat_pdf(
    name: str,
    seat_number: str,
    tech_stack: str
) -> str:
    """
    Creates a PDF and returns the file path.
    """
    os.makedirs(f"{BASE_PDF_DIR}/selected_with_seat", exist_ok=True)

    filename = f"{name}_{seat_number}_{int(datetime.now().timestamp())}.pdf"
    path = os.path.join(BASE_PDF_DIR, "selected_with_seat", filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, "Onboarding Seat Allocation")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"Name: {name}")
    c.drawString(50, height - 160, f"Seat Number: {seat_number}")
    c.drawString(50, height - 190, f"Tech Stack: {tech_stack.capitalize()}")

    c.drawString(
        50,
        height - 240,
        "Please report to the above seat on your joining day."
    )

    # c.showPage()
    c.save()
    return path


def generate_no_seat_pdf(name: str) -> str:
    """
    PDF for selected candidates without seat allocation
    """

    os.makedirs(f"{BASE_PDF_DIR}/selected_no_seat", exist_ok=True)

    filename = f"{name}_coming_soon_{int(datetime.now().timestamp())}.pdf"
    path = os.path.join(BASE_PDF_DIR, "selected_no_seat", filename)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, "Onboarding Update")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 130, f"Name: {name}")
    c.drawString(50, height - 160, "Seat Number: Coming Soon")
    c.drawString(50, height - 190, "Tech Stack: Will be confirmed")

    c.drawString(
        50,
        height - 240,
        "Your seat will be assigned on your joining day."
    )

    # c.showPage()
    c.save()

    return path