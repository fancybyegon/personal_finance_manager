from datetime import datetime
from finance.manager import FinanceManager
from finance.storage import FileStorage
from finance.budget import FinanceManagerWithBudget
from finance.models import Transaction, Budget

class PersonalFinanceApp:
    def __init__(self):
        # Switch between FinanceManager and FinanceManagerWithBudget as needed
        self.manager = FinanceManagerWithBudget()
        self.storage = FileStorage()
        self.load_data()
    
    def load_data(self) -> None:
        """Load transactions from storage"""
        self.manager.transactions = self.storage.load_transactions()
    
    def save_data(self) -> None:
        """Save transactions to storage"""
        self.storage.save_transactions(self.manager.transactions)
    
    def display_menu(self) -> None:
        """Display main menu options"""
        print("\nPersonal Finance Manager")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Current Balance")
        print("5. View Spending by Category")
        print("6. Manage Budgets")
        print("7. Exit")
    
    def run(self) -> None:
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_transaction('income')
            elif choice == '2':
                self.add_transaction('expense')
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                self.view_balance()
            elif choice == '5':
                self.view_spending_by_category()
            elif choice == '6':
                self.manage_budgets()
            elif choice == '7':
                self.save_data()
                print("\nThank you for using Personal Finance Manager!")
                break
            else:
                print("Invalid choice. Please enter a number between 1-7.")
    
    def add_transaction(self, transaction_type: str) -> None:
        """Add a new income or expense transaction"""
        print(f"\nAdd {transaction_type.capitalize()}")
        
        try:
            amount = float(input("Amount: $").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            category = input("Category: ").strip()
            if not category:
                print("Category cannot be empty.")
                return
            
            description = input("Description (optional): ").strip()
            date_input = input("Date (YYYY-MM-DD, leave blank for today): ").strip()
            
            date = datetime.now().date() if not date_input else datetime.strptime(date_input, '%Y-%m-%d').date()
            
            transaction = Transaction(amount, category, date, description, transaction_type)
            self.manager.add_transaction(transaction)
            print(f"\n{transaction_type.capitalize()} added successfully!")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_transactions(self) -> None:
        """Display all transactions"""
        print("\nAll Transactions")
        transactions = self.manager.get_all_transactions()
        
        if not transactions:
            print("No transactions found.")
            return
        
        for i, t in enumerate(transactions, 1):
            print(f"{i}. {t}")
    
    def view_balance(self) -> None:
        """Display current balance"""
        balance = self.manager.get_balance()
        print(f"\nCurrent Balance: ${balance:.2f}")
    
    def view_spending_by_category(self) -> None:
        """Display spending breakdown by category"""
        print("\nSpending by Category")
        expenses = self.manager.get_transactions_by_type('expense')
        
        if not expenses:
            print("No expenses found.")
            return
        
        categories = {}
        for t in expenses:
            categories[t.category] = categories.get(t.category, 0) + t.amount
        
        print("\nCategory\tAmount")
        print("-" * 30)
        for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"{category:<15}${amount:>10.2f}")
    
    def manage_budgets(self) -> None:
        """Budget management submenu"""
        while True:
            print("\nBudget Management")
            print("1. Add Budget")
            print("2. View Budget Status")
            print("3. Back to Main Menu")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.add_budget()
            elif choice == '2':
                self.view_budget_status()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please enter 1-3.")
    
    def add_budget(self) -> None:
        """Add a new budget category"""
        print("\nAdd New Budget")
        
        try:
            category = input("Category: ").strip()
            if not category:
                print("Category cannot be empty.")
                return
            
            limit = float(input("Budget Limit: $").strip())
            if limit <= 0:
                print("Budget limit must be positive.")
                return
            
            self.manager.add_budget(Budget(category, limit))
            print(f"\nBudget for {category} set to ${limit:.2f}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_budget_status(self) -> None:
        """Display current budget status"""
        status = self.manager.get_budget_status()
        
        if not status:
            print("\nNo budgets set up yet.")
            return
        
        print("\nBudget Status")
        print("-" * 60)
        print(f"{'Category':<15} {'Limit':>10} {'Spent':>10} {'Remaining':>12} {'Status':>10}")
        print("-" * 60)
        
        for category, data in status.items():
            status_indicator = "OVER" if data['over_budget'] else "OK"
            print(f"{category:<15} ${data['limit']:>9.2f} ${data['spent']:>9.2f} "
                  f"${data['remaining']:>10.2f} {status_indicator:>10}")

if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()