
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QStackedWidget
)

from client.ui.components.sidebar import Sidebar
from client.ui.components.header import Header
from client.ui.pages.dashboard_page import DashboardPage
from client.ui.pages.placeholder_page import PlaceholderPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dental Care - Clinic Management System")
        self.setMinimumSize(1200, 750)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        root_layout.addWidget(self.sidebar)

        # Khu vực bên phải
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Header
        self.header = Header()
        right_layout.addWidget(self.header)

        # Nội dung các trang
        self.stack = QStackedWidget()
        self.pages = {}

        self.add_page("dashboard", DashboardPage(), "Tổng quan")

        self.add_page(
            "patients",
            PlaceholderPage("Quản lý bệnh nhân"),
            "Bệnh nhân"
        )

        self.add_page(
            "appointments",
            PlaceholderPage("Quản lý lịch hẹn"),
            "Lịch hẹn"
        )

        self.add_page(
            "clinical",
            PlaceholderPage("Khám và điều trị"),
            "Khám và điều trị"
        )

        self.add_page(
            "accounting",
            PlaceholderPage("Quản lý thanh toán"),
            "Thanh toán"
        )

        self.add_page(
            "employees",
            PlaceholderPage("Quản lý nhân sự"),
            "Nhân sự"
        )

        self.add_page(
            "reports",
            PlaceholderPage("Báo cáo thống kê"),
            "Báo cáo thống kê"
        )

        self.add_page(
            "settings",
            PlaceholderPage("Cài đặt hệ thống"),
            "Cài đặt"
        )

        right_layout.addWidget(self.stack)
        root_layout.addWidget(right_widget)

        # Kết nối điều hướng
        self.sidebar.page_changed.connect(self.navigate_to)

    def add_page(self, page_id, page, title):
        self.pages[page_id] = {
            "widget": page,
            "title": title
        }
        self.stack.addWidget(page)

    def navigate_to(self, page_id):
        if page_id not in self.pages:
            return

        page_info = self.pages[page_id]

        self.stack.setCurrentWidget(page_info["widget"])
        self.header.set_title(page_info["title"])
