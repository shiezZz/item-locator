import random
import string
import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "item_locator.db")
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "item_images")
os.makedirs(IMAGES_DIR, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password: str) -> str:
    """Simple SHA-256 hash. Fine for a local desktop app; not meant for
    high-security multi-user systems."""
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
            verification_code TEXT
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

def generate_code() -> str:
    return "".join(random.choices(string.digits, k=6))

def verify_user(username: str, password: str):
    """Returns 'ok', 'unverified', or 'invalid'."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, is_verified FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None or row[1] != hash_password(password):
        return "invalid", None
    if row[2] == 0:
        return "unverified", None
    return "ok", row[0]

def create_account(username: str, email: str, password: str):
    """Returns the verification code on success, or None if username/email taken."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email))

    if cur.fetchone() is not None:
        conn.close()
        return None

    code = generate_code()
    cur.execute(
        "INSERT INTO users (username, email, password_hash, is_verified, verification_code) VALUES (?, ?, ?, 0, ?)",
        (username, email, hash_password(password), code),
    )
    conn.commit()
    conn.close()
    return code

def verify_code(username: str, code: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT verification_code FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    if row is None or row[0] != code:
        conn.close()
        return False

    cur.execute(
        "UPDATE users SET is_verified = 1, verification_code = NULL WHERE username = ?",
        (username,),
    )
    conn.commit()
    conn.close()
    return True

def add_item(user_id: int, name:str, location: str, category: str, notes: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ITEMS (user_id, name, location, category, notes) VALUES (?, ?, ?, ?, ?)", 
        (user_id, name, location, category, notes,)
        )
    conn.commit()
    conn.close()
    return True

def get_all_items(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, location, category, notes, date_updated from items WHERE user_id = ? ORDER BY name",
        (user_id,)
    )

    rows = cur.fetchall()
    conn.close()
    return rows

def delete_item(item_id: int, user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM items where id = ? AND user_id = ?",
        (item_id, user_id),
    ) 
    conn.commit()
    conn.close()
    return True

def get_item(item_id: int, user_id:int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, location, category, notes, date_updated, image_path from items WHERE id = ? AND user_id = ?",
        (item_id, user_id)
    )
    row = cur.fetchone()
    conn.close()
    return row

def edit_item(user_id: int, item_id: int, name: str, location: str, category: str, notes: str, image_path: str = None) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    if image_path is not None:
        cur.execute(
            """ UPDATE items
                SET name = ?, location = ?, category = ?, notes = ?,
                    image_path = ?, date_updated = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
            """,
            (name, location, category, notes, image_path, item_id, user_id)
        )
    else:
        cur.execute(
            """ UPDATE items
                SET name = ?, location = ?, category = ?, notes = ?,
                    date_updated = CURRENT_TIMESTAMP
                WHERE id = ? AND user_id = ?
            """,
            (name, location, category, notes, item_id, user_id)
        )
    conn.commit()
    conn.close()
    return True
