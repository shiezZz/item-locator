"""
connection.py
Raw connection handling, password hashing, schema creation/migrations.
"""

import sqlite3
import hashlib
from src.config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def hash_password(password: str) -> str:
    """Simple SHA-256 hash."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_verified INTEGER DEFAULT 0,
            verification_code TEXT,
            code_expires_at REAL
        )
    """)

    # Placeholder for the items feature you'll build out next.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            category TEXT,
            notes TEXT,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            date_updated TEXT DEFAULT CURRENT_TIMESTAMP,
            image_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Seed a default test user: admin / admin123
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, is_verified) VALUES (?, ?, ?, 1)",
            ("admin", "admin@example.com", hash_password("admin123")),
        )



    conn.commit()
    conn.close()
