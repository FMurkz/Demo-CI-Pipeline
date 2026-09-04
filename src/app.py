"""Core shopping-list operations, independent from the user interface."""

from src.db import get_connection


def _run(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Execute a query and optionally fetch/commit, always closing the connection."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if commit:
            conn.commit()
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return cursor
    finally:
        conn.close()


def add_item(item):
    """Add an item and return it. Accepts a name or a name/quantity mapping."""
    if isinstance(item, str):
        name, quantity = item.strip(), 1
    else:
        name = str(item.get("name", "")).strip()
        quantity = int(item.get("quantity", 1))

    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    if any(existing["name"] == name for existing in get_items()):
        raise ValueError("Item already exists")

    cursor = _run(
        "INSERT INTO items (name, quantity, bought) VALUES (%s, %s, %s)",
        (name, quantity, False),
        commit=True,
    )
    return {"id": cursor.lastrowid, "name": name, "quantity": quantity, "bought": False}


def get_items():
    """Return a copy of the current shopping list."""
    return _run("SELECT id, name, quantity, bought FROM items", fetchall=True)


def mark_item_as_bought(item_id, bought=True):
    """Set an item's bought state and return it, or None if it does not exist."""
    #BUG: the parameters for the SQL query are in the wrong order
    _run("UPDATE items SET bought = %s WHERE id = %s", (item_id, bought), commit=True)
    item = _run(
        "SELECT id, name, quantity, bought FROM items WHERE id = %s",
        (item_id,),
        fetchone=True,
    )
    return item


def delete_item(item_id):
    """Delete an item by id. Returns True if a row was deleted."""
    cursor = _run("DELETE FROM items WHERE id = %s", (item_id,), commit=True)
    return cursor.rowcount > 0