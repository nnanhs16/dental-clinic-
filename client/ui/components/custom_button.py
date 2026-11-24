
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class CustomButton(QPushButton):
    def __init__(self, text, variant="primary", parent=None):
        super().__init__(text, parent)

        # Thiết lập con trỏ chuột
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Thiết lập kích thước
        self.setMinimumHeight(38)

        # Các kiểu nút
        styles = {
            "primary": """
                background-color: #278F8B;
                color: white;
                border: none;
            """,

            "secondary": """
                background-color: #E8EDF3;
                color: #34445C;
                border: none;
            """,

            "danger": """
                background-color: #DC5555;
                color: white;
                border: none;
            """,

            "outline": """
                background-color: white;
                color: #278F8B;
                border: 1px solid #278F8B;
            """
        }

        # Lấy kiểu nút được chọn
        style = styles.get(variant, styles["primary"])

        # Áp dụng giao diện
        self.setStyleSheet(f"""
            QPushButton {{
                {style}
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }}

            QPushButton:hover {{
                border: 1px solid #1F7773;
            }}

            QPushButton:disabled {{
                background-color: #CBD5E0;
                color: #718096;
            }}
        """)
