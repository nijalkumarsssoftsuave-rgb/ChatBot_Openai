from fastapi import APIRouter, Depends, HTTPException
from db.sqlite_db import get_connection
from app.pydantic.seating_pydantic import SeatingCreateRequest
from utils.admin_guard import admin_required

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

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM seating")

        for row_idx in range(data.rows):
            tech = data.row_allocation[row_idx].lower()
            for col_idx in range(1, data.cols + 1):
                cur.execute("""
                    INSERT INTO seating (row_number, column_number, tech_stack, employee_id)
                    VALUES (?, ?, ?, NULL)
                """, (row_idx + 1, col_idx, tech))

        conn.commit()
    finally:
        conn.close()

    return {
        "message": "Seating arrangement created successfully",
        "rows": data.rows,
        "cols": data.cols
    }


@seating_router.get("/view")
def view_seating():
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT row_number, column_number, tech_stack, employee_id
            FROM seating
            ORDER BY row_number, column_number
        """)
        rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        return {"message": "No seating arrangement has been created yet."}

    seating = {}
    for r, c, tech, emp in rows:
        seating.setdefault(f"R{r}", []).append({
            "column": c,
            "tech_stack": tech,
            "occupied": bool(emp),
            "employee_id": emp
        })

    return {
        "seating": seating
    }
