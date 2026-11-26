
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QFrame, QScrollArea
)
from PySide6.QtCore import Qt


class AccountPage(QWidget):
    def __init__(self, api_service, user_data=None):
        super().__init__()

        self.api_service = api_service
        self.user_data = user_data or {}

        self.setup_ui()
        self.load_profile()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        title = QLabel("Tài khoản cá nhân")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #173B57;
        """)

        subtitle = QLabel(
            "Quản lý và cập nhật thông tin cá nhân của bạn."
        )
        subtitle.setStyleSheet("color: #718096; font-size: 13px;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(18)

        form_title = QLabel("Thông tin cá nhân")
        form_title.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #173B57;
            border: none;
        """)

        card_layout.addWidget(form_title)

        form = QFormLayout()
        form.setSpacing(15)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.full_name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.date_of_birth_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.address_input = QLineEdit()
        self.occupation_input = QLineEdit()

        self.date_of_birth_input.setPlaceholderText("Ví dụ: 2005-03-16")
        self.gender_input.setPlaceholderText("Ví dụ: FEMALE hoặc MALE")

        self.inputs = [
            self.full_name_input,
            self.email_input,
            self.phone_input,
            self.date_of_birth_input,
            self.gender_input,
            self.address_input,
            self.occupation_input
        ]

        for field in self.inputs:
            field.setMinimumHeight(38)
            field.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #CBD5E0;
                    border-radius: 6px;
                    padding: 7px 10px;
                    font-size: 13px;
                    background-color: white;
                }
                QLineEdit:focus {
                    border: 1px solid #3182CE;
                }
            """)

        form.addRow("Họ và tên:", self.full_name_input)
        form.addRow("Email:", self.email_input)
        form.addRow("Số điện thoại:", self.phone_input)
        form.addRow("Ngày sinh:", self.date_of_birth_input)
        form.addRow("Giới tính:", self.gender_input)
        form.addRow("Địa chỉ:", self.address_input)
        form.addRow("Nghề nghiệp:", self.occupation_input)

        card_layout.addLayout(form)

        note = QLabel(
            "Lưu ý: Ngày sinh nhập theo định dạng YYYY-MM-DD."
        )
        note.setStyleSheet(
            "color: #718096; font-size: 12px; border: none;"
        )
        card_layout.addWidget(note)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("Lưu thay đổi")
        self.save_button.setMinimumSize(140, 42)
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #1E6A8D;
                color: white;
                border: none;
                border-radius: 7px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #15516F;
            }
        """)
        self.save_button.clicked.connect(self.save_profile)

        button_layout.addWidget(self.save_button)
        card_layout.addLayout(button_layout)

        main_layout.addWidget(card)
        main_layout.addStretch()

    def load_profile(self):
        result = self.api_service.get_patient_profile()

        if not result.get("success"):
            QMessageBox.warning(
                self,
                "Thông báo",
                result.get("message", "Không thể tải thông tin cá nhân.")
            )
            return

        profile = result.get("data", {})

        # Một số API có thể trả dữ liệu bên trong key results.
        if isinstance(profile, dict) and "results" in profile:
            profile = profile["results"]

        if not isinstance(profile, dict):
            QMessageBox.warning(
                self,
                "Thông báo",
                "Dữ liệu hồ sơ không đúng định dạng."
            )
            return

        self.full_name_input.setText(
            str(profile.get("full_name") or "")
        )
        self.email_input.setText(
            str(profile.get("email") or "")
        )
        self.phone_input.setText(
            str(profile.get("phone_number") or "")
        )
        self.date_of_birth_input.setText(
            str(profile.get("date_of_birth") or "")
        )
        self.gender_input.setText(
            str(profile.get("gender") or "")
        )
        self.address_input.setText(
            str(profile.get("address") or "")
        )
        self.occupation_input.setText(
            str(profile.get("occupation") or "")
        )

    def save_profile(self):
        full_name = self.full_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        date_of_birth = self.date_of_birth_input.text().strip()
        gender = self.gender_input.text().strip()
        address = self.address_input.text().strip()
        occupation = self.occupation_input.text().strip()

        if not full_name:
            QMessageBox.warning(
                self, "Thông báo", "Họ và tên không được để trống."
            )
            return

        if date_of_birth:
            from datetime import date

            try:
                date.fromisoformat(date_of_birth)
            except ValueError:
                QMessageBox.warning(
                    self,
                    "Ngày sinh không hợp lệ",
                    "Vui lòng nhập ngày sinh theo định dạng YYYY-MM-DD."
                )
                return

        data = {
            "full_name": full_name,
            "email": email,
            "phone_number": phone,
            "gender": gender,
            "address": address,
            "occupation": occupation
        }

        if date_of_birth:
            data["date_of_birth"] = date_of_birth
        else:
            data["date_of_birth"] = None

        self.save_button.setEnabled(False)
        self.save_button.setText("Đang lưu...")

        result = self.api_service.update_patient_profile(data)

        self.save_button.setEnabled(True)
        self.save_button.setText("Lưu thay đổi")

        if result.get("success"):
            QMessageBox.information(
                self,
                "Thành công",
                "Thông tin cá nhân đã được cập nhật."
            )
            self.load_profile()
        else:
            QMessageBox.warning(
                self,
                "Không thể cập nhật",
                result.get("message", "Đã xảy ra lỗi khi lưu thông tin.")
            )
