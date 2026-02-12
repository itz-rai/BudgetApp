from PySide2.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide2.QtCore import Qt

def format_currency(amount: float, currency_symbol: str = "TT$") -> str:
    return f"{currency_symbol}{amount:,.2f}"

class StatCard(QFrame):
    def __init__(self, title: str, value: float, color: str = None, parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setFixedSize(220, 120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.titleLbl = QLabel(title)
        self.titleLbl.setObjectName("StatTitle")
        self.titleLbl.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.valueLbl = QLabel(format_currency(value))
        self.valueLbl.setObjectName("StatValue")
        self.valueLbl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        if color:
            self.valueLbl.setStyleSheet(f"color: {color};")

        layout.addWidget(self.titleLbl)
        layout.addStretch()
        layout.addWidget(self.valueLbl)

    def updateValue(self, value: float):
        self.valueLbl.setText(format_currency(value))
