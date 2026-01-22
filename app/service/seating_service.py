from db.sqlite_db import get_connection


def create_seating_service(rows: int, cols: int, row_allocation: list[str]):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM seating")

        for row_idx in range(rows):
            tech = row_allocation[row_idx].lower()
            for col_idx in range(1, cols + 1):
                cur.execute(
                    """
                    INSERT INTO seating (row_number, column_number, tech_stack, employee_id)
                    VALUES (?, ?, ?, NULL)
                    """,
                    (row_idx + 1, col_idx, tech)
                )

        conn.commit()
    finally:
        conn.close()


def view_seating_service():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                s.row_number,
                s.column_number,
                s.tech_stack,
                e.id AS employee_id,
                e.name AS employee_name
            FROM seating s
            LEFT JOIN employees e
              ON e.seat = ('R' || s.row_number || 'C' || s.column_number)
            ORDER BY s.row_number, s.column_number
        """)
        rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        return None

    seating = {}
    for r, c, tech, emp_id, emp_name in rows:
        seating.setdefault(f"R{r}", []).append({
            "column": c,
            "tech_stack": tech,
            "occupied": emp_id is not None,
            "employee_id": emp_id,
            "employee_name": emp_name
        })

    return seating


def view_seating_array_service():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT
                s.tech_stack,
                s.row_number,
                s.column_number,
                e.name AS employee_name
            FROM seating s
            LEFT JOIN employees e
              ON e.seat = ('R' || s.row_number || 'C' || s.column_number)
            ORDER BY s.tech_stack, s.row_number, s.column_number
        """)
        rows = cur.fetchall()
    finally:
        conn.close()

    seating = {}
    for tech, _, _, emp_name in rows:
        seating.setdefault(tech, []).append(emp_name)

    return seating
