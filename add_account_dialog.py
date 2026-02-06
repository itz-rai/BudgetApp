from PySide2.QtWidgets import QDialog, QMessageBox
from PySide2.QtGui import QDoubleValidator
from ui.ui_addAccountDialog import Ui_createAccountDialog


class AddAccountDialog(QDialog):
    def __init__(self,parent=None,initial_name: str = "",initial_amount:float = None ):
        super().__init__(parent)
        self.ui = Ui_createAccountDialog()
        self.ui.setupUi(self)

        amount_validator = QDoubleValidator(0.0,10_000_000.0,2,self)
        amount_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.accBalanceLe.setValidator(amount_validator)

        #confirm or cancel buttons

        self.ui.addNewAccBtn.clicked.connect(self._try_accept)
        self.ui.closeAddAccountDialogBtn.clicked.connect(self.reject)


        self.setWindowTitle("Edit Account" if initial_name else "Add Account")

        if initial_name:
            self.ui.accNameLe.setText(initial_name)
        if initial_amount is not None:
            self.ui.accBalanceLe.setText(f"{initial_amount:.2f}")

        #Holds the result tuple(name,account) after accept
        self._result = None

    def _try_accept(self):
        name = self.ui.accNameLe.text().strip()
        amount_text = self.ui.accBalanceLe.text().strip()


        if not name:
            QMessageBox.warning(self,"Missing name","Please enter a valid number.")
            return
        

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self,"Invalid amount","Please enter a valid number.")
            return
        if amount < 0:
            QMessageBox.warning(self,"Invalid amount","Amount cannot be negative.")
            return
        
        self._result =(name,amount)
        self.accept()


    def get_result(self):
        return getattr(self,"_result",None)


