
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout
)


class BasePage(QWidget):
    def __init__(
        self,
        title,
        description="",
        parent=None
    ):
        super().__init__(parent)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(18)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("""
            font-size: 23px;
            font-weight: bold;
            color: #172B4D;
        """)

        self.description_label = QLabel(description)
        self.description_label.setStyleSheet("""
            font-size: 13px;
            color: #718096;
        """)

        self.main_layout.addWidget(self.title_label)

        if description:
            self.main_layout.addWidget(self.description_label)

    def add_content(self, widget):
        self.main_layout.addWidget(widget)

    def add_layout(self, layout):
        self.main_layout.addLayout(layout)

    def add_spacing(self, spacing=10):
        self.main_layout.addSpacing(spacing)

    def add_stretch(self):
        self.main_layout.addStretch()
