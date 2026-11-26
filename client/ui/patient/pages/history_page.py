
from datetime import datetime
from zoneinfo import ZoneInfo

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QTabWidget, QMessageBox,
    QDialog, QFormLayout, QDateTimeEdit,
    QDialogButtonBox, QHeaderView, QFrame
)
from PySide6.QtCore import Qt, QDateTime


class RescheduleDialog(QDialog):

    def __init__(self, current_datetime, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Đổi lịch khám")
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setCalendarPopup(True)
        self.datetime_edit.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.datetime_edit.setMinimumDateTime(
            QDateTime.currentDateTime()
        )

        try:
            current = datetime.fromisoformat(
                current_datetime.replace("Z", "+00:00")
            )
            local_time = current.astimezone(
                ZoneInfo("Asia/Ho_Chi_Minh")
            )
            self.datetime_edit.setDateTime(
                QDateTime(
                    local_time.year,
                    local_time.month,
                    local_time.day,
                    local_time.hour,
                    local_time.minute
                )
            )
        except (ValueError, AttributeError):
            self.datetime_edit.setDateTime(
                QDateTime.currentDateTime().addDays(1)
            )

        form.addRow("Ngày giờ mới:", self.datetime_edit)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.button(QDialogButtonBox.Ok).setText("Xác nhận")
        buttons.button(QDialogButtonBox.Cancel).setText("Hủy")

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_datetime(self):
        selected = self.datetime_edit.dateTime().toPython()

        return selected.replace(
            tzinfo=ZoneInfo("Asia/Ho_Chi_Minh")
        ).isoformat()


class HistoryPage(QWidget):

    def __init__(self, api_service=None):
        super().__init__()

        self.api_service = api_service
        self.appointments = []
        self.medical_records = []

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                color: #172B4D;
                font-family: Arial;
            }

            QTabWidget::pane {
                border: 1px solid #E4EAF1;
                background: white;
                border-radius: 8px;
            }

            QTabBar::tab {
                background: #E8EDF3;
                color: #52627A;
                padding: 12px 22px;
                margin-right: 4px;
                border-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #278F8B;
                color: white;
                font-weight: bold;
            }

            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #E8EDF3;
                font-size: 12px;
                selection-background-color: #E0F2F1;
                selection-color: #172B4D;
            }

            QHeaderView::section {
                background-color: #EAF0F6;
                color: #52627A;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            QPushButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #207A77;
            }

            QPushButton#cancelButton {
                background-color: #D9534F;
            }

            QPushButton#cancelButton:hover {
                background-color: #B9403C;
            }
        """)

        self.setup_ui()
        self.load_all_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 22, 25, 22)
        main_layout.setSpacing(15)

        title = QLabel("Lịch hẹn và lịch sử khám")
        title.setStyleSheet(
            "font-size: 23px; font-weight: bold;"
        )

        subtitle = QLabel(
            "Theo dõi lịch hẹn, kết quả khám và lịch tái khám của bạn."
        )
        subtitle.setStyleSheet(
            "font-size: 13px; color: #718096;"
        )

        top_layout = QHBoxLayout()
        top_layout.addWidget(title)
        top_layout.addStretch()

        refresh_button = QPushButton("↻ Làm mới")
        refresh_button.clicked.connect(self.load_all_data)
        top_layout.addWidget(refresh_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(subtitle)

        self.tabs = QTabWidget()

        # Tab lịch hẹn
        appointment_tab = QWidget()
        appointment_layout = QVBoxLayout(appointment_tab)

        self.appointment_table = QTableWidget()
        self.appointment_table.setColumnCount(6)
        self.appointment_table.setHorizontalHeaderLabels([
            "Mã lịch", "Bác sĩ", "Dịch vụ",
            "Ngày giờ", "Trạng thái", "Thao tác"
        ])

        self.configure_table(self.appointment_table)
        appointment_layout.addWidget(self.appointment_table)

        self.tabs.addTab(appointment_tab, "Lịch hẹn")

        # Tab hồ sơ khám
        record_tab = QWidget()
        record_layout = QVBoxLayout(record_tab)

        self.record_table = QTableWidget()
        self.record_table.setColumnCount(6)
        self.record_table.setHorizontalHeaderLabels([
            "Ngày khám", "Bác sĩ", "Dịch vụ",
            "Chẩn đoán", "Kết quả", "Tái khám"
        ])

        self.configure_table(self.record_table)
        record_layout.addWidget(self.record_table)

        self.tabs.addTab(record_tab, "Lịch sử khám")

        main_layout.addWidget(self.tabs)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            "color: #718096; font-size: 12px;"
        )
        main_layout.addWidget(self.status_label)

    def configure_table(self, table):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(
            QTableWidget.SelectRows
        )
        table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )
        table.verticalHeader().setVisible(False)

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        table.setMinimumHeight(350)

    def extract_list(self, result):
        data = result.get("data", [])

        if isinstance(data, dict):
            data = data.get("results", [])

        return data if isinstance(data, list) else []

    def load_all_data(self):
        if not self.api_service:
            self.status_label.setText(
                "Chưa kết nối API."
            )
            return

        self.status_label.setText("Đang tải dữ liệu...")

        appointment_result = (
            self.api_service.get_appointments()
        )

        if appointment_result.get("success"):
            self.appointments = self.extract_list(
                appointment_result
            )
            self.display_appointments()
        else:
            self.appointment_table.setRowCount(0)

        record_result = (
            self.api_service.get_medical_records()
        )

        if record_result.get("success"):
            self.medical_records = self.extract_list(
                record_result
            )
            self.display_medical_records()
        else:
            self.record_table.setRowCount(0)

        if (
            appointment_result.get("success")
            and record_result.get("success")
        ):
            self.status_label.setText(
                f"Có {len(self.appointments)} lịch hẹn và "
                f"{len(self.medical_records)} hồ sơ khám."
            )
        else:
            self.status_label.setText(
                "Một số dữ liệu chưa tải được. "
                "Vui lòng kiểm tra kết nối hoặc đăng nhập lại."
            )

    def format_datetime(self, value):
        if not value:
            return "Chưa cập nhật"

        try:
            dt = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

            if dt.tzinfo:
                dt = dt.astimezone(
                    ZoneInfo("Asia/Ho_Chi_Minh")
                )

            return dt.strftime("%d/%m/%Y %H:%M")

        except (ValueError, AttributeError):
            return str(value)

    def display_appointments(self):
        self.appointment_table.setRowCount(
            len(self.appointments)
        )

        for row, appointment in enumerate(self.appointments):
            values = [
                appointment.get("id", ""),
                appointment.get("doctor_name")
                or appointment.get("doctor", ""),
                appointment.get("service_name", ""),
                self.format_datetime(
                    appointment.get("appointment_datetime")
                ),
                appointment.get("status", "")
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.appointment_table.setItem(
                    row, column, item
                )

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(3, 3, 3, 3)
            action_layout.setSpacing(5)

            status = appointment.get("status", "")

            if status in ("PENDING", "CONFIRMED"):
                change_button = QPushButton("Đổi")
                change_button.clicked.connect(
                    lambda checked=False, a=appointment:
                    self.reschedule_appointment(a)
                )

                cancel_button = QPushButton("Hủy")
                cancel_button.setObjectName("cancelButton")
                cancel_button.clicked.connect(
                    lambda checked=False, a=appointment:
                    self.cancel_appointment(a)
                )

                action_layout.addWidget(change_button)
                action_layout.addWidget(cancel_button)
            else:
                label = QLabel("Không có thao tác")
                label.setAlignment(Qt.AlignCenter)
                action_layout.addWidget(label)

            self.appointment_table.setCellWidget(
                row, 5, action_widget
            )

    def display_medical_records(self):
        self.record_table.setRowCount(
            len(self.medical_records)
        )

        for row, record in enumerate(self.medical_records):
            values = [
                self.format_datetime(
                    record.get("examination_date")
                ),
                record.get("doctor_name", ""),
                record.get("service_name", ""),
                record.get("diagnosis", ""),
                record.get("result", ""),
                record.get("follow_up_date") or "Không có"
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignCenter | Qt.AlignVCenter
                )
                item.setToolTip(str(value))

                self.record_table.setItem(
                    row, column, item
                )

    def reschedule_appointment(self, appointment):
        appointment_id = appointment.get("id")

        current_datetime = appointment.get(
            "appointment_datetime", ""
        )

        dialog = RescheduleDialog(
            current_datetime,
            self
        )

        if dialog.exec() != QDialog.Accepted:
            return

        new_datetime = dialog.get_datetime()

        result = self.api_service.update_appointment(
            appointment_id,
            {
                "appointment_datetime": new_datetime
            }
        )

        if result.get("success"):
            QMessageBox.information(
                self,
                "Thành công",
                "Đã gửi yêu cầu đổi lịch thành công."
            )
            self.load_all_data()
        else:
            self.show_api_error(
                "Không thể đổi lịch",
                result
            )

    def cancel_appointment(self, appointment):
        appointment_id = appointment.get("id")

        answer = QMessageBox.question(
            self,
            "Xác nhận hủy lịch",
            f"Bạn có chắc muốn hủy lịch hẹn #{appointment_id} không?",
            QMessageBox.Yes | QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        result = self.api_service.cancel_appointment(
            appointment_id
        )

        if result.get("success"):
            QMessageBox.information(
                self,
                "Thành công",
                "Lịch hẹn đã được hủy."
            )
            self.load_all_data()
        else:
            self.show_api_error(
                "Không thể hủy lịch",
                result
            )

    def show_api_error(self, title, result):
        error_data = result.get("data") or {}

        if isinstance(error_data, dict):
            message = "\n".join(
                f"{key}: {value}"
                for key, value in error_data.items()
            )
        else:
            message = result.get(
                "message",
                "Đã xảy ra lỗi."
            )

        QMessageBox.warning(
            self,
            title,
            message
        )
