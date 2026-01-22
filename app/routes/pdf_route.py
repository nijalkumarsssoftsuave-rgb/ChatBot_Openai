from fastapi.responses import FileResponse
from fastapi import APIRouter,HTTPException
import os

pdf_router = APIRouter()


@pdf_router.get("/pdf/view")
def view_pdf(path: str):
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")

    return FileResponse(path, media_type="application/pdf")
