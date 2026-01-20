from db.sqlite_db import get_connection

def create_seating(rows, cols, row_allocation):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM seating")

    for r in range(rows):
        for c in range(cols):
            cur.execute("""
            INSERT INTO seating (row_number, column_number, tech_stack, employee_id)
            VALUES (?, ?, ?, NULL)
            """, (r+1, c+1, row_allocation[r]))

    conn.commit()
    conn.close()


def find_seat(tech_stack):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT row_number, column_number
    FROM seating
    WHERE tech_stack = ? AND employee_id IS NULL
    ORDER BY row_number, column_number
    LIMIT 1
    """, (tech_stack,))

    seat = cur.fetchone()
    conn.close()
    return seat


def allocate_seat(tech_stack: str, employee_email: str) -> str | None:
    conn = get_connection()
    cur = conn.cursor()

    # Get first available seat for tech stack
    cur.execute("""
        SELECT id, row_number, column_number
        FROM seating
        WHERE tech_stack = ?
          AND employee_email IS NULL
        ORDER BY row_number, column_number
        LIMIT 1
    """, (tech_stack,))

    seat = cur.fetchone()

    if not seat:
        conn.close()
        return None

    seat_id, row, col = seat
    seat_number = f"R{row}C{col}"

    # Mark seat as occupied
    cur.execute("""
        UPDATE seating
        SET employee_email = ?
        WHERE id = ?
    """, (employee_email, seat_id))

    conn.commit()
    conn.close()

    return seat_number