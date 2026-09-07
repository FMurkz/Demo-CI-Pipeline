import pytest

from src.app import add_item, delete_item, get_items, mark_item_as_bought, get_connection

@pytest.fixture(autouse=True)
def clean_table():
    yield
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE items")
        conn.commit()
    finally:
        conn.close()

def test_adding_same_item_different_case_is_rejected_integration():
    add_item("milk")

    with pytest.raises(ValueError):
        add_item("Milk")

def test_mark_item_as_bought_integration():
    add_item("Flour")
    add_item("Milk")
    added = add_item("Eggs")
    result = mark_item_as_bought(added["id"], bought=True)
    assert result["bought"] in (True, 1)