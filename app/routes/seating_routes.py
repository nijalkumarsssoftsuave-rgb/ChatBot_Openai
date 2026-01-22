from fastapi import APIRouter, Depends, HTTPException
from app.pydantic.seating_pydantic import SeatingCreateRequest
from utils.admin_guard import admin_required
from app.service.seating_service import (
    create_seating_service,
    view_seating_service,
    view_seating_array_service
)

seating_router = APIRouter(prefix="/admin/seating", tags=["Admin Seating"])


@seating_router.post("/create")
def create_seating(
    data: SeatingCreateRequest,
    admin=Depends(admin_required)
):
    if data.rows != len(data.row_allocation):
        raise HTTPException(
            status_code=400,
            detail="row_allocation length must match rows"
        )

    create_seating_service(
        rows=data.rows,
        cols=data.cols,
        row_allocation=data.row_allocation
    )

    return {
        "message": "Seating arrangement created successfully",
        "rows": data.rows,
        "cols": data.cols
    }


@seating_router.get("/view")
def view_seating(admin=Depends(admin_required)):
    seating = view_seating_service()
    if seating is None:
        return {"message": "No seating arrangement has been created yet."}
    return {"seating": seating}


@seating_router.get("/view-array")
def view_seating_array(
    admin=Depends(admin_required)
):
    return view_seating_array_service()
