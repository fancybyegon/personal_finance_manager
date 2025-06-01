from typing import Dict, List, Optional
from .models import Budget, Transaction
from .manager import FinanceManager

class FinanceManagerWithBudget(FinanceManager):
    def __init__(self):
        super().__init__()
        self.budgets: List[Budget] = []
    
    def add_budget(self, budget: Budget) -> None:
        """Add a new budget category"""
        self.budgets.append(budget)
    
    def get_budget_status(self) -> Dict[str, Dict[str, float]]:
        """Get spending status for all budget categories"""
        status = {}
        expenses_by_category = {}
        
        # Calculate total expenses per category
        for t in self.get_transactions_by_type('expense'):
            expenses_by_category[t.category] = expenses_by_category.get(t.category, 0) + t.amount
        
        # Compare against budgets
        for budget in self.budgets:
            spent = expenses_by_category.get(budget.category, 0)
            remaining = budget.limit - spent
            percentage = (spent / budget.limit) * 100 if budget.limit > 0 else 0
            
            status[budget.category] = {
                'limit': budget.limit,
                'spent': spent,
                'remaining': remaining,
                'percentage': percentage,
                'over_budget': remaining < 0
            }
        
        return status
    
    def get_budget_for_category(self, category: str) -> Optional[Budget]:
        """Get budget for a specific category if it exists"""
        for budget in self.budgets:
            if budget.category.lower() == category.lower():
                return budget
        return None