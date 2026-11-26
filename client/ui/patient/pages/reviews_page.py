
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTextEdit,
    QPushButton, QFrame, QMessageBox,
    QListWidget, QListWidgetItem,
    QSpinBox
)
from PySide6.QtCore import Qt


class ReviewsPage(QWidget):

    def __init__(self, api_service):
        super().__init__()

        self.api_service = api_service
        self.services = []
        self.reviews = []
        self.editing_review_id = None

        self.setup_ui()
        self.load_services()
        self.load_reviews()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(18)

        title = QLabel("Đánh giá dịch vụ")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #173B57;
        """)

        subtitle = QLabel(
            "Chia sẻ trải nghiệm của bạn để giúp phòng khám "
            "nâng cao chất lượng dịch vụ."
        )
        subtitle.setStyleSheet(
            "color: #718096; font-size: 13px;"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # =====================================
        # FORM ĐÁNH GIÁ
        # =====================================

        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
            }
        """)

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(22, 20, 22, 20)
        form_layout.setSpacing(12)

        form_title = QLabel("Gửi đánh giá")
        form_title.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #173B57;
            border: none;
        """)

        form_layout.addWidget(form_title)

        service_label = QLabel("Dịch vụ:")
        service_label.setStyleSheet("border: none;")

        self.service_combo = QComboBox()
        self.service_combo.setMinimumHeight(38)

        self.service_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                padding: 7px;
                background-color: white;
            }
        """)

        form_layout.addWidget(service_label)
        form_layout.addWidget(self.service_combo)

        rating_label = QLabel("Mức độ hài lòng:")
        rating_label.setStyleSheet("border: none;")

        self.rating_input = QSpinBox()
        self.rating_input.setRange(1, 5)
        self.rating_input.setValue(5)
        self.rating_input.setSuffix(" sao")
        self.rating_input.setMinimumHeight(38)

        form_layout.addWidget(rating_label)
        form_layout.addWidget(self.rating_input)

        comment_label = QLabel("Nội dung đánh giá:")
        comment_label.setStyleSheet("border: none;")

        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText(
            "Hãy chia sẻ trải nghiệm của bạn..."
        )
        self.comment_input.setMinimumHeight(100)

        self.comment_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CBD5E0;
                border-radius: 6px;
                padding: 8px;
                background-color: white;
            }
        """)

        form_layout.addWidget(comment_label)
        form_layout.addWidget(self.comment_input)

        # Nút thao tác
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.clear_button = QPushButton("Làm mới")
        self.clear_button.clicked.connect(
            self.reset_form
        )

        self.submit_button = QPushButton("Gửi đánh giá")
        self.submit_button.clicked.connect(
            self.submit_review
        )

        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #EDF2F7;
                color: #2D3748;
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
            }
        """)

        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #1E6A8D;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #15516F;
            }
        """)

        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        form_layout.addLayout(button_layout)

        main_layout.addWidget(form_card)

        # =====================================
        # DANH SÁCH ĐÁNH GIÁ
        # =====================================

        list_title = QLabel("Đánh giá của tôi")
        list_title.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #173B57;
        """)

        main_layout.addWidget(list_title)

        self.review_list = QListWidget()
        self.review_list.setSpacing(8)

        self.review_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        main_layout.addWidget(self.review_list)

    # =====================================
    # LẤY DANH SÁCH DỊCH VỤ
    # =====================================

    def get_list_data(self, data):

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return data.get("results", [])

        return []

    def load_services(self):

        result = self.api_service.get_services()

        if not result.get("success"):
            QMessageBox.warning(
                self,
                "Thông báo",
                result.get("message", "Không thể tải danh sách dịch vụ.")
            )
            return

        self.services = self.get_list_data(
            result.get("data", [])
        )

        self.service_combo.clear()

        for service in self.services:

            if not service.get("is_active", True):
                continue

            service_id = service.get("id")
            service_name = service.get("name", "Dịch vụ")

            self.service_combo.addItem(
                service_name,
                service_id
            )

    # =====================================
    # LẤY DANH SÁCH ĐÁNH GIÁ
    # =====================================

    def load_reviews(self):

        result = self.api_service.get_reviews()

        if not result.get("success"):
            QMessageBox.warning(
                self,
                "Thông báo",
                result.get("message", "Không thể tải đánh giá.")
            )
            return

        self.reviews = self.get_list_data(
            result.get("data", [])
        )

        self.review_list.clear()

        if not self.reviews:
            self.review_list.addItem(
                "Bạn chưa có đánh giá nào."
            )
            return

        for review in self.reviews:

            review_id = review.get("id")
            service_name = review.get(
                "service_name",
                "Dịch vụ"
            )

            rating = review.get("rating", 0)
            comment = review.get("comment", "")

            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(8, 8, 8, 8)

            name_label = QLabel(
                f"{service_name}  |  {'★' * int(rating)}"
            )
            name_label.setStyleSheet("""
                font-weight: bold;
                color: #173B57;
                font-size: 14px;
            """)

            comment_label = QLabel(
                comment or "Không có nội dung nhận xét."
            )
            comment_label.setWordWrap(True)
            comment_label.setStyleSheet(
                "color: #4A5568; font-size: 13px;"
            )

            item_layout.addWidget(name_label)
            item_layout.addWidget(comment_label)

            button_layout = QHBoxLayout()
            button_layout.addStretch()

            edit_button = QPushButton("Chỉnh sửa")
            delete_button = QPushButton("Xóa")

            edit_button.clicked.connect(
                lambda checked=False, r=review:
                self.edit_review(r)
            )

            delete_button.clicked.connect(
                lambda checked=False, rid=review_id:
                self.delete_review(rid)
            )

            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)

            item_layout.addLayout(button_layout)

            list_item = QListWidgetItem()
            list_item.setSizeHint(
                item_widget.sizeHint()
            )

            self.review_list.addItem(list_item)
            self.review_list.setItemWidget(
                list_item,
                item_widget
            )

    # =====================================
    # GỬI ĐÁNH GIÁ
    # =====================================

    def submit_review(self):

        service_id = self.service_combo.currentData()
        rating = self.rating_input.value()
        comment = self.comment_input.toPlainText().strip()

        if service_id is None:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng chọn dịch vụ."
            )
            return

        if not comment:
            QMessageBox.warning(
                self,
                "Thông báo",
                "Vui lòng nhập nội dung đánh giá."
            )
            return

        data = {
            "service": service_id,
            "rating": rating,
            "comment": comment
        }

        if self.editing_review_id is None:

            result = self.api_service.create_review(data)

            success_message = "Đánh giá đã được gửi thành công."

        else:

            result = self.api_service.update_review(
                self.editing_review_id,
                data
            )

            success_message = "Đánh giá đã được cập nhật."

        if result.get("success"):

            QMessageBox.information(
                self,
                "Thành công",
                success_message
            )

            self.reset_form()
            self.load_reviews()

        else:

            QMessageBox.warning(
                self,
                "Không thể gửi đánh giá",
                result.get("message", "Đã xảy ra lỗi.")
            )

    # =====================================
    # CHỈNH SỬA ĐÁNH GIÁ
    # =====================================

    def edit_review(self, review):

        self.editing_review_id = review.get("id")

        service_id = review.get("service")

        index = self.service_combo.findData(service_id)

        if index >= 0:
            self.service_combo.setCurrentIndex(index)

        self.rating_input.setValue(
            int(review.get("rating", 5))
        )

        self.comment_input.setPlainText(
            review.get("comment", "")
        )

        self.submit_button.setText(
            "Cập nhật đánh giá"
        )

    # =====================================
    # XÓA ĐÁNH GIÁ
    # =====================================

    def delete_review(self, review_id):

        answer = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa đánh giá này?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        result = self.api_service.delete_review(
            review_id
        )

        if result.get("success"):

            QMessageBox.information(
                self,
                "Thành công",
                "Đã xóa đánh giá."
            )

            self.load_reviews()
            self.reset_form()

        else:

            QMessageBox.warning(
                self,
                "Lỗi",
                result.get("message", "Không thể xóa đánh giá.")
            )

    # =====================================
    # LÀM MỚI FORM
    # =====================================

    def reset_form(self):

        self.editing_review_id = None

        self.rating_input.setValue(5)
        self.comment_input.clear()

        self.submit_button.setText(
            "Gửi đánh giá"
        )
