
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame,
    QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt, Signal


class DoctorsPage(QWidget):

    booking_requested = Signal(dict)

    def __init__(self, api_service=None):
        super().__init__()

        self.api_service = api_service
        self.doctors = []

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                color: #172B4D;
                font-family: Arial;
            }

            QFrame#doctorCard {
                background-color: white;
                border: 1px solid #E4EAF1;
                border-radius: 12px;
            }

            QLabel#doctorName {
                font-size: 18px;
                font-weight: bold;
                color: #172B4D;
            }

            QLabel#doctorInfo {
                font-size: 13px;
                color: #718096;
            }

            QLabel#doctorRole {
                color: #278F8B;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #207A77;
            }
        """)

        self.setup_ui()
        self.load_doctors()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(18)

        title = QLabel("Đội ngũ bác sĩ")
        title.setStyleSheet(
            "font-size: 23px; font-weight: bold;"
        )

        subtitle = QLabel(
            "Tìm hiểu thông tin đội ngũ bác sĩ tại Dental Care."
        )
        subtitle.setStyleSheet(
            "font-size: 13px; color: #718096;"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Nút tải lại danh sách
        top_layout = QHBoxLayout()
        top_layout.addStretch()

        refresh_button = QPushButton("↻ Làm mới")
        refresh_button.clicked.connect(self.load_doctors)

        top_layout.addWidget(refresh_button)
        main_layout.addLayout(top_layout)

        # Khu vực hiển thị danh sách bác sĩ
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.content_widget = QWidget()
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(18)
        self.grid_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            "font-size: 12px; color: #718096;"
        )
        main_layout.addWidget(self.status_label)

    def load_doctors(self):
        if not self.api_service:
            self.status_label.setText(
                "Chưa kết nối API."
            )
            return

        self.status_label.setText(
            "Đang tải danh sách bác sĩ..."
        )

        result = self.api_service.get_doctors()

        if not result.get("success"):
            error_data = result.get("data") or {}

            message = (
                error_data.get("detail")
                or result.get("message")
                or "Không thể tải danh sách bác sĩ."
            )

            self.status_label.setText(message)
            return

        data = result.get("data", [])

        if isinstance(data, dict):
            data = data.get("results", [])

        if not isinstance(data, list):
            self.status_label.setText(
                "Dữ liệu bác sĩ không đúng định dạng."
            )
            return

        self.doctors = data
        self.display_doctors()

    def display_doctors(self):
        # Xóa các thẻ cũ
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not self.doctors:
            empty_label = QLabel(
                "Hiện chưa có bác sĩ nào trong danh sách."
            )
            empty_label.setAlignment(Qt.AlignCenter)

            self.grid_layout.addWidget(empty_label, 0, 0)

            self.status_label.setText(
                "Không có dữ liệu bác sĩ."
            )
            return

        for index, doctor in enumerate(self.doctors):
            card = self.create_doctor_card(doctor)

            row = index // 2
            column = index % 2

            self.grid_layout.addWidget(card, row, column)

        self.status_label.setText(
            f"Tìm thấy {len(self.doctors)} bác sĩ."
        )

    def create_doctor_card(self, doctor):
        card = QFrame()
        card.setObjectName("doctorCard")
        card.setMinimumHeight(210)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Tên bác sĩ
        name = QLabel(
            doctor.get("full_name")
            or doctor.get("username")
            or "Bác sĩ"
        )
        name.setObjectName("doctorName")
        name.setWordWrap(True)

        role = QLabel("BÁC SĨ NHA KHOA")
        role.setObjectName("doctorRole")

        email = QLabel(
            f"Email: {doctor.get('email') or 'Chưa cập nhật'}"
        )
        email.setObjectName("doctorInfo")
        email.setWordWrap(True)

        phone = QLabel(
            f"Điện thoại: "
            f"{doctor.get('phone_number') or 'Chưa cập nhật'}"
        )
        phone.setObjectName("doctorInfo")

        doctor_id = QLabel(
            f"Mã bác sĩ: {doctor.get('id', '')}"
        )
        doctor_id.setObjectName("doctorInfo")

        layout.addWidget(name)
        layout.addWidget(role)
        layout.addWidget(email)
        layout.addWidget(phone)
        layout.addWidget(doctor_id)
        layout.addStretch()

        booking_button = QPushButton("Đặt lịch với bác sĩ")
        booking_button.clicked.connect(
            lambda checked=False, d=doctor:
            self.booking_requested.emit(d)
        )

        layout.addWidget(booking_button)

        return card
