
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt


class DataTable(QTableWidget):
    def __init__(self, headers, parent=None):
        super().__init__(0, len(headers), parent)

        self.setHorizontalHeaderLabels(headers)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.verticalHeader().setVisible(False)

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #F8FAFC;
                border: 1px solid #E8EDF3;
                border-radius: 8px;
                gridline-color: #E8EDF3;
                font-size: 13px;
            }

            QHeaderView::section {
                background-color: #F4F7FB;
                color: #52627A;
                padding: 11px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QTableWidget::item:selected {
                background-color: #D8F0EE;
                color: #172B4D;
            }
        """)

    def set_data(self, rows):
        self.setRowCount(0)

        for row_data in rows:
            row_index = self.rowCount()
            self.insertRow(row_index)

            for column, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )
                self.setItem(row_index, column, item)

    def selected_row_data(self):
        row = self.currentRow()

        if row < 0:
            return None

        return [
            self.item(row, column).text()
            if self.item(row, column) else ""
            for column in range(self.columnCount())
        ]
