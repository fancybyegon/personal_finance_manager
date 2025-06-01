from typing import List
from .models import Transaction

class FinanceManager:
    def __init__(self):
        self.transactions: List[Transaction] = []
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to the manager"""
        self.transactions.append(transaction)
    
    def get_balance(self) -> float:
        """Calculate current balance (income - expenses)"""
        income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return income - expenses
    
    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        """Get all transactions for a specific category"""
        return [t for t in self.transactions if t.category.lower() == category.lower()]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get all transactions of a specific type (income/expense)"""
        return [t for t in self.transactions if t.transaction_type.lower() == transaction_type.lower()]
    
    def get_all_transactions(self) -> List[Transaction]:
        """Get all transactions sorted by date (newest first)"""
        return sorted(self.transactions, key=lambda x: x.date, reverse=True)