
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFrame, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt


class ServicesPage(QWidget):

    def __init__(self, api_service=None):
        super().__init__()

        self.api_service = api_service
        self.services = []

        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FB;
                color: #172B4D;
                font-family: Arial;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #DCE5EF;
                border-radius: 8px;
                padding: 11px;
                font-size: 13px;
            }

            QPushButton {
                background-color: #278F8B;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #207A77;
            }

            QFrame#serviceCard {
                background-color: white;
                border: 1px solid #E4EAF1;
                border-radius: 12px;
            }

            QLabel#serviceName {
                font-size: 17px;
                font-weight: bold;
                color: #172B4D;
            }

            QLabel#serviceDescription {
                font-size: 13px;
                color: #718096;
            }

            QLabel#servicePrice {
                font-size: 18px;
                font-weight: bold;
                color: #278F8B;
            }

            QLabel#serviceInfo {
                font-size: 12px;
                color: #718096;
            }
        """)

        self.setup_ui()
        self.load_services()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(18)

        # Tiêu đề
        title = QLabel("Dịch vụ nha khoa")
        title.setStyleSheet(
            "font-size: 23px; font-weight: bold;"
        )

        subtitle = QLabel(
            "Khám phá các dịch vụ chăm sóc răng miệng tại Dental Care."
        )
        subtitle.setStyleSheet(
            "font-size: 13px; color: #718096;"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Thanh tìm kiếm
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Nhập tên dịch vụ cần tìm..."
        )
        self.search_input.textChanged.connect(
            self.filter_services
        )

        refresh_button = QPushButton("Làm mới")
        refresh_button.clicked.connect(self.load_services)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(refresh_button)

        main_layout.addLayout(search_layout)

        # Khu vực hiển thị dịch vụ
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
            "color: #718096; font-size: 12px;"
        )
        main_layout.addWidget(self.status_label)

    def load_services(self):
        if not self.api_service:
            self.status_label.setText(
                "Chưa kết nối dịch vụ API."
            )
            return

        self.status_label.setText("Đang tải danh sách dịch vụ...")

        result = self.api_service.get_services()

        if not result.get("success"):
            self.status_label.setText(
                result.get("message", "Không thể tải dịch vụ.")
            )
            return

        data = result.get("data", [])

        # Hỗ trợ cả API trả về danh sách trực tiếp
        # hoặc dạng phân trang có trường results
        if isinstance(data, dict):
            data = data.get("results", [])

        if not isinstance(data, list):
            self.status_label.setText(
                "Dữ liệu dịch vụ không đúng định dạng."
            )
            return

        self.services = data
        self.filter_services()

    def filter_services(self):
        keyword = self.search_input.text().strip().lower()

        filtered = [
            service for service in self.services
            if keyword in str(service.get("name", "")).lower()
        ]

        self.display_services(filtered)

    def display_services(self, services):
        # Xóa các thẻ cũ
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if not services:
            empty_label = QLabel(
                "Không tìm thấy dịch vụ phù hợp."
            )
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet(
                "font-size: 15px; color: #718096; padding: 30px;"
            )

            self.grid_layout.addWidget(empty_label, 0, 0)
            self.status_label.setText("Không có dịch vụ để hiển thị.")
            return

        for index, service in enumerate(services):
            card = self.create_service_card(service)

            row = index // 2
            column = index % 2

            self.grid_layout.addWidget(card, row, column)

        self.status_label.setText(
            f"Tìm thấy {len(services)} dịch vụ."
        )

    def create_service_card(self, service):
        card = QFrame()
        card.setObjectName("serviceCard")
        card.setMinimumHeight(190)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        name = QLabel(service.get("name", "Dịch vụ"))
        name.setObjectName("serviceName")
        name.setWordWrap(True)

        category = QLabel(
            service.get("category_display")
            or service.get("category", "Nha khoa")
        )
        category.setStyleSheet(
            "color: #278F8B; font-size: 12px; font-weight: bold;"
        )

        description = QLabel(
            service.get("description") or "Chưa có mô tả."
        )
        description.setObjectName("serviceDescription")
        description.setWordWrap(True)

        price = service.get("price", 0)

        try:
            price_text = f"{float(price):,.0f} VNĐ"
        except (ValueError, TypeError):
            price_text = f"{price} VNĐ"

        price_label = QLabel(price_text)
        price_label.setObjectName("servicePrice")

        duration = service.get("duration", 0)
        duration_label = QLabel(
            f"Thời gian thực hiện: {duration} phút"
        )
        duration_label.setObjectName("serviceInfo")

        layout.addWidget(name)
        layout.addWidget(category)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(price_label)
        layout.addWidget(duration_label)

        return card
