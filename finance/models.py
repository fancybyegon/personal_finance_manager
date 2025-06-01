from datetime import datetime
from typing import Optional

class Transaction:
    def __init__(self, amount: float, category: str, date: datetime.date, 
                 description: str, transaction_type: str):
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.transaction_type = transaction_type  # 'income' or 'expense'
    
    def __str__(self):
        return f"{self.date} - {self.transaction_type}: {self.category} - ${self.amount:.2f} ({self.description})"

class Budget:
    def __init__(self, category: str, limit: float):
        self.category = category
        self.limit = limit
    
    def __str__(self):
        return f"Budget for {self.category}: ${self.limit:.2f}"