import uuid
from database import DatabaseManager
from models import Account

class MainController:
    def __init__(self):
        self.db = DatabaseManager()

    def get_all_accounts(self):
        """Retrieves all accounts from the database."""
        accounts_data = self.db.fetch_all("SELECT * FROM accounts")
        return [Account.from_dict(data) for data in accounts_data]

    def add_account(self, name: str, balance: float) -> Account:
        """Adds a new account to the database."""
        new_id = uuid.uuid4().hex
        if self.db.execute_query(
            "INSERT INTO accounts (id, name, balance) VALUES (?, ?, ?)",
            (new_id, name, balance)
        ):
            return Account(id=new_id, name=name, balance=balance)
        return None

    def update_account(self, account_id: str, name: str, balance: float) -> bool:
        """Updates an existing account's details."""
        return self.db.execute_query(
            "UPDATE accounts SET name = ?, balance = ? WHERE id = ?",
            (name, balance, account_id)
        )

        return self.db.execute_query(
            "DELETE FROM accounts WHERE id = ?",
            (account_id,)
        )

    # --- Transaction Methods ---

    def add_transaction(self, account_id: str, date: str, amount: float, category: str, type: str, note: str) -> bool:
        """Adds a transaction and updates the account balance."""
        new_id = uuid.uuid4().hex
        
        # 1. Add Transaction
        success = self.db.execute_query(
            """INSERT INTO transactions (id, account_id, date, amount, category, type, note) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (new_id, account_id, date, amount, category, type, note)
        )
        
        if success:
            # 2. Update Account Balance
            # Expense subtracts, Income adds
            balance_adjustment = amount if type == "Income" else -amount
            
            # Get current balance
            account = self.db.fetch_one("SELECT balance FROM accounts WHERE id = ?", (account_id,))
            if account:
                new_balance = account["balance"] + balance_adjustment
                self.db.execute_query(
                    "UPDATE accounts SET balance = ? WHERE id = ?", 
                    (new_balance, account_id)
                )
            return True
        return False

    def get_transactions(self, account_id: str = None):
        """Fetches transactions, optionally filtered by account."""
        query = "SELECT * FROM transactions"
        params = ()
        if account_id:
            query += " WHERE account_id = ?"
            params = (account_id,)
        
        query += " ORDER BY date DESC"
        data = self.db.fetch_all(query, params)
        from models import Transaction # Import here to avoid circular dependency if any
        return [Transaction.from_dict(row) for row in data]

    def get_unique_categories(self):
        """Fetches distinct categories from transactions combined with defaults."""
        defaults = {"Food", "Rent", "Salary", "Entertainment", "Transport", "Shopping", "Utilities", "Health"}
        
        # Get used categories
        data = self.db.fetch_all("SELECT DISTINCT category FROM transactions")
        used = {row["category"] for row in data if row["category"]}
        
        return sorted(list(defaults.union(used)))
