from fastapi import APIRouter,Depends
from app.model.seating_db import create_seating
from utils.admin_guard import AdminOnly
# from app.service.seating_service import allocate_seat
from db.sqlite_db import get_connection

admin_router = APIRouter(prefix="/admin/seating")

@admin_router.post("/configure")
def configure_seating(config: dict):
    if len(config["row_allocation"]) != config["rows"]:
        return {"error": "row_allocation length mismatch"}

    create_seating(
        config["rows"],
        config["cols"],
        config["row_allocation"]
    )

    return {"status": "seating configured"}
#
# #####
# @admin_router.post("/allocate")
# def allocate_seat_to_user(user_id: int, tech_stack: str, admin=Depends(AdminOnly)):
#     seat = allocate_seat(tech_stack)
#
#     if not seat:
#         return {"message": "No seat available"}
#
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute("""
#     UPDATE employees
#     SET seat_number = ?
#     WHERE id = ?
#     """, (seat, user_id))
#
#     cur.execute("""
#     UPDATE seating
#     SET employee_id = ?
#     WHERE tech_stack = ? AND employee_id IS NULL
#     ORDER BY row_number, column_number
#     LIMIT 1
#     """, (user_id, tech_stack))
#
#     conn.commit()
#     conn.close()
#
#     return {"seat_allocated": seat}











