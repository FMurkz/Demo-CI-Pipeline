from unittest.mock import MagicMock, patch

from mysql.connector import IntegrityError
import pytest

from src.app import add_item, delete_item, get_items, mark_item_as_bought
@patch("src.app.get_connection")
def test_add_item_returns_new_record(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 7
    cursor.fetchone.return_value = None
    mock_get_connection.return_value = conn

    result = add_item("milk")

    assert result == {"id": 7, "name": "milk", "quantity": 1, "bought": False}
    assert conn.commit.call_count == 1
    assert conn.close.call_count == 2

@patch("src.app.get_connection")
def test_mark_item_as_bought(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.fetchone.return_value = {"id": 1, "name": "milk", "quantity": 1, "bought": True}
    mock_get_connection.return_value = conn

    result = mark_item_as_bought(1, True)

    assert result["bought"] is True
    conn.commit.assert_called_once()
    conn.close.assert_called_once()

@patch("src.app.get_connection")
def test_mark_item_as_bought(mock_get_connection):
    conn = MagicMock()
    mock_get_connection.return_value = conn
    cursor = conn.cursor.return_value
    cursor.fetchone.return_value = {"id": 5, "bought": True} 

    result = mark_item_as_bought(5, bought=True)

    assert result["bought"] is True

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

@patch("src.app.get_connection")
def test_mark_nonexistent_item_returns_none(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.lastrowid = 1
    cursor.fetchone.return_value = None
    mock_get_connection.return_value = conn

    result = mark_item_as_bought(999, True)
    assert result is None


@patch("src.app.get_connection")
def test_get_items_returns_list(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.fetchall.return_value = [
        {"id": 1, "name": "Item 1", "quantity": 1, "bought": False},
        {"id": 2, "name": "Item 2", "quantity": 2, "bought": True},
    ]
    mock_get_connection.return_value = conn

    items = get_items()
    assert len(items) == 2
    assert items[0]["name"] == "Item 1"
    assert items[1]["bought"] is True

@patch("src.app.get_connection")
def test_delete_item_returns_true_for_existing_item(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.rowcount = 1
    mock_get_connection.return_value = conn

    result = delete_item(1)
    assert result is True

@patch("src.app.get_connection")
def test_delete_item_returns_false_for_nonexistent_item(mock_get_connection):
    conn = MagicMock()
    cursor = conn.cursor.return_value
    cursor.rowcount = 0
    mock_get_connection.return_value = conn

    result = delete_item(999)
    assert result is False


@patch("src.app.get_connection")
@patch("src.app.get_items")
def test_add_item_allows_case_variants_as_separate_items(mock_get_items, mock_get_connection):
    """Intended behavior: no duplicates allowed"""
    conn = MagicMock()
    cursor = conn.cursor.return_value
    mock_get_connection.return_value = conn

    mock_get_items.return_value = [
        {"id": 1, "name": "milk", "quantity": 1, "bought": False}
    ]
    cursor.lastrowid = 2
    with pytest.raises(ValueError):
        add_item("milk")
    
@pytest.mark.integration
def test_case_duplicate_rejected():
    add_item("Milk")
    with pytest.raises(ValueError):
        add_item("milk")

@pytest.mark.integration
def test_mark_item_as_bought():
    added = add_item("Eggs")
    result = mark_item_as_bought(added["id"], bought=True)

    assert result["bought"] in (True, 1)
    

