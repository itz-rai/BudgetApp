from PySide2.QtWidgets import (QDialog, QVBoxLayout, QPushButton, 
                               QLineEdit, QLabel, QComboBox, QDateEdit, QMessageBox)
from PySide2.QtCore import QDate, Qt

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None, accounts=None, categories=None, initial_data=None):
        super().__init__(parent)
        self.initial_data = initial_data
        self.setWindowTitle("Edit Transaction" if initial_data else "Add Transaction")
        self.setFixedSize(350, 480)
        # ... styles ...
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
        
        if initial_data:
            idx = self.account_combo.findData(initial_data["account_id"])
            if idx != -1: self.account_combo.setCurrentIndex(idx)
        
        layout.addWidget(self.account_combo)

        # Date
        layout.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        if initial_data:
            self.date_input.setDate(QDate.fromString(initial_data["date"], "yyyy-MM-dd"))
        else:
            self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Amount
        layout.addWidget(QLabel("Amount"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        if initial_data:
            self.amount_input.setText(str(initial_data["amount"]))
        layout.addWidget(self.amount_input)

        # Type (Income/Expense)
        layout.addWidget(QLabel("Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Expense", "Income"])
        if initial_data:
            self.type_combo.setCurrentText(initial_data["type"])
        layout.addWidget(self.type_combo)

        # Category
        layout.addWidget(QLabel("Category"))
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(self.categories)
        if initial_data:
            self.category_input.setCurrentText(initial_data["category"])
        layout.addWidget(self.category_input)

        # Note
        layout.addWidget(QLabel("Note (Optional)"))
        self.note_input = QLineEdit()
        if initial_data:
            self.note_input.setText(initial_data["note"])
        layout.addWidget(self.note_input)

        layout.addStretch()

        # Save Button
        self.save_btn = QPushButton("Update Transaction" if initial_data else "Save Transaction")
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
