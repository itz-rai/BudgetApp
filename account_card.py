from PySide2.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QMenu, QWidget
from PySide2.QtCore import Qt, Signal

def format_currency(amount: float, currency_symbol: str = "TT$") -> str:
    return f"{currency_symbol}{amount:,.2f}"

class AccountCard(QFrame):
    editRequested = Signal(str) #emits account_id
    deleteRequested = Signal(str) #emits account_id

    def __init__(self, account_id:str, name: str, balance: float, parent=None):
        super().__init__(parent)
        self.account_id = account_id
        self.name = name
        self.balance = balance
        
        self.setObjectName("AccountCard")
        
        # Initialize UI elements once
        self.nameLbl = QLabel(name, self)
        self.nameLbl.setObjectName("AccountName")
        
        self.balanceLbl = QLabel(format_currency(balance), self)
        self.balanceLbl.setObjectName("AccountBalance")
        
        self.menuBtn = QToolButton(self)
        self.menuBtn.setObjectName("MenuBtn")
        self.menuBtn.setText("⋮")
        self.menuBtn.setToolTip("Options")
        self.menuBtn.setPopupMode(QToolButton.InstantPopup)

        menu = QMenu(self.menuBtn)
        editAction = menu.addAction("Edit")
        deleteAction = menu.addAction("Delete")
        self.menuBtn.setMenu(menu)

        editAction.triggered.connect(lambda: self.editRequested.emit(self.account_id))
        deleteAction.triggered.connect(lambda: self.deleteRequested.emit(self.account_id))

        # Default mode
        self.mode = "grid"
        self.set_view_mode("grid")

    def set_view_mode(self, mode: str):
        self.mode = mode
        
        # Detach persistent widgets from the current layout/parent to prevent deletion
        self.nameLbl.setParent(None)
        self.balanceLbl.setParent(None)
        self.menuBtn.setParent(None)
        
        # Delete the old layout
        if self.layout():
            QWidget().setLayout(self.layout())
            
        # Reparent back to self
        self.nameLbl.setParent(self)
        self.balanceLbl.setParent(self)
        self.menuBtn.setParent(self)
        
        # Ensure they are visible (setParent(None) hides them)
        self.nameLbl.show()
        self.balanceLbl.show()
        self.menuBtn.show()

        if mode == "list":
            layout = QHBoxLayout(self)
            layout.setContentsMargins(15, 10, 15, 10)
            layout.setSpacing(15)
            
            # Reset constraints
            self.setMinimumWidth(0)
            self.setMaximumWidth(16777215)
            self.setMinimumHeight(60)
            self.setMaximumHeight(80)
            self.setFixedSize(16777215, 16777215) # Release fixed size if possible, or just reset min/max
            # QWidget.setFixedSize sets min and max. To unset, we might need to set min/max explicitly.
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
            # Re-apply list specific constraints
            self.setMinimumHeight(60)
            self.setMaximumHeight(80)
            
            # Name
            self.nameLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            layout.addWidget(self.nameLbl)
            
            layout.addStretch()
            
            # Balance
            self.balanceLbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout.addWidget(self.balanceLbl)
            
            # Menu
            layout.addWidget(self.menuBtn)
            
        else: # grid / card
            layout = QVBoxLayout(self)
            layout.setContentsMargins(15, 15, 15, 15)
            layout.setSpacing(10)
            
            # Constraints
            self.setFixedSize(220, 120)
            
            # Header (Name + Menu)
            header = QHBoxLayout()
            self.nameLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            header.addWidget(self.nameLbl)
            header.addStretch()
            header.addWidget(self.menuBtn)
            
            layout.addLayout(header)
            
            layout.addStretch()
            
            # Balance
            self.balanceLbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            layout.addWidget(self.balanceLbl)

    def updateData(self, name:str, balance: float):
        self.name = name
        self.balance = balance
        self.nameLbl.setText(name)
        self.balanceLbl.setText(format_currency(balance))