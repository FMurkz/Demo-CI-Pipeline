from unittest.mock import MagicMock, patch

from mysql.connector import IntegrityError
import pytest

from src.app import add_item, delete_item, get_items, mark_item_as_bought
@patch("src.app.get_connection")
def test_add_item_returns_new_record(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 7
    mock_get_connection.return_value = conn

    result = add_item("milk")

    assert result == {"id": 7, "name": "milk", "quantity": 1, "bought": False}
    conn.commit.assert_called_once()
    conn.close.assert_called_once()



    
@patch("src.app.get_connection")
def test_add_two_items_with_same_name_raises(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 1
    cursor.execute.side_effect = [None, IntegrityError("Duplicate entry")]
    mock_get_connection.return_value = conn

    add_item("Duplicate Item")

    with pytest.raises(ValueError, match="^Item already exists$"):
        add_item("Duplicate Item")


@patch("src.app.get_connection")
def test_mark_item_as_bought(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 1
    cursor.fetchone.return_value = {
        "id": 1,
        "name": "Item",
        "quantity": 1,
        "bought": True,
    }
    mock_get_connection.return_value = conn

    item = add_item("Item")
    marked_item = mark_item_as_bought(item["id"], True)
    assert marked_item["bought"] is True


@patch("src.app.get_connection")
def test_mark_item_as_unbought(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 1
    cursor.fetchone.side_effect = [
        {"id": 1, "name": "Item", "quantity": 1, "bought": True},
        {"id": 1, "name": "Item", "quantity": 1, "bought": False},
    ]
    mock_get_connection.return_value = conn

    item = add_item("Item")
    mark_item_as_bought(item["id"], True)
    marked_item = mark_item_as_bought(item["id"], False)
    assert marked_item["bought"] is False

