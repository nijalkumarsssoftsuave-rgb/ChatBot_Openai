import sqlite3
from pathlib import Path

DB_PATH = Path("rag_chat.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'admin'))
    )
    """)

    #employee table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    tech_stack TEXT NOT NULL,
    tenth REAL NOT NULL,
    twelfth REAL NOT NULL,
    status TEXT NOT NULL,
    seat TEXT
    )
    """)

    # cur.execute("""
    # CREATE TABLE IF NOT EXISTS seating (
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # tech_stack TEXT NOT NULL,
    # row_number INTEGER NOT NULL,
    # column_number INTEGER NOT NULL,
    # employee_email TEXT,
    # UNIQUE (tech_stack, row_number, column_number)
    # )
    # """)

    cur.execute("""
    
    CREATE TABLE IF NOT EXISTS seating (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    row_number INTEGER NOT NULL,
    column_number INTEGER NOT NULL,
    tech_stack TEXT NOT NULL CHECK (
        tech_stack IN ('python', 'java', 'node', 'qa')
    ),
    occupied INTEGER NOT NULL DEFAULT 0,
    employee_id INTEGER,
    UNIQUE (tech_stack, row_number, column_number),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)


    # Chat history table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
