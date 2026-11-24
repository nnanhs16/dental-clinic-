
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame
)
from PySide6.QtCore import Qt

from client.ui.components.stat_card import StatCard


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Tiêu đề
        title = QLabel("Tổng quan hoạt động")
        title.setStyleSheet("""
            font-size: 23px;
            font-weight: bold;
            color: #172B4D;
        """)

        description = QLabel(
            "Theo dõi tình hình hoạt động của phòng khám nha khoa."
        )
        description.setStyleSheet("color: #718096;")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # Các thẻ thống kê
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)

        stats = [
            ("Tổng bệnh nhân", "1.248", "+12 tháng này", "♙"),
            ("Lịch hẹn hôm nay", "24", "6 đang chờ", "▦"),
            ("Doanh thu hôm nay", "12,5 triệu", "+8,5%", "₫"),
            ("Ca điều trị", "18", "4 đang thực hiện", "✚"),
        ]

        for index, data in enumerate(stats):
            card = StatCard(*data)
            stats_layout.addWidget(card, index // 2, index % 2)

        main_layout.addLayout(stats_layout)

        # Bảng lịch hẹn
        table_title = QLabel("Lịch hẹn hôm nay")
        table_title.setStyleSheet("""
            font-size: 17px;
            font-weight: bold;
            color: #172B4D;
        """)
        main_layout.addWidget(table_title)

        table_container = QFrame()
        table_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E8EDF3;
                border-radius: 8px;
            }
        """)

        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(10, 10, 10, 10)

        table = QTableWidget(4, 4)
        table.setHorizontalHeaderLabels([
            "Thời gian",
            "Bệnh nhân",
            "Dịch vụ",
            "Trạng thái"
        ])

        appointments = [
            ["08:30", "Nguyễn Văn An", "Khám tổng quát", "Đã xác nhận"],
            ["09:30", "Trần Thị Mai", "Lấy cao răng", "Đang chờ"],
            ["10:00", "Lê Minh Tuấn", "Điều trị tủy", "Đã xác nhận"],
            ["14:00", "Phạm Thu Hà", "Niềng răng", "Chưa xác nhận"],
        ]

        for row, appointment in enumerate(appointments):
            for column, value in enumerate(appointment):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, column, item)

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        table.verticalHeader().setVisible(False)
        table.setMinimumHeight(220)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                gridline-color: #E8EDF3;
                alternate-background-color: #F8FAFC;
            }

            QHeaderView::section {
                background-color: #F4F7FB;
                color: #52627A;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        table_layout.addWidget(table)
        main_layout.addWidget(table_container)
        main_layout.addStretch()
