import uuid
from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtCore import Qt
from ui.ui_home import Ui_homeDialog
from add_account_dialog import AddAccountDialog
from account_card import AccountCard

class HomeScreen(QDialog):
    def __init__(self, parent =None):
        super().__init__(parent)
        self.ui =Ui_homeDialog()
        self.ui.setupUi(self)

        #Spacing between accounts
        self.ui.accHL.setContentsMargins(12,12,12,12)
        self.ui.accHL.setSpacing(12)

        #Scroll Behaviour
        self.ui.accScrollArea.setWidgetResizable(True)
        self.ui.accScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.accScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        btn = self.ui.addAccBtn
        print("addAccBtnExists:",bool(btn))
        btn.clicked.connect(self.open_add_account_dialog)
        btn.clicked.connect(lambda:print("clicked signal fired"))
        btn2 = self.ui.testPushButton
        btn2.clicked.connect(lambda:print("I have been pushed"))



        self._accounts=[] # [{'id', 'name', 'balance', 'card'}]

    def open_add_account_dialog(self):
        dlg = AddAccountDialog(self)
        if dlg.exec_():
            result =dlg.get_result()
            if result:
                name,balance = result
                self._add_account(name,balance)

    def _add_account(self,name: str, balance: float):
        account_id = uuid.uuid4().hex

        parent =self.ui.scrollAreaWidgetContents
        card = AccountCard(account_id,name,balance,parent=parent)
        card.editRequested.connect(self._edit_account)
        card.deleteRequested.connect(self._delete_account)

        self.ui.accHL.addWidget(card)
        self._accounts.append({"id":account_id,"name":name,"balance":balance, "card":card})

    def _edit_account(self,account_id:str):
        acc =self._find_account(account_id)
        if not acc:
            return
        dlg = AddAccountDialog(self,initial_name=acc["name"],initial_amount=acc["balance"])
        if dlg.exec_():
            name, balance =dlg.get_result()
            acc["name"] = name
            acc["balance"] = balance
            acc["card"].updateData(name,balance)
        
    def _delete_account(self, account_id:str):
        acc =self._find_account(account_id)
        if not acc:
            return
        confirm = QMessageBox.question(
            self, "Delete account",
            f"Are you sure you want to delete'{acc['name']}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        
        self.ui.accHL.removeWidget(acc["card"])
        acc["card"].setParent(None)
        acc["card"].deleteLater()

        self._accounts = [a for a in self._accounts if a["id"] != account_id]


    def _find_account(self, account_id: str):
        for a in self._accounts:
            if a["id"] == account_id:
                return a




