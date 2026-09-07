from unittest.mock import MagicMock, patch

from mysql.connector import IntegrityError
import pytest

from src.app import add_item, delete_item, get_items, mark_item_as_bought, get_connection

@pytest.fixture
def clean_table():
    yield
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE items")
        conn.commit()
    finally:
        conn.close()

def test_adding_same_item_different_case_is_rejected_integration(clean_table):
    add_item("milk")

    with pytest.raises(ValueError):
        add_item("Milk")

    names = sorted(item["name"] for item in get_items())
    assert names == ["milk"], f"expected one row, got {names}"

def test_mark_item_as_bought_integration(clean_table):
    add_item("Flour")
    add_item("Milk")
    added = add_item("Eggs")
    result = mark_item_as_bought(added["id"], bought=True)
    assert result["bought"] in (True, 1)