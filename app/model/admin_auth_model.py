# from db.sqlite_db import get_connection
# from bcrypt import checkpw
# from utils.jwt_utils import _normalize_password
#
# def authenticate_admin(email: str, password: str):
#     email = email.strip().lower()
#
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute(
#         "SELECT id, password FROM admins WHERE email = ?",
#         (email,)
#     )
#
#     row = cur.fetchone()
#     conn.close()
#
#     if not row:
#         return None
#
#     admin_id, stored_hash = row
#
#     if not checkpw(_normalize_password(password), stored_hash.encode()):
#         return None
#
#     return {"id": admin_id, "email": email, "role": "admin"}
