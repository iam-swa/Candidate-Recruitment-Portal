import os
import sqlite3
from datetime import datetime
import shutil

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "portal.db")
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                resume_path TEXT NOT NULL,
                cover_letter TEXT,
                status TEXT DEFAULT 'Applied',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        conn.commit()

def get_user(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT email, first_name, last_name FROM users WHERE email = ?', (email,))
        return cursor.fetchone()

def create_or_update_user(email, fname, lname):
    with get_connection() as conn:
        cursor = conn.cursor()
        user = get_user(email)
        if user:
            cursor.execute('UPDATE users SET first_name = ?, last_name = ? WHERE email = ?', (fname, lname, email))
        else:
            cursor.execute('INSERT INTO users (email, first_name, last_name) VALUES (?, ?, ?)', (email, fname, lname))
        conn.commit()

def save_application(email, resume_temp_path, cover_letter):
    # Copy resume to uploads dir
    if resume_temp_path and os.path.exists(resume_temp_path):
        filename = os.path.basename(resume_temp_path)
        final_path = os.path.join(UPLOADS_DIR, f"{email}_{filename}")
        shutil.copy2(resume_temp_path, final_path)
    else:
        final_path = ""

    with get_connection() as conn:
        cursor = conn.cursor()
        # Check if already applied
        cursor.execute('SELECT id FROM applications WHERE user_email = ?', (email,))
        if cursor.fetchone():
            # Update existing Application
            cursor.execute('UPDATE applications SET resume_path = ?, cover_letter = ? WHERE user_email = ?', 
                           (final_path, cover_letter, email))
        else:
            cursor.execute('INSERT INTO applications (user_email, resume_path, cover_letter) VALUES (?, ?, ?)', 
                           (email, final_path, cover_letter))
        conn.commit()

def get_application_status(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM applications WHERE user_email = ?', (email,))
        row = cursor.fetchone()
        return row[0] if row else None
