from db.sqlite_db import get_connection
def save_employee(data: dict):
    """
    Saves employee onboarding result.
    Prevents duplicate submissions by email.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM employees WHERE email = ?",
        (data["email"],)
    )
    exists = cur.fetchone()

    if exists:
        conn.close()
        return  # silently ignore duplicate submissions
    cur.execute("""
        INSERT INTO employees (
            name,
            email,
            phone,
            tech_stack,
            tenth,
            twelfth,
            status,
            seat
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["email"],
        data["phone"],
        data["tech_stack"],
        data["tenth"],
        data["twelfth"],
        data["status"],
        data.get("seat")
    ))
    conn.commit()
    conn.close()
