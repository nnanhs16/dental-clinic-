
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QWidget
)
from PySide6.QtCore import Signal, Qt


class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(245)
        self.setObjectName("sidebar")

        self.setStyleSheet("""
            QFrame#sidebar {
                background-color: #172B4D;
                border: none;
            }

            QLabel#brand {
                color: white;
                font-size: 21px;
                font-weight: bold;
            }

            QLabel#subtitle {
                color: #AFC0D5;
                font-size: 11px;
            }

            QLabel#section {
                color: #8296B2;
                font-size: 10px;
                font-weight: bold;
                padding-left: 10px;
            }

            QPushButton {
                color: #D4DDE9;
                background-color: transparent;
                border: none;
                border-radius: 6px;
                text-align: left;
                padding: 12px;
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #29466B;
                color: white;
            }

            QPushButton:checked {
                background-color: #278F8B;
                color: white;
                font-weight: bold;
            }
        """)

        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(15, 25, 15, 20)
        self.layout_main.setSpacing(8)

        self.create_brand()
        self.create_menu()

        self.layout_main.addStretch()
        self.create_user_info()

    def create_brand(self):
        brand = QLabel("DENTAL CARE")
        brand.setObjectName("brand")

        subtitle = QLabel("CLINIC MANAGEMENT SYSTEM")
        subtitle.setObjectName("subtitle")

        self.layout_main.addWidget(brand)
        self.layout_main.addWidget(subtitle)
        self.layout_main.addSpacing(30)

    def create_menu(self):
        section = QLabel("MENU CHÍNH")
        section.setObjectName("section")
        self.layout_main.addWidget(section)

        menus = [
            ("⌂", "Tổng quan", "dashboard"),
            ("♙", "Bệnh nhân", "patients"),
            ("▦", "Lịch hẹn", "appointments"),
            ("✚", "Khám và điều trị", "clinical"),
            ("▤", "Thanh toán", "accounting"),
            ("♧", "Nhân sự", "employees"),
            ("▥", "Báo cáo thống kê", "reports"),
            ("⚙", "Cài đặt", "settings"),
        ]

        self.buttons = {}

        for icon, title, page_id in menus:
            button = QPushButton(f"{icon}    {title}")
            button.setCheckable(True)

            button.clicked.connect(
                lambda checked=False, p=page_id:
                self.change_page(p)
            )

            self.layout_main.addWidget(button)
            self.buttons[page_id] = button

        self.buttons["dashboard"].setChecked(True)

    def change_page(self, page_id):
        for button in self.buttons.values():
            button.setChecked(False)

        self.buttons[page_id].setChecked(True)
        self.page_changed.emit(page_id)

    def create_user_info(self):
        user = QLabel("QUẢN TRỊ HỆ THỐNG")
        user.setStyleSheet("""
            color: white;
            font-weight: bold;
            padding: 10px;
        """)

        self.layout_main.addWidget(user)
