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

    def delete_account(self, account_id: str) -> bool:
        """Deletes an account from the database."""
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

    def get_transactions(self, account_id: str = None, month_str: str = None):
        """Fetches transactions, optionally filtered by account and month (YYYY-MM)."""
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        
        if account_id:
            query += " AND account_id = ?"
            params.append(account_id)
        
        if month_str:
            query += " AND date LIKE ?"
            params.append(f"{month_str}%")
        
        query += " ORDER BY date DESC"
        data = self.db.fetch_all(query, tuple(params))
        from models import Transaction
        return [Transaction.from_dict(row) for row in data]

    def get_monthly_summary(self, month_str: str = None):
        """Calculates Net Worth (current) and Income/Expenses for a specific month (YYYY-MM)."""
        # 1. Net Worth: Current total sum of all account balances (independent of month)
        net_worth_data = self.db.fetch_one("SELECT SUM(balance) as total FROM accounts")
        net_worth = net_worth_data["total"] if net_worth_data and net_worth_data["total"] is not None else 0.0

        # Use current month if none provided
        if not month_str:
            from datetime import datetime
            month_str = datetime.now().strftime("%Y-%m")

        # 2. Monthly Income
        income_query = "SELECT SUM(amount) as total FROM transactions WHERE type = 'Income' AND date LIKE ?"
        income_data = self.db.fetch_one(income_query, (f"{month_str}%",))
        income = income_data["total"] if income_data and income_data["total"] is not None else 0.0

        # 3. Monthly Expenses
        expense_query = "SELECT SUM(amount) as total FROM transactions WHERE type = 'Expense' AND date LIKE ?"
        expense_data = self.db.fetch_one(expense_query, (f"{month_str}%",))
        expense = expense_data["total"] if expense_data and expense_data["total"] is not None else 0.0

        return {
            "net_worth": net_worth,
            "income": income,
            "expenses": expense,
            "net_income": income - expense
        }

    def get_transaction_date_range(self):
        """Returns the first transaction month and the current month."""
        from datetime import datetime
        now = datetime.now()
        
        first = self.db.fetch_one("SELECT MIN(date) as first_date FROM transactions")
        if first and first["first_date"]:
            first_date = datetime.strptime(first["first_date"], "%Y-%m-%d")
        else:
            first_date = now
            
        return first_date, now

    def update_transaction(self, transaction_id: str, data: dict) -> bool:
        """Updates a transaction and corrects account balances."""
        # 1. Get old transaction to revert balance
        old_t = self.db.fetch_one("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        if not old_t:
            return False
        
        old_amount = old_t["amount"]
        old_type = old_t["type"]
        old_account_id = old_t["account_id"]

        # 2. Update Transaction
        success = self.db.execute_query(
            """UPDATE transactions 
               SET account_id = ?, date = ?, amount = ?, category = ?, type = ?, note = ? 
               WHERE id = ?""",
            (data["account_id"], data["date"], data["amount"], 
             data["category"], data["type"], data["note"], transaction_id)
        )

        if success:
            # 3. Correct Balances
            # Revert old
            old_adj = -old_amount if old_type == "Income" else old_amount
            self.db.execute_query("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                (old_adj, old_account_id))
            
            # Apply new
            new_adj = data["amount"] if data["type"] == "Income" else -data["amount"]
            self.db.execute_query("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                (new_adj, data["account_id"]))
            return True
        return False

    def delete_transaction(self, transaction_id: str) -> bool:
        """Deletes a transaction and reverts account balance."""
        old_t = self.db.fetch_one("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        if not old_t: return False

        if self.db.execute_query("DELETE FROM transactions WHERE id = ?", (transaction_id,)):
            adj = -old_t["amount"] if old_t["type"] == "Income" else old_t["amount"]
            self.db.execute_query("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                (adj, old_t["account_id"]))
            return True
        return False

    def get_unique_categories(self):
        """Fetches distinct categories from transactions combined with defaults."""
        defaults = {"Food", "Rent", "Salary", "Entertainment", "Transport", "Shopping", "Utilities", "Health"}
        
        # Get used categories
        data = self.db.fetch_all("SELECT DISTINCT category FROM transactions")
        used = {row["category"] for row in data if row["category"]}
        
        return sorted(list(defaults.union(used)))
