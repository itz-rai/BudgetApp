import sys
import os
from PySide2.QtWidgets import QApplication
from export_engine import PDFExporter
from models_transaction import Transaction

def test_export():
    app = QApplication(sys.argv)
    
    # Mock data
    data = {
        "month": "2026-02",
        "summary": {
            "net_worth": 5000.0,
            "income": 3000.0,
            "expenses": 1200.0,
            "net_income": 1800.0
        },
        "categories": {
            "Food": 400.0,
            "Rent": 800.0
        },
        "transactions": [
            Transaction(id="1", account_id="acc1", date="2026-02-01", amount=3000.0, category="Salary", type="Income", note="Test Income"),
            Transaction(id="2", account_id="acc1", date="2026-02-05", amount=400.0, category="Food", type="Expense", note="Groceries"),
            Transaction(id="3", account_id="acc1", date="2026-02-10", amount=800.0, category="Rent", type="Expense", note="Monthly Rent")
        ]
    }
    
    output_path = "test_report.pdf"
    print(f"Exporting to {output_path}...")
    success = PDFExporter.export_monthly_report(data, output_path)
    
    if success and os.path.exists(output_path):
        print(f"Success! PDF created at {os.path.abspath(output_path)}")
    else:
        print("Failed to create PDF.")

if __name__ == "__main__":
    test_export()
