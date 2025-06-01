import json
from datetime import datetime
from pathlib import Path
from typing import List
from .models import Transaction

class FileStorage:
    def __init__(self, filename: str = 'transactions.json'):
        self.filename = filename
        Path(filename).touch(exist_ok=True)  # Create file if it doesn't exist
    
    def save_transactions(self, transactions: List[Transaction]) -> None:
        """Save transactions to JSON file"""
        data = []
        for t in transactions:
            data.append({
                'amount': t.amount,
                'category': t.category,
                'date': t.date.isoformat(),
                'description': t.description,
                'transaction_type': t.transaction_type
            })
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_transactions(self) -> List[Transaction]:
        """Load transactions from JSON file"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            transactions = []
            for item in data:
                try:
                    transactions.append(Transaction(
                        amount=float(item['amount']),
                        category=item['category'],
                        date=datetime.strptime(item['date'], '%Y-%m-%d').date(),
                        description=item['description'],
                        transaction_type=item['transaction_type']
                    ))
                except (KeyError, ValueError) as e:
                    print(f"Error loading transaction: {e}")
            return transactions
        except (FileNotFoundError, json.JSONDecodeError):
            return []