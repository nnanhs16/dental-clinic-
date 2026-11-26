
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal


class HomePage(QWidget):
    booking_requested = Signal()

    def __init__(self, user_data=None):
        super().__init__()

        self.user_data = user_data or {}

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                color: #172B4D;
                font-family: Arial;
            }

            QFrame#card {
                background-color: white;
                border: 1px solid #E8EDF3;
                border-radius: 12px;
            }

            QLabel#heading {
                font-size: 23px;
                font-weight: bold;
                color: #172B4D;
            }

            QLabel#subheading {
                font-size: 14px;
                color: #718096;
            }

            QLabel#cardTitle {
                font-size: 15px;
                font-weight: bold;
                color: #52627A;
            }

            QLabel#cardValue {
                font-size: 25px;
                font-weight: bold;
                color: #278F8B;
            }

            QPushButton#bookingButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 13px 22px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#bookingButton:hover {
                background-color: #207A77;
            }

            QPushButton#quickButton {
                background-color: white;
                border: 1px solid #DCE5EF;
                border-radius: 8px;
                padding: 13px;
                text-align: left;
                color: #172B4D;
                font-size: 13px;
            }

            QPushButton#quickButton:hover {
                border: 1px solid #278F8B;
                background-color: #F0FAF9;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(22)

        # Lời chào
        name = (
            self.user_data.get("full_name")
            or self.user_data.get("username")
            or "Bạn"
        )

        welcome_layout = QHBoxLayout()

        welcome_info = QVBoxLayout()

        heading = QLabel(f"Xin chào, {name}!")
        heading.setObjectName("heading")

        subtitle = QLabel(
            "Chào mừng bạn đến với hệ thống chăm sóc răng miệng Dental Care."
        )
        subtitle.setObjectName("subheading")

        welcome_info.addWidget(heading)
        welcome_info.addWidget(subtitle)

        welcome_layout.addLayout(welcome_info)
        welcome_layout.addStretch()

        booking_button = QPushButton("+ Đặt lịch khám")
        booking_button.setObjectName("bookingButton")
        booking_button.clicked.connect(
            self.booking_requested.emit
        )

        welcome_layout.addWidget(booking_button)

        main_layout.addLayout(welcome_layout)

        # Thẻ thông tin
        grid = QGridLayout()
        grid.setSpacing(18)

        grid.addWidget(
            self.create_card("Lịch hẹn sắp tới", "0", "Cuộc hẹn"),
            0, 0
        )

        grid.addWidget(
            self.create_card("Lịch sử khám", "0", "Lần khám"),
            0, 1
        )

        grid.addWidget(
            self.create_card("Dịch vụ nha khoa", "0", "Dịch vụ"),
            0, 2
        )

        main_layout.addLayout(grid)

        # Giới thiệu
        intro_card = QFrame()
        intro_card.setObjectName("card")

        intro_layout = QVBoxLayout(intro_card)
        intro_layout.setContentsMargins(22, 20, 22, 20)
        intro_layout.setSpacing(12)

        intro_title = QLabel("Chăm sóc nụ cười của bạn")
        intro_title.setStyleSheet(
            "font-size: 19px; font-weight: bold;"
        )

        intro_text = QLabel(
            "Dental Care đồng hành cùng bạn trong hành trình "
            "chăm sóc sức khỏe răng miệng. "
            "Hãy đặt lịch để được bác sĩ tư vấn và thăm khám."
        )
        intro_text.setWordWrap(True)
        intro_text.setStyleSheet(
            "font-size: 14px; color: #718096;"
        )

        intro_layout.addWidget(intro_title)
        intro_layout.addWidget(intro_text)

        main_layout.addWidget(intro_card)

        # Truy cập nhanh
        quick_title = QLabel("Truy cập nhanh")
        quick_title.setStyleSheet(
            "font-size: 19px; font-weight: bold;"
        )

        main_layout.addWidget(quick_title)

        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(15)

        quick_items = [
            ("✚   Xem dịch vụ", "services"),
            ("♙   Tìm bác sĩ", "doctors"),
            ("▤   Lịch sử khám", "history"),
            ("♧   Hồ sơ cá nhân", "account"),
        ]

        for title, page_id in quick_items:
            button = QPushButton(title)
            button.setObjectName("quickButton")
            button.clicked.connect(
                lambda checked=False, p=page_id:
                self.open_page(p)
            )
            quick_layout.addWidget(button)

        main_layout.addLayout(quick_layout)
        main_layout.addStretch()

    def create_card(self, title, value, description):
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        description_label = QLabel(description)
        description_label.setStyleSheet(
            "font-size: 12px; color: #718096;"
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)

        return card

    def open_page(self, page_id):
        self.parent_window.navigate_to(page_id)
