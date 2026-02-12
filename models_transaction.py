from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    account_id: str
    date: str
    amount: float
    category: str
    type: str # "Income" or "Expense"
    note: str

    @staticmethod
    def from_dict(data):
        return Transaction(
            id=data.get("id"),
            account_id=data.get("account_id"),
            date=data.get("date"),
            amount=data.get("amount", 0.0),
            category=data.get("category", ""),
            type=data.get("type", "Expense"),
            note=data.get("note", "")
        )
