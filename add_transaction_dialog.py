from PySide2.QtWidgets import (QDialog, QVBoxLayout, QPushButton, 
                               QLineEdit, QLabel, QComboBox, QDateEdit, QMessageBox)
from PySide2.QtCore import QDate, Qt

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None, accounts=None, categories=None):
        super().__init__(parent)
        self.setWindowTitle("Add Transaction")
        self.setFixedSize(350, 450)
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; color: white; }
            QLabel { font-size: 14px; margin-top: 8px; }
            QLineEdit, QComboBox, QDateEdit { 
                padding: 8px; font-size: 14px; border-radius: 4px; 
                border: 1px solid #555; background-color: #3b3b3b; color: white;
            }
            QPushButton {
                background-color: #007acc; color: white; padding: 10px;
                border-radius: 6px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #0098ff; }
        """)

        layout = QVBoxLayout(self)
        self.result = None
        self.accounts = accounts or []
        self.categories = categories or ["Food", "Rent", "Salary", "Entertainment", "Transport", "Shopping"]

        # Account Selection
        layout.addWidget(QLabel("Account"))
        self.account_combo = QComboBox()
        for acc in self.accounts:
            self.account_combo.addItem(acc.name, acc.id)
        layout.addWidget(self.account_combo)

        # Date
        layout.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Amount
        layout.addWidget(QLabel("Amount"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        layout.addWidget(self.amount_input)

        # Type (Income/Expense)
        layout.addWidget(QLabel("Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        layout.addWidget(self.type_combo)

        # Category
        layout.addWidget(QLabel("Category"))
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(self.categories)
        layout.addWidget(self.category_input)

        # Note
        layout.addWidget(QLabel("Note (Optional)"))
        self.note_input = QLineEdit()
        layout.addWidget(self.note_input)

        layout.addStretch()

        # Save Button
        self.save_btn = QPushButton("Save Transaction")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.save_btn)

    def save(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
            return

        if self.account_combo.currentIndex() == -1:
            QMessageBox.warning(self, "Error", "Please select an account.")
            return

        self.result = {
            "account_id": self.account_combo.currentData(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "amount": amount,
            "type": self.type_combo.currentText(),
            "category": self.category_input.currentText(),
            "note": self.note_input.text()
        }
        self.accept()

    def get_result(self):
        return self.result
