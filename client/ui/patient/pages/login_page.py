
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame
)
from PySide6.QtCore import Qt, Signal


class LoginPage(QWidget):

    login_success = Signal(dict)

    def __init__(self, api_service):
        super().__init__()

        self.api_service = api_service

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                font-family: Arial;
            }

            QFrame#loginCard {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #E4EAF1;
            }

            QLabel#title {
                font-size: 27px;
                font-weight: bold;
                color: #172B4D;
            }

            QLabel#subtitle {
                font-size: 13px;
                color: #718096;
            }

            QLabel#fieldLabel {
                font-size: 13px;
                font-weight: bold;
                color: #172B4D;
            }

            QLineEdit {
                border: 1px solid #DCE5EF;
                border-radius: 7px;
                padding: 12px;
                font-size: 14px;
                background-color: white;
            }

            QLineEdit:focus {
                border: 1px solid #278F8B;
            }

            QPushButton#loginButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 13px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#loginButton:hover {
                background-color: #207A77;
            }
        """)

        self.setup_ui()

    def setup_ui(self):

        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(430)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(17)

        # Logo
        logo = QLabel("DENTAL CARE")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            color: #278F8B;
            font-size: 24px;
            font-weight: bold;
        """)

        layout.addWidget(logo)

        # Tiêu đề
        title = QLabel("Đăng nhập")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "Đăng nhập để sử dụng các dịch vụ của chúng tôi."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # Username
        username_label = QLabel("Tên đăng nhập")
        username_label.setObjectName("fieldLabel")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(
            "Nhập tên đăng nhập"
        )

        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # Password
        password_label = QLabel("Mật khẩu")
        password_label.setObjectName("fieldLabel")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText(
            "Nhập mật khẩu"
        )
        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # Thông báo lỗi
        self.message_label = QLabel("")
        self.message_label.setStyleSheet(
            "color: #D64545; font-size: 12px;"
        )
        self.message_label.setWordWrap(True)

        layout.addWidget(self.message_label)

        # Nút đăng nhập
        self.login_button = QPushButton("ĐĂNG NHẬP")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.handle_login)

        layout.addWidget(self.login_button)

        root_layout.addWidget(card)

        self.password_input.returnPressed.connect(
            self.handle_login
        )

    def handle_login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.message_label.setText(
                "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu."
            )
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("ĐANG ĐĂNG NHẬP...")
        self.message_label.clear()

        try:
            # Bước 1: Đăng nhập lấy JWT
            result = self.api_service.login(
                username,
                password
            )

            if not result.get("success"):
                error_data = result.get("data") or {}

                message = (
                    error_data.get("detail")
                    or result.get("message")
                    or "Đăng nhập thất bại."
                )

                self.message_label.setText(message)
                return

            # Bước 2: Lấy thông tin tài khoản
            user_result = self.api_service.get_current_user()

            if not user_result.get("success"):
                self.api_service.logout()

                self.message_label.setText(
                    "Không lấy được thông tin tài khoản."
                )
                return

            user_data = user_result.get("data") or {}

            # Chỉ cho phép tài khoản bệnh nhân vào cổng bệnh nhân
            if user_data.get("role") != "PATIENT":
                self.api_service.logout()

                self.message_label.setText(
                    "Tài khoản này không thuộc nhóm bệnh nhân."
                )
                return

            # Bước 3: Lấy hồ sơ bệnh nhân
            profile_result = (
                self.api_service.get_patient_profile()
            )

            if profile_result.get("success"):
                profile_data = profile_result.get("data") or {}
                user_data.update(profile_data)

            # Phát tín hiệu đăng nhập thành công
            self.login_success.emit(user_data)

        except Exception as error:
            self.message_label.setText(
                f"Đã xảy ra lỗi: {error}"
            )

        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("ĐĂNG NHẬP")
