from fastapi import APIRouter, HTTPException,Depends
from app.model.admin_auth_model import authenticate_admin
from utils.jwt_utils import create_access_token
from app.pydantic.base_pydantic import TokenRequest, TokenResponse
from  db.sqlite_db import get_connection
from utils.admin_guard import AdminOnly

router = APIRouter(prefix="/admin/auth")

@router.post("/login", response_model=TokenResponse)
def admin_login(email: str, password: str):
    admin = authenticate_admin(email, password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    token_request = TokenRequest(
        id=str(admin["id"]),
        email=admin["email"],
        role="admin"          # 🔑 IMPORTANT
    )

    access_token = create_access_token(token_request)

    return {"access_token": access_token}

#####
# @router.post("/approve")
# def approve_user(user_id: int, admin=Depends(AdminOnly)):
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute("""
#     UPDATE employees
#     SET eligibility_status = 'selected'
#     WHERE id = ?
#     """, (user_id,))
#
#     conn.commit()
#     conn.close()
#
#     return {"status": "approved"}
#
#
# @router.post("/reject")
# def reject_user(user_id: int, admin=Depends(AdminOnly)):
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute("""
#     UPDATE employees
#     SET eligibility_status = 'rejected',
#         seat_number = NULL
#     WHERE id = ?
#     """, (user_id,))
#
#     conn.commit()
#     conn.close()
#
#     return {"status": "rejected"}