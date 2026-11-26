
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow
)

from client.services.api_service import APIService

from client.ui.patient.pages.login_page import LoginPage
from client.ui.patient.patient_main_window import PatientMainWindow


class PatientLoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dental Care - Đăng nhập")
        self.setFixedSize(1000, 700)

        # Dùng chung APIService cho toàn bộ ứng dụng
        self.api_service = APIService()

        self.login_page = LoginPage(self.api_service)

        self.setCentralWidget(self.login_page)

        # Kết nối sự kiện đăng nhập thành công
        self.login_page.login_success.connect(
            self.open_patient_window
        )

        self.patient_window = None

    def open_patient_window(self, user_data):

        self.patient_window = PatientMainWindow(
            api_service=self.api_service,
            user_data=user_data
        )

        self.patient_window.show()

        # Ẩn màn hình đăng nhập
        self.hide()


def main():

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = PatientLoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
