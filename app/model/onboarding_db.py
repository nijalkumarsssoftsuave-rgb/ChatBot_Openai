from db.sqlite_db import get_connection

def save_employee(data: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO employees (
        name, email, phone, tech_stack,
        tenth_percentage, twelfth_percentage,
        eligibility_status, seat_number
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
