import os
from controllers import MainController

DB_FILE = "budget.db"

def test_transactions():
    # 1. Initialize
    print("Initializing Controller...")
    controller = MainController()
    
    # 2. Add Account (if not exists)
    acc = controller.add_account("Trans Test Bank", 500.00)
    print(f"Added Account: {acc.name} with balance {acc.balance}")
    
    # 3. Add Expense
    print("Adding Expense of 100.00...")
    success = controller.add_transaction(
        acc.id, "2023-10-27", 100.00, "Food", "Expense", "Lunch"
    )
    assert success, "Failed to add expense"
    
    # 4. Verify Balance Update (500 - 100 = 400)
    updated_acc = controller.get_all_accounts()[-1] # Get last added
    assert updated_acc.id == acc.id
    print(f"New Balance: {updated_acc.balance}")
    assert updated_acc.balance == 400.00, f"Expected 400.0, got {updated_acc.balance}"
    
    # 5. Add Income
    print("Adding Income of 200.00...")
    success = controller.add_transaction(
        acc.id, "2023-10-28", 200.00, "Salary", "Income", "Freelance"
    )
    assert success
    
    # 6. Verify Balance Update (400 + 200 = 600)
    updated_acc = controller.get_all_accounts()[-1]
    assert updated_acc.balance == 600.00, f"Expected 600.0, got {updated_acc.balance}"
    
    # 7. Verify Transaction History
    trans = controller.get_transactions(acc.id)
    assert len(trans) == 2
    print(f"Found {len(trans)} transactions.")
    
    print("Phase 3 Test Successful!")

if __name__ == "__main__":
    try:
        test_transactions()
    except AssertionError as e:
        print(f"Test Failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
