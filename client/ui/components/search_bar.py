
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QLabel
)
from PySide6.QtCore import Signal


class SearchBar(QWidget):
    text_changed = Signal(str)

    def __init__(self, placeholder="Tìm kiếm...", parent=None):
        super().__init__(parent)

        self.setup_ui(placeholder)

    def setup_ui(self, placeholder):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Biểu tượng tìm kiếm
        icon_label = QLabel("⌕")
        icon_label.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 22px;
                background-color: white;
            }
        """)

        # Ô nhập tìm kiếm
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setMinimumHeight(40)

        self.input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #DCE3EC;
                border-radius: 7px;
                padding: 8px 12px;
                font-size: 13px;
                color: #34445C;
            }

            QLineEdit:focus {
                border: 1px solid #278F8B;
            }
        """)

        # Phát tín hiệu khi nội dung thay đổi
        self.input.textChanged.connect(
            self.text_changed.emit
        )

        layout.addWidget(icon_label)
        layout.addWidget(self.input)

    def text(self):
        return self.input.text()

    def clear(self):
        self.input.clear()

    def set_placeholder(self, placeholder):
        self.input.setPlaceholderText(placeholder)

    def set_text(self, value):
        self.input.setText(value)
