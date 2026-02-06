from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QMenu
from PySide2.QtCore import Qt, Signal

def format_currency(amount: float, currency_symbol: str = "TT$") -> str:
    return f"{currency_symbol}{amount:,.2f}"

class AccountCard(QFrame):
    editRequested = Signal(str) #emits account_id
    deleteRequested = Signal(str) #emits account_id

    def __init__(self,account_id:str, name: str, balance: float, parent=None):
        super().__init__(parent)
        self.account_id = account_id

        self.setObjectName("AccountCard")
        self.setMinimumWidth(180)
        self.setMinimumHeight(100)
        self.setStyleSheet("""
            QFrame#AccountCard {
                border: 2px solid #d0d0d0;
                border-radius: 12px;
                background-color: #2f2f2f;
            }
            QLabel#Name {
                color: #ffffff;
                font-weight: 600;
                font-size: 14px;
            }
            QLabel#Balance {
                color: #a0ffa0;
                font-size: 16px;
            }
            QToolButton#MenuBtn {
                color: #cccccc;
                border: none;
                padding: 0px 4px;
            }
            QToolButton#MenuBtn:hover{
                color: #ffffff;
                background: rgba(232,235,247,0.07)
                border-radius:6px;
            }
                           
        """)
        

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(6)

        header = QHBoxLayout()
        header.setContentsMargins(0,0,0,0)

        self.nameLbl = QLabel(name, self)
        self.nameLbl.setObjectName("Name")
        self.nameLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.menuBtn = QToolButton(self)
        self.menuBtn.setObjectName("MenuBtn")
        self.menuBtn.setText("⋮")
        self.menuBtn.setToolTip("Options")
        self.menuBtn.setPopupMode(QToolButton.InstantPopup)

        menu =QMenu(self.menuBtn)
        editAction =menu.addAction("Edit")
        deleteAction = menu.addAction("Delete")
        self.menuBtn.setMenu(menu)

        editAction.triggered.connect(lambda: self.editRequested.emit(self.account_id))
        deleteAction.triggered.connect(lambda: self.deleteRequested.emit(self.account_id))

        header.addWidget(self.nameLbl)
        header.addStretch(1)
        header.addWidget(menu)
        
        

        self.balanceLbl = QLabel(format_currency(balance), self)
        self.balanceLbl.setObjectName("Balance")
        self.balanceLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        root.addLayout(header)
        root.addWidget(self.balanceLbl)

        

    def updateData(self, name:str, balance: float):
        self.nameLbl.setText(name)
        self.balanceLbl.setText(format_currency(balance))