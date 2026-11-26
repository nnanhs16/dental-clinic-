
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

# Components
from client.ui.patient.components.patient_sidebar import PatientSidebar
from client.ui.patient.components.patient_header import PatientHeader

# Patient pages
from client.ui.patient.pages.home_page import HomePage
from client.ui.patient.pages.services_page import ServicesPage
from client.ui.patient.pages.doctors_page import DoctorsPage
from client.ui.patient.pages.booking_page import BookingPage
from client.ui.patient.pages.history_page import HistoryPage
from client.ui.patient.pages.account_page import AccountPage
from client.ui.patient.pages.reviews_page import ReviewsPage


class PatientMainWindow(QMainWindow):

    def __init__(self, api_service=None, user_data=None):
        super().__init__()

        self.api_service = api_service
        self.user_data = user_data or {}
        self.selected_doctor = None

        self.setWindowTitle("Dental Care - Cổng thông tin bệnh nhân")
        self.setMinimumSize(1200, 750)

        self.setup_ui()

    # ==========================================
    # KHỞI TẠO GIAO DIỆN
    # ==========================================

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # =====================================
        # 1. SIDEBAR
        # =====================================

        self.sidebar = PatientSidebar()
        root_layout.addWidget(self.sidebar)

        # =====================================
        # 2. KHU VỰC BÊN PHẢI
        # =====================================

        right_widget = QWidget()

        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # =====================================
        # 3. HEADER
        # =====================================

        user_name = (
            self.user_data.get("full_name")
            or self.user_data.get("username")
            or "Bệnh nhân"
        )

        self.header = PatientHeader(user_name)
        right_layout.addWidget(self.header)

        # =====================================
        # 4. STACKED WIDGET
        # =====================================

        self.stack = QStackedWidget()
        self.pages = {}

        # =====================================
        # 5. TRANG CHỦ
        # =====================================

        self.home_page = HomePage(self.user_data)

        self.home_page.parent_window = self

        self.home_page.booking_requested.connect(
            lambda: self.navigate_to("booking")
        )

        self.register_page(
            "home",
            self.home_page,
            "Trang chủ"
        )

        # =====================================
        # 6. TRANG DỊCH VỤ NHA KHOA
        # =====================================

        self.services_page = ServicesPage(
            self.api_service
        )

        self.register_page(
            "services",
            self.services_page,
            "Dịch vụ nha khoa"
        )

        # =====================================
        # 7. TRANG ĐỘI NGŨ BÁC SĨ
        # =====================================

        self.doctors_page = DoctorsPage(
            self.api_service
        )

        self.doctors_page.booking_requested.connect(
            self.select_doctor_for_booking
        )

        self.register_page(
            "doctors",
            self.doctors_page,
            "Đội ngũ bác sĩ"
        )

        # =====================================
        # 8. TRANG ĐẶT LỊCH KHÁM
        # =====================================

        self.booking_page = BookingPage(
            self.api_service
        )

        self.register_page(
            "booking",
            self.booking_page,
            "Đặt lịch khám"
        )

        # =====================================
        # 9. TRANG LỊCH SỬ KHÁM
        # =====================================

        self.history_page = HistoryPage(
            self.api_service
        )

        self.register_page(
            "history",
            self.history_page,
            "Lịch sử khám"
        )

        # =====================================
        # 10. TRANG TÀI KHOẢN CÁ NHÂN
        # =====================================

        self.account_page = AccountPage(
            api_service=self.api_service,
            user_data=self.user_data
        )

        self.register_page(
            "account",
            self.account_page,
            "Tài khoản cá nhân"
        )

        # =====================================
        # 11. TRANG ĐÁNH GIÁ DỊCH VỤ
        # =====================================

        self.reviews_page = ReviewsPage(
            self.api_service
        )

        self.register_page(
            "reviews",
            self.reviews_page,
            "Đánh giá dịch vụ"
        )

        # =====================================
        # 12. HOÀN THIỆN GIAO DIỆN
        # =====================================

        right_layout.addWidget(self.stack)

        root_layout.addWidget(right_widget)

        # Kết nối sự kiện chuyển trang từ Sidebar
        self.sidebar.page_changed.connect(
            self.navigate_to
        )

        # Mặc định mở trang chủ
        self.navigate_to("home")

    # ==========================================
    # ĐĂNG KÝ TRANG
    # ==========================================

    def register_page(self, page_id, page, title):

        self.pages[page_id] = {
            "widget": page,
            "title": title
        }

        self.stack.addWidget(page)

    # ==========================================
    # CHUYỂN TRANG
    # ==========================================

    def navigate_to(self, page_id):

        if page_id not in self.pages:
            return

        page_info = self.pages[page_id]

        # Hiển thị trang được chọn
        self.stack.setCurrentWidget(
            page_info["widget"]
        )

        # Cập nhật tiêu đề Header
        self.header.set_title(
            page_info["title"]
        )

        # Tải lại dữ liệu khi mở trang lịch sử
        if page_id == "history":
            self.history_page.load_all_data()

        # Tải lại thông tin cá nhân
        elif page_id == "account":
            self.account_page.load_profile()

        # Tải lại danh sách đánh giá
        elif page_id == "reviews":
            self.reviews_page.load_reviews()

    # ==========================================
    # CHỌN BÁC SĨ ĐỂ ĐẶT LỊCH
    # ==========================================

    def select_doctor_for_booking(self, doctor):

        self.selected_doctor = doctor

        self.booking_page.set_selected_doctor(
            doctor
        )

        self.navigate_to("booking")
