"""
users_repo.py
All queries and logic for the users table: signup, login, verification.
"""

import random
import string
import time
from src.db.connection import get_connection, hash_password
from src.config import CODE_EXPIRY_SECONDS

def generate_code() -> str:
    return "".join(random.choices(string.digits, k=6))

def verify_user(username: str, password: str):
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
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email))

    if cur.fetchone() is not None:
        conn.close()
        return None

    code = generate_code()
    expires_at = time.time() + CODE_EXPIRY_SECONDS
    cur.execute(
        "INSERT INTO users (username, email, password_hash, is_verified, verification_code, code_expires_at) VALUES (?, ?, ?, 0, ?, ?)",
        (username, email, hash_password(password), code, expires_at),
    )
    conn.commit()
    conn.close()
    return code

def verify_code(username: str, code: str) -> str:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT verification_code FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    if row is None or row[0] != code:
        conn.close()
        return "invalid"

    stored_code, expires_at = row

    if expires_at is None or time.time() > expires_at:
        conn.close()
        return "expired"

    if stored_code != code: 
        conn.close()
        return "invalid"

    cur.execute(
        "UPDATE users SET is_verified = 1, verification_code = NULL, code_expires_at = NULL WHERE username = ?",
        (username,),
    )
    conn.commit()
    conn.close()
    return True

def resend_code(username: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, is_verified FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    if row is None or row[1] == 1:
        conn.close()
        return None

    code = generate_code()
    cur.execute(
        "UPDATE users SET verification_code = ?, code_expires_at = ? WHERE username = ?",
        (code, time.time() + CODE_EXPIRY_SECONDS, username),
    )
    conn.commit()
    conn.close()
    return row[0], code