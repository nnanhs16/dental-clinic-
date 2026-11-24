
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt


class Header(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(75)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #E8EDF3;
            }

            QLabel#pageTitle {
                color: #172B4D;
                font-size: 20px;
                font-weight: bold;
            }

            QLabel#userName {
                color: #52627A;
                font-size: 13px;
            }

            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 18px;
                padding: 8px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(25, 10, 25, 10)

        self.page_title = QLabel("Tổng quan")
        self.page_title.setObjectName("pageTitle")

        layout.addWidget(self.page_title)
        layout.addStretch()

        notification = QPushButton("♧")
        notification.setToolTip("Thông báo")

        user_name = QLabel("Quản trị viên")
        user_name.setObjectName("userName")

        layout.addWidget(notification)
        layout.addWidget(user_name)

    def set_title(self, title):
        self.page_title.setText(title)
