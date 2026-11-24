
from PySide6.QtWidgets import QMessageBox


class ConfirmDialog:

    @staticmethod
    def confirm(parent, title, message):
        result = QMessageBox.question(
            parent,
            title,
            message,
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        return result == QMessageBox.StandardButton.Yes

    @staticmethod
    def show_success(parent, message):
        QMessageBox.information(
            parent,
            "Thành công",
            message
        )

    @staticmethod
    def show_error(parent, message):
        QMessageBox.critical(
            parent,
            "Có lỗi xảy ra",
            message
        )
