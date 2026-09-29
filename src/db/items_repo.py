"""
items_repo.py
All queries for the items table: add, list, fetch one, edit, delete.
"""

from src.db.connection import get_connection

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
        "SELECT id, name, location, category, notes, date_updated, image_path from items WHERE user_id = ? ORDER BY name",
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
