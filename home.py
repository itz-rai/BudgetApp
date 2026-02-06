import uuid
from PySide2.QtWidgets import QDialog, QMessageBox, QApplication, QPushButton
from PySide2.QtCore import Qt
from ui.ui_home import Ui_homeDialog
from add_account_dialog import AddAccountDialog
from account_card import AccountCard
from controllers import MainController
from theme_manager import ThemeManager

class HomeScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_homeDialog()
        self.ui.setupUi(self)

        # Spacing between accounts
        self.ui.accHL.setContentsMargins(12, 12, 12, 12)
        self.ui.accHL.setSpacing(12)

        # Scroll Behaviour
        self.ui.accScrollArea.setWidgetResizable(True)
        self.ui.accScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.accScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        btn = self.ui.addAccBtn
        print("addAccBtnExists:", bool(btn))
        btn.clicked.connect(self.open_add_account_dialog)
        btn.clicked.connect(lambda: print("clicked signal fired"))
        
        # Initialize Controller
        self.controller = MainController()

        # Theme Support
        self.theme_manager = ThemeManager(QApplication.instance())
        
        # Add Theme Toggle Button to Sidebar
        self.themeBtn = QPushButton("Switch Theme")
        self.themeBtn.setStyleSheet("background-color: #555; color: white; border-radius: 10px; padding: 10px;")
        self.themeBtn.clicked.connect(self.theme_manager.toggle_theme)
        self.ui.sideMenuVL.addWidget(self.themeBtn)
        self.ui.sideMenuVL.addStretch() # Push everything up
        
        # Load existing accounts
        self._load_accounts()

    def _load_accounts(self):
        """Loads accounts from the database and displays them."""
        # Clear existing widgets from layout if any (optional, for refresh)
        while self.ui.accHL.count():
            item = self.ui.accHL.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        accounts = self.controller.get_all_accounts()
        for acc in accounts:
            self._create_account_card(acc.id, acc.name, acc.balance)

    def _create_account_card(self, account_id, name, balance):
        parent = self.ui.scrollAreaWidgetContents
        card = AccountCard(account_id, name, balance, parent=parent)
        card.editRequested.connect(self._edit_account)
        card.deleteRequested.connect(self._delete_account)
        self.ui.accHL.addWidget(card)

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
                # We need to find the specific card to update it without reloading everything
                for i in range(self.ui.accHL.count()):
                    widget = self.ui.accHL.itemAt(i).widget()
                    if isinstance(widget, AccountCard) and widget.account_id == account_id:
                        widget.updateData(name, balance)
                        break

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
            for i in range(self.ui.accHL.count()):
                widget = self.ui.accHL.itemAt(i).widget()
                if isinstance(widget, AccountCard) and widget.account_id == account_id:
                    self.ui.accHL.removeWidget(widget)
                    widget.setParent(None)
                    widget.deleteLater()
                    break




