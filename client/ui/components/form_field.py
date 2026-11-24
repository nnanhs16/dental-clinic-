
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit
)
from PySide6.QtCore import Signal


class FormField(QWidget):
    value_changed = Signal(str)

    def __init__(
        self,
        label,
        placeholder="",
        password=False,
        parent=None
    ):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)

        self.label = QLabel(label)
        self.label.setStyleSheet("""
            color: #34445C;
            font-size: 13px;
            font-weight: 600;
        """)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(40)

        self.input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #DCE3EC;
                border-radius: 6px;
                padding: 8px 10px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #278F8B;
            }
        """)

        if password:
            self.input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

        self.input.textChanged.connect(self.value_changed.emit)

        layout.addWidget(self.label)
        layout.addWidget(self.input)

    def text(self):
        return self.input.text()

    def set_text(self, value):
        self.input.setText(value)

    def clear(self):
        self.input.clear()
