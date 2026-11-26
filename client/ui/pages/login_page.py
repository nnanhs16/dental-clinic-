
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class LoginPage(QWidget):
    login_success = Signal()

    def __init__(self, api_service):
        super().__init__()

        self.api = api_service

        self.setStyleSheet("""
            QWidget {
                background-color: #F5F7FA;
                font-family: Arial;
            }

            QFrame#loginCard {
                background-color: white;
                border-radius: 14px;
            }

            QLineEdit {
                border: 1px solid #D9DEE7;
                border-radius: 7px;
                padding: 12px;
                font-size: 14px;
                background: white;
            }

            QLineEdit:focus {
                border: 1px solid #2563EB;
            }

            QPushButton#loginButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#loginButton:hover {
                background-color: #1D4ED8;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(420)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(16)

        title = QLabel("DENTAL CLINIC")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 23, QFont.Weight.Bold))
        title.setStyleSheet("color: #2563EB;")

        subtitle = QLabel("Đăng nhập tài khoản bệnh nhân")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #64748B; font-size: 14px;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.password_input.returnPressed.connect(self.handle_login)

        self.login_button = QPushButton("ĐĂNG NHẬP")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        main_layout.addWidget(card)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu."
            )
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("ĐANG ĐĂNG NHẬP...")

        result = self.api.login(username, password)

        self.login_button.setEnabled(True)
        self.login_button.setText("ĐĂNG NHẬP")

        if result["success"]:
            self.login_success.emit()
        else:
            QMessageBox.warning(
                self,
                "Đăng nhập thất bại",
                str(result.get("data") or result.get("message"))
            )
