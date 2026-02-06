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
