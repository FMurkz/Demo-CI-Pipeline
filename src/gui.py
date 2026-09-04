"""PyQt6 desktop interface for the shopping list."""

from PyQt6.QtCore import QPoint, QSize, QTimer, Qt
from PyQt6.QtGui import QFont, QIcon, QPainter, QPen, QPixmap, QPolygon
from PyQt6.QtWidgets import (
    QApplication,
    QAbstractSpinBox,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from src.app import add_item, delete_item, get_items, mark_item_as_bought


class ShoppingListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shopping List")
        self.setMinimumSize(560, 500)
        self._build_ui()
        self.refresh_items()

    def _build_ui(self):
        self.setStyleSheet(
            """
            QWidget { background: #f7f4ec; color: #20302b; }
            QLineEdit, QSpinBox, QListWidget { background: #fffdf8; border: 1px solid #d9e1d8; border-radius: 5px; padding: 8px; }
            QPushButton { background: #176b54; border: 0; border-radius: 5px; color: white; padding: 9px 16px; font-weight: bold; }
            QPushButton:hover { background: #208366; }
            QToolButton { background: transparent; border: 1px solid #d9e1d8; border-radius: 5px; padding: 6px; }
            QToolButton:hover { background: #e8eee7; }
            QListWidget { padding: 6px; }
            QListWidget::item { border-bottom: 1px solid #e5e9e0; padding: 8px; }
            """
        )
        layout = QVBoxLayout(self)

        title = QLabel("Shopping list")
        title.setFont(QFont("Georgia", 30))
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        self.add_toggle_button = QPushButton("Add item")
        self.add_toggle_button.clicked.connect(self.toggle_add_form)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setIcon(self._refresh_icon(0))
        self.refresh_button.setIconSize(QSize(20, 20))
        self.refresh_button.setToolTip("Refresh list")
        self.refresh_button.clicked.connect(self.refresh_with_animation)
        toolbar.addWidget(self.add_toggle_button)
        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.add_panel = QFrame()
        add_row = QHBoxLayout(self.add_panel)
        add_row.setContentsMargins(0, 0, 0, 8)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Add an ingredient...")
        self.name_input.returnPressed.connect(self.add_current_item)
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 999)
        self.quantity_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.quantity_input.setMinimumWidth(58)
        self.add_button = QPushButton("Add item")
        self.add_button.clicked.connect(self.add_current_item)
        add_row.addWidget(self.name_input, 1)
        add_row.addWidget(self.quantity_input)
        add_row.addWidget(self.add_button)
        layout.addWidget(self.add_panel)
        self.add_panel.hide()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget, 1)

    def add_current_item(self):
        try:
            add_item({"name": self.name_input.text(), "quantity": self.quantity_input.value()})
        except ValueError as error:
            QMessageBox.warning(self, "Could not add item", str(error))
            return
        self.name_input.clear()
        self.quantity_input.setValue(1)
        self.close_add_form()
        self.refresh_items()

    def refresh_items(self):
        self.list_widget.clear()
        items = get_items()
        if not items:
            empty = QListWidgetItem("Your list is clear. Use Add item to get started.")
            empty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setForeground(Qt.GlobalColor.gray)
            self.list_widget.addItem(empty)
            return
        for item in items:
            row = QListWidgetItem()
            self.list_widget.addItem(row)
            widget = self._item_widget(item)
            row.setSizeHint(widget.sizeHint())
            self.list_widget.setItemWidget(row, widget)

    def _item_widget(self, item):
        widget = QWidget()
        row = QHBoxLayout(widget)
        checkbox = QCheckBox()
        checkbox.setChecked(item["bought"])
        checkbox.setToolTip("Mark item as bought")
        checkbox.stateChanged.connect(
            lambda state: self.set_item_bought(
                item["id"], state == Qt.CheckState.Checked.value
            )
        )
        row.addWidget(checkbox)
        name = QLabel(f"{item['name']}  x{item['quantity']}")
        name.setStyleSheet("font-size: 16px;")
        if item["bought"]:
            name.setStyleSheet("color: #6d7d76; font-size: 16px; text-decoration: line-through;")
        row.addWidget(name, 1)
        delete_button = QToolButton()
        delete_button.setText("X")
        delete_button.setFixedSize(36, 36)
        delete_button.setToolTip("Delete item")
        delete_button.setAccessibleName("Delete item")
        delete_button.clicked.connect(lambda: self.remove_item(item["id"]))
        row.addWidget(delete_button)
        return widget

    def toggle_add_form(self):
        is_visible = not self.add_panel.isVisible()
        self.add_panel.setVisible(is_visible)
        self.add_toggle_button.setText("Cancel" if is_visible else "Add item")
        if is_visible:
            self.name_input.setFocus()

    def _refresh_icon(self, angle):
        pixmap = QPixmap(22, 22)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(11, 11)
        painter.rotate(angle)
        painter.translate(-11, -11)
        pen = QPen(Qt.GlobalColor.white, 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(3, 3, 16, 16, 45 * 16, 285 * 16)
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(QPolygon([QPoint(12, 2), QPoint(19, 3), QPoint(16, 9)]))
        painter.end()
        return QIcon(pixmap)

    def refresh_with_animation(self):
        if self.refresh_button.isEnabled() is False:
            return
        self.refresh_button.setEnabled(False)
        self._refresh_angle = 0
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._animate_refresh)
        self._refresh_timer.start(35)
        self.refresh_items()
        QTimer.singleShot(450, self._finish_refresh_animation)

    def _animate_refresh(self):
        self._refresh_angle = (self._refresh_angle + 30) % 360
        self.refresh_button.setIcon(self._refresh_icon(self._refresh_angle))

    def _finish_refresh_animation(self):
        self._refresh_timer.stop()
        self.refresh_button.setIcon(self._refresh_icon(0))
        self.refresh_button.setEnabled(True)

    def close_add_form(self):
        self.add_panel.hide()
        self.add_toggle_button.setText("Add item")

    def set_item_bought(self, item_id, bought):
        mark_item_as_bought(item_id, bought)
        self.refresh_items()

    def remove_item(self, item_id):
        delete_item(item_id)
        self.refresh_items()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ShoppingListWindow()
    window.show()
    sys.exit(app.exec())