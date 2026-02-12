import uuid
from PySide2.QtWidgets import (QDialog, QMessageBox, QApplication, QPushButton, 
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame,
                               QStackedWidget)
from PySide2.QtCore import Qt
from add_account_dialog import AddAccountDialog
from add_transaction_dialog import AddTransactionDialog
from account_card import AccountCard
from controllers import MainController
from theme_manager import ThemeManager

class HomeScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar Setup
        self.setup_sidebar()
        main_layout.addWidget(self.sidebarContainer)

        # 2. Content Area Setup
        self.contentArea = QStackedWidget()
        main_layout.addWidget(self.contentArea)

        # 3. Dashboard View (Home)
        self.setup_dashboard_view()
        self.contentArea.addWidget(self.dashboardWidget)

        # 4. Transactions View
        self.setup_transactions_view()
        self.contentArea.addWidget(self.transWidget)
        
        # Initialize Controller
        self.controller = MainController()

        # Load Data
        self._load_accounts()

    def setup_sidebar(self):
        self.sidebarContainer = QFrame()
        self.sidebarContainer.setObjectName("Sidebar")
        self.sidebarContainer.setFixedWidth(250)
        self.sidebarContainer.setStyleSheet("#Sidebar { background-color: #181825; border-right: 1px solid #2f2f3e; }")
        
        layout = QVBoxLayout(self.sidebarContainer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # App Title / Logo Area
        title_lbl = QLabel("Budget App")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #cdd6f4; padding: 20px 0;")
        layout.addWidget(title_lbl)

        # Navigation Buttons
        self.nav_btns = []
        self.add_nav_btn(layout, "Dashboard", lambda: self.switch_view(0))
        self.add_nav_btn(layout, "Transactions", lambda: self.switch_view(1))
        self.add_nav_btn(layout, "Calendar", lambda: print("Calendar Clicked")) # Placeholder

        layout.addStretch()

        # Theme Support
        self.theme_manager = ThemeManager(QApplication.instance())
        self.themeBtn = QPushButton("Switch Theme")
        self.themeBtn.setObjectName("NavButton")
        self.themeBtn.clicked.connect(self.theme_manager.toggle_theme)
        layout.addWidget(self.themeBtn)
        
        # Margin at bottom
        layout.addSpacing(20)

    def add_nav_btn(self, layout, text, callback):
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        if not self.nav_btns: # First one is active
            btn.setChecked(True)
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        self.nav_btns.append(btn)

    def setup_dashboard_view(self):
        self.dashboardWidget = QWidget()
        layout = QVBoxLayout(self.dashboardWidget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(header)

        # Actions Row
        actions_layout = QHBoxLayout()
        
        self.addAccBtn = QPushButton("+ Add Account")
        self.addAccBtn.setObjectName("ActionBtn")
        self.addAccBtn.clicked.connect(self.open_add_account_dialog)
        actions_layout.addWidget(self.addAccBtn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Accounts Grid (Scroll Area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.accScrollWidget = QWidget()
        self.accFlowLayout = QHBoxLayout(self.accScrollWidget) # Simple horizontal for now, or FlowLayout if needed
        self.accFlowLayout.setAlignment(Qt.AlignLeft)
        self.accFlowLayout.setSpacing(20)
        scroll.setWidget(self.accScrollWidget)
        
        layout.addWidget(scroll)

    def setup_transactions_view(self):
        self.transWidget = QWidget()
        layout = QVBoxLayout(self.transWidget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header Row
        header_layout = QHBoxLayout()
        title = QLabel("Transactions")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.addTransBtn = QPushButton("+ Add Transaction")
        self.addTransBtn.setObjectName("ActionBtn")
        self.addTransBtn.clicked.connect(self.open_add_transaction_dialog)
        header_layout.addWidget(self.addTransBtn)
        
        layout.addLayout(header_layout)

        # Transaction List (Scroll Area)
        self.transList = QScrollArea()
        self.transList.setWidgetResizable(True)
        self.transList.setFrameShape(QFrame.NoFrame)
        self.transListContent = QWidget()
        self.transListLayout = QVBoxLayout(self.transListContent)
        self.transListLayout.setAlignment(Qt.AlignTop)
        self.transListLayout.setSpacing(10)
        self.transList.setWidget(self.transListContent)
        
        layout.addWidget(self.transList)

    def switch_view(self, index):
        self.contentArea.setCurrentIndex(index)
        if index == 1: # Transactions
            self._load_transactions()
        
        # Update Nav State
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)

    def _load_transactions(self):
        # Clear existing
        while self.transListLayout.count():
            item = self.transListLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        transactions = self.controller.get_transactions()
        
        for t in transactions:
            row = QFrame()
            row.setObjectName("TransactionRow")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(15, 10, 15, 10)
            
            # Date
            date_lbl = QLabel(t.date)
            date_lbl.setFixedWidth(100)
            
            # Category & Note
            details_layout = QVBoxLayout()
            cat_lbl = QLabel(t.category)
            cat_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")
            note_lbl = QLabel(t.note)
            note_lbl.setStyleSheet("color: #a6adc8; font-size: 12px;")
            details_layout.addWidget(cat_lbl)
            details_layout.addWidget(note_lbl)
            
            # Amount
            amount_str = f"+${t.amount:,.2f}" if t.type == "Income" else f"-${t.amount:,.2f}"
            color = "#a6e3a1" if t.type == "Income" else "#f38ba8" 
            amount_lbl = QLabel(amount_str)
            amount_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            amount_lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")
            
            row_layout.addWidget(date_lbl)
            row_layout.addLayout(details_layout)
            row_layout.addStretch()
            row_layout.addWidget(amount_lbl)
            
            self.transListLayout.addWidget(row)

    def _load_accounts(self):
        """Loads accounts from the database and displays them."""
        # Clear existing
        while self.accFlowLayout.count():
            item = self.accFlowLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        accounts = self.controller.get_all_accounts()
        for acc in accounts:
            self._create_account_card(acc.id, acc.name, acc.balance)

    def _create_account_card(self, account_id, name, balance):
        # We need to make sure AccountCard can fit in the layout
        # Assuming AccountCard is a custom widget
        card = AccountCard(account_id, name, balance)
        # card.setFixedSize(200, 150) # Optional: enforce size
        card.editRequested.connect(self._edit_account)
        card.deleteRequested.connect(self._delete_account)
        self.accFlowLayout.addWidget(card)

    # REMOVED OLD METHODS TO AVOID CONFLICTS
    # show_home_view, show_transactions_view, existing __init__ logic...








    def open_add_account_dialog(self):
        dlg = AddAccountDialog(self)
        if dlg.exec_():
            result = dlg.get_result()
            if result:
                name, balance = result
                self._add_account(name, balance)

    def _add_account(self, name: str, balance: float):
        # Use controller to add to DB
        new_acc = self.controller.add_account(name, balance)
        if new_acc:
            self._create_account_card(new_acc.id, new_acc.name, new_acc.balance)

    def _edit_account(self, account_id: str):
        
        all_accs = self.controller.get_all_accounts()
        acc = next((a for a in all_accs if a.id == account_id), None)
        
        if not acc:
            return

        dlg = AddAccountDialog(self, initial_name=acc.name, initial_amount=acc.balance)
        if dlg.exec_():
            name, balance = dlg.get_result()
            if self.controller.update_account(account_id, name, balance):
                # Update UI
                for i in range(self.accFlowLayout.count()):
                    item = self.accFlowLayout.itemAt(i)
                    if not item: continue
                    widget = item.widget()
                    if isinstance(widget, AccountCard) and widget.account_id == account_id:
                        widget.updateData(name, balance)
                        break

    def open_add_transaction_dialog(self):
        # Pass all accounts to the dialog
        accounts = self.controller.get_all_accounts()
        if not accounts:
            QMessageBox.warning(self, "No Accounts", "Please add an account first.")
            return

        # Fetch Categories
        categories = self.controller.get_unique_categories()

        dlg = AddTransactionDialog(self, accounts=accounts, categories=categories)
        if dlg.exec_():
            data = dlg.get_result()
            if data:
                if self.controller.add_transaction(
                    data["account_id"], 
                    data["date"], 
                    data["amount"], 
                    data["category"], 
                    data["type"], 
                    data["note"]
                ):
                    # Refresh viewing
                    self._load_accounts()
                    self._load_transactions()
                    QMessageBox.information(self, "Success", "Transaction added successfully!")
                else:
                    QMessageBox.critical(self, "Error", "Failed to add transaction.")

    def _delete_account(self, account_id: str):
        confirm = QMessageBox.question(
            self, "Delete account",
            "Are you sure you want to delete this account?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        if self.controller.delete_account(account_id):
            # Remove from UI
            for i in range(self.accFlowLayout.count()):
                item = self.accFlowLayout.itemAt(i)
                if not item: continue
                widget = item.widget()
                if isinstance(widget, AccountCard) and widget.account_id == account_id:
                    self.accFlowLayout.removeWidget(widget)
                    widget.setParent(None)
                    widget.deleteLater()
                    break




