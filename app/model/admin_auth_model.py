# import bcrypt
# from db.sqlite_db import get_connection
#
# def hash_password(password: str) -> str:
#     return bcrypt.hashpw(
#         password.encode("utf-8"),
#         bcrypt.gensalt()
#     ).decode("utf-8")
#
# def verify_password(password: str, hashed: str) -> bool:
#     return bcrypt.checkpw(
#         password.encode("utf-8"),
#         hashed.encode("utf-8")
#     )
#
# def create_admin(email: str, password: str):
#     conn = get_connection()
#     cur = conn.cursor()
#
#     # Check existing admin
#     cur.execute("SELECT id FROM admins WHERE email = ?", (email,))
#     if cur.fetchone():
#         conn.close()
#         return None
#
#     hashed_password = hash_password(password)
#
#     cur.execute(
#         "INSERT INTO admins (email, password) VALUES (?, ?)",
#         (email, hashed_password)
#     )
#     conn.commit()
#
#     cur.execute(
#         "SELECT id, email FROM admins WHERE email = ?",
#         (email,)
#     )
#     admin = cur.fetchone()
#     conn.close()
#
#     return {"id": admin[0], "email": admin[1]}
#
# def authenticate_admin(email: str, password: str):
#     conn = get_connection()
#     cur = conn.cursor()
#
#     cur.execute(
#         "SELECT id, email, password FROM admins WHERE email = ?",
#         (email,)
#     )
#     admin = cur.fetchone()
#     conn.close()
#
#     if not admin:
#         return None
#
#     if not verify_password(password, admin[2]):
#         return None
#
#     return {"id": admin[0], "email": admin[1]}
