import os
from controllers import MainController

DB_FILE = "budget.db"

def test_persistence():
    # Remove existing db to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("Removed existing DB.")

    # 1. Initialize Controller (creates DB)
    print("Initializing Controller...")
    controller = MainController()
    
    # 2. Add Account
    print("Adding account 'Test Bank'...")
    acc = controller.add_account("Test Bank", 1000.50)
    print(f"Added: {acc}")
    
    # 3. Verify it's in the list
    accounts = controller.get_all_accounts()
    assert len(accounts) == 1
    assert accounts[0].name == "Test Bank"
    print("Verification 1 passed: Account in memory/DB.")

    # 4. Simulate Restart (New Controller instance)
    print("Simulating App Restart...")
    controller2 = MainController()
    saved_accounts = controller2.get_all_accounts()
    
    # 5. Verify persistence
    assert len(saved_accounts) == 1
    assert saved_accounts[0].name == "Test Bank"
    assert saved_accounts[0].balance == 1000.50
    print("Verification 2 passed: Account persisted after restart.")

    print("Phase 1 Test Successful!")

if __name__ == "__main__":
    try:
        test_persistence()
    except AssertionError as e:
        print(f"Test Failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
