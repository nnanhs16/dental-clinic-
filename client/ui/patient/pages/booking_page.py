
from datetime import datetime
from zoneinfo import ZoneInfo

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox,
    QDateEdit, QTimeEdit, QTextEdit,
    QFrame, QMessageBox, QFormLayout
)
from PySide6.QtCore import QDate, QTime, Qt


class BookingPage(QWidget):

    def __init__(self, api_service=None):
        super().__init__()

        self.api_service = api_service
        self.doctors = []
        self.services = []
        self.selected_doctor = None

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                color: #172B4D;
                font-family: Arial;
            }

            QFrame#bookingCard {
                background-color: white;
                border: 1px solid #E4EAF1;
                border-radius: 12px;
            }

            QLabel#pageTitle {
                font-size: 23px;
                font-weight: bold;
                color: #172B4D;
            }

            QLabel#description {
                font-size: 13px;
                color: #718096;
            }

            QLabel {
                font-size: 13px;
            }

            QComboBox, QDateEdit, QTimeEdit, QTextEdit {
                background-color: white;
                border: 1px solid #DCE5EF;
                border-radius: 7px;
                padding: 9px;
                font-size: 13px;
            }

            QComboBox:focus, QDateEdit:focus,
            QTimeEdit:focus, QTextEdit:focus {
                border: 1px solid #278F8B;
            }

            QPushButton#submitButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 13px 20px;
                font-weight: bold;
            }

            QPushButton#submitButton:hover {
                background-color: #207A77;
            }

            QPushButton#refreshButton {
                background-color: #E8F3F2;
                color: #278F8B;
                border: none;
                border-radius: 7px;
                padding: 9px 15px;
            }
        """)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(15)

        title = QLabel("Đặt lịch khám")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Vui lòng điền thông tin để đặt lịch thăm khám tại Dental Care."
        )
        subtitle.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Khung form
        card = QFrame()
        card.setObjectName("bookingCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 22, 25, 22)
        card_layout.setSpacing(18)

        form = QFormLayout()
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignLeft)

        # Chọn bác sĩ
        self.doctor_combo = QComboBox()
        self.doctor_combo.setMinimumHeight(42)

        form.addRow("Bác sĩ:", self.doctor_combo)

        # Chọn dịch vụ
        self.service_combo = QComboBox()
        self.service_combo.setMinimumHeight(42)

        form.addRow("Dịch vụ khám:", self.service_combo)

        # Chọn ngày
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.setDate(QDate.currentDate().addDays(1))
        self.date_edit.setMinimumHeight(42)

        form.addRow("Ngày khám:", self.date_edit)

        # Chọn giờ
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(8, 0))
        self.time_edit.setMinimumHeight(42)

        form.addRow("Giờ khám:", self.time_edit)

        # Lý do khám
        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText(
            "Ví dụ: Đau răng hàm, muốn kiểm tra răng miệng..."
        )
        self.reason_input.setFixedHeight(100)

        form.addRow("Lý do khám:", self.reason_input)

        card_layout.addLayout(form)

        # Hiển thị trạng thái
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet(
            "color: #718096; font-size: 12px;"
        )

        card_layout.addWidget(self.status_label)

        # Các nút
        button_layout = QHBoxLayout()

        refresh_button = QPushButton("Làm mới dữ liệu")
        refresh_button.setObjectName("refreshButton")
        refresh_button.clicked.connect(self.load_data)

        self.submit_button = QPushButton("XÁC NHẬN ĐẶT LỊCH")
        self.submit_button.setObjectName("submitButton")
        self.submit_button.clicked.connect(self.submit_booking)

        button_layout.addWidget(refresh_button)
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)

        card_layout.addLayout(button_layout)

        main_layout.addWidget(card)
        main_layout.addStretch()

    def get_list_data(self, result):
        data = result.get("data", [])

        if isinstance(data, dict):
            data = data.get("results", [])

        return data if isinstance(data, list) else []

    def load_data(self):
        if not self.api_service:
            self.status_label.setText("Chưa kết nối API.")
            return

        self.status_label.setText(
            "Đang tải danh sách bác sĩ và dịch vụ..."
        )

        # Tải bác sĩ
        doctor_result = self.api_service.get_doctors()

        if not doctor_result.get("success"):
            self.status_label.setText(
                "Không tải được danh sách bác sĩ. "
                "Vui lòng đăng nhập lại."
            )
            return

        self.doctors = self.get_list_data(doctor_result)

        # Tải dịch vụ
        service_result = self.api_service.get_services()

        if not service_result.get("success"):
            self.status_label.setText(
                "Không tải được danh sách dịch vụ."
            )
            return

        self.services = self.get_list_data(service_result)

        self.doctor_combo.clear()
        self.service_combo.clear()

        for doctor in self.doctors:
            name = (
                doctor.get("full_name")
                or doctor.get("username")
                or f"Bác sĩ {doctor.get('id')}"
            )

            self.doctor_combo.addItem(
                name,
                doctor.get("id")
            )

        for service in self.services:
            name = service.get("name", "Dịch vụ")
            price = service.get("price", 0)

            try:
                price_text = f"{float(price):,.0f} VNĐ"
            except (ValueError, TypeError):
                price_text = str(price)

            self.service_combo.addItem(
                f"{name} - {price_text}",
                name
            )

        # Chọn lại bác sĩ nếu đã được truyền từ trang bác sĩ
        if self.selected_doctor:
            self.set_selected_doctor(self.selected_doctor)

        if not self.doctors or not self.services:
            self.status_label.setText(
                "Hiện chưa có đủ bác sĩ hoặc dịch vụ để đặt lịch."
            )
        else:
            self.status_label.setText(
                f"Đã tải {len(self.doctors)} bác sĩ và "
                f"{len(self.services)} dịch vụ."
            )

    def set_selected_doctor(self, doctor):
        self.selected_doctor = doctor

        doctor_id = doctor.get("id")

        for index in range(self.doctor_combo.count()):
            if self.doctor_combo.itemData(index) == doctor_id:
                self.doctor_combo.setCurrentIndex(index)
                break

    def submit_booking(self):
        if not self.api_service:
            return

        doctor_id = self.doctor_combo.currentData()
        service_name = self.service_combo.currentData()

        if not doctor_id or not service_name:
            QMessageBox.warning(
                self,
                "Thiếu thông tin",
                "Vui lòng chọn bác sĩ và dịch vụ khám."
            )
            return

        reason = self.reason_input.toPlainText().strip()

        if not reason:
            QMessageBox.warning(
                self,
                "Thiếu thông tin",
                "Vui lòng nhập lý do khám."
            )
            return

        selected_date = self.date_edit.date()
        selected_time = self.time_edit.time()

        appointment_date = datetime(
            selected_date.year(),
            selected_date.month(),
            selected_date.day(),
            selected_time.hour(),
            selected_time.minute(),
            tzinfo=ZoneInfo("Asia/Ho_Chi_Minh")
        )

        if appointment_date <= datetime.now(
            ZoneInfo("Asia/Ho_Chi_Minh")
        ):
            QMessageBox.warning(
                self,
                "Ngày giờ không hợp lệ",
                "Vui lòng chọn thời gian trong tương lai."
            )
            return

        booking_data = {
            "doctor": doctor_id,
            "service_name": service_name,
            "appointment_datetime": appointment_date.isoformat(),
            "reason": reason
        }

        self.submit_button.setEnabled(False)
        self.submit_button.setText("ĐANG GỬI...")

        try:
            result = self.api_service.create_appointment(
                booking_data
            )

            if result.get("success"):
                QMessageBox.information(
                    self,
                    "Đặt lịch thành công",
                    "Lịch khám của bạn đã được gửi thành công."
                )

                self.reason_input.clear()

                self.status_label.setText(
                    "Đặt lịch thành công. "
                    "Trạng thái ban đầu: Chờ xác nhận."
                )

            else:
                error_data = result.get("data") or {}

                if isinstance(error_data, dict):
                    error_message = "\n".join(
                        f"{key}: {value}"
                        for key, value in error_data.items()
                    )
                else:
                    error_message = result.get(
                        "message",
                        "Không thể đặt lịch."
                    )

                QMessageBox.warning(
                    self,
                    "Đặt lịch thất bại",
                    error_message
                )

        finally:
            self.submit_button.setEnabled(True)
            self.submit_button.setText("XÁC NHẬN ĐẶT LỊCH")
