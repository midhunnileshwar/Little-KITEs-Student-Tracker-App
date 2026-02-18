import sqlite3
import pandas as pd

DB_PATH = "students.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_all_students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students ORDER BY id", conn)
    conn.close()
    return df

def get_student_progress(student_id, session_name):
    conn = get_connection()
    query = "SELECT activity_name, status, stars FROM progress WHERE student_id = ? AND session_name = ?"
    df = pd.read_sql(query, conn, params=(student_id, session_name))
    conn.close()
    return df

def update_progress(student_id, session_name, activity_name, status, stars):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO progress (student_id, session_name, activity_name, status, stars)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id, session_name, activity_name) 
        DO UPDATE SET status=excluded.status, stars=excluded.stars
    ''', (student_id, session_name, activity_name, status, stars))
    conn.commit()
    conn.close()

def add_student(admission_no, name, school_unit="Rajahs H.S.S Nileshwar"):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (admission_no, name, school_unit) VALUES (?, ?, ?)", (admission_no, name, school_unit))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
