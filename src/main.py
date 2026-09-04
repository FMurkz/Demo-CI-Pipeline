"""Launch the shopping-list desktop application."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PyQt6.QtWidgets import QApplication

from src.db import get_connection
from src.gui import ShoppingListWindow


def main():
    application = QApplication([])
    window = ShoppingListWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    get_connection()
    raise SystemExit(main())