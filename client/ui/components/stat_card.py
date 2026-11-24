
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatCard(QFrame):
    def __init__(self, title, value, description, icon=""):
        super().__init__()

        self.setObjectName("statCard")
        self.setMinimumHeight(130)

        self.setStyleSheet("""
            QFrame#statCard {
                background-color: white;
                border: 1px solid #E8EDF3;
                border-radius: 10px;
            }

            QLabel#cardTitle {
                color: #718096;
                font-size: 13px;
            }

            QLabel#cardValue {
                color: #172B4D;
                font-size: 25px;
                font-weight: bold;
            }

            QLabel#cardDescription {
                color: #278F8B;
                font-size: 12px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(8)

        title_label = QLabel(f"{icon}  {title}")
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        description_label = QLabel(description)
        description_label.setObjectName("cardDescription")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)
        layout.addStretch()
