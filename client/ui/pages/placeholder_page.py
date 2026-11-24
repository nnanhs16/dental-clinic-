
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class PlaceholderPage(QWidget):
    def __init__(
        self,
        title,
        description="Chức năng đang được phát triển."
    ):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #172B4D;
        """)

        description_label = QLabel(description)
        description_label.setStyleSheet("""
            font-size: 14px;
            color: #718096;
        """)

        layout.addWidget(
            title_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            description_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
