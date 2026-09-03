"""Launch the shopping-list desktop application."""

from PyQt6.QtWidgets import QApplication

from gui import ShoppingListWindow

from db import get_connection


def main():
    application = QApplication([])
    window = ShoppingListWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    get_connection()
    raise SystemExit(main())