"""Core shopping-list operations, independent from the user interface."""

from mysql.connector import IntegrityError
from db import get_connection


def add_item(item):
    """Add an item and return it. Accepts a name or a name/quantity mapping."""
    if isinstance(item, str):
        name = item.strip()
        quantity = 1
    else:
        name = str(item.get("name", "")).strip()
        quantity = int(item.get("quantity", 1))

    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "INSERT INTO items (name, quantity, bought) VALUES (%s, %s, %s)",
                (name, quantity, False),
            )
            conn.commit()
        except IntegrityError:
            raise ValueError("Item already exists")

        new_id = cursor.lastrowid
        return {"id": new_id, "name": name, "quantity": quantity, "bought": False}
    finally:
        conn.close()


def get_items():
    """Return a copy of the current shopping list."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, quantity, bought FROM items")
        return cursor.fetchall()
    finally:
        conn.close()


def mark_item_as_bought(item_id, bought=True):
    """Set an item's bought state and return it, or None if it does not exist."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE items SET bought = %s WHERE id = %s", (bought, item_id)
        )
        conn.commit()

        cursor.execute(
            "SELECT id, name, quantity, bought FROM items WHERE id = %s", (item_id,)
        )
        return cursor.fetchone()
    finally:
        conn.close()


def delete_item(item_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()