from unittest.mock import MagicMock, patch

import pytest

from src.app import add_item
from src.app import mark_item_as_bought
from src.db import get_connection


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
