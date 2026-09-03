"""Launch the shopping-list desktop application."""

from PyQt5.QtWidgets import QApplication

from gui import ShoppingListWindow


def main():
    application = QApplication([])
    window = ShoppingListWindow()
    window.show()
    return application.exec_()


if __name__ == "__main__":
    raise SystemExit(main())