from dataclasses import dataclass

@dataclass
class Account:
    id: str
    name: str
    balance: float

    @staticmethod
    def from_dict(data):
        return Account(
            id=data.get("id"),
            name=data.get("name"),
            balance=data.get("balance", 0.0)
        )
