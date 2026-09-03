"""Core shopping-list operations, independent from the user interface."""

_items = []
_next_id = 1


def add_item(item):
    """Add an item and return it. Accepts a name or a name/quantity mapping."""
    global _next_id

    if isinstance(item, str):
        name = item.strip()
        quantity = 1
    else:
        name = str(item.get("name", "")).strip()
        quantity = int(item.get("quantity", 1))

    if not name:
        raise ValueError("Item name cannot be empty")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    if any(existing["name"].casefold() == name.casefold() for existing in _items):
        raise ValueError("That item is already on the list")

    new_item = {"id": _next_id, "name": name, "quantity": quantity, "bought": False}
    _items.append(new_item)
    _next_id += 1
    return new_item.copy()


def get_items():
    """Return a copy of the current shopping list."""
    return [item.copy() for item in _items]


def mark_item_as_bought(item_id, bought=True):
    """Set an item's bought state and return it, or None if it does not exist."""
    for item in _items:
        if item["id"] == int(item_id):
            item["bought"] = bool(bought)
            return item.copy()
    return None


def delete_item(item_id):
    """Delete an item and return True when it existed."""
    for index, item in enumerate(_items):
        if item["id"] == int(item_id):
            del _items[index]
            return True
    return False