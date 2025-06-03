from finance_manager.db.session import SessionLocal
from finance_manager.db.models import User, Transaction, Budget
from tabulate import tabulate

session = SessionLocal()

def main_menu():
    while True:
        print("\n=== Personal Finance Manager ===")
        print("1. Manage Users")
        print("2. Manage Transactions")
        print("3. Manage Budgets")
        print("4. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            user_menu()
        elif choice == "2":
            transaction_menu()
        elif choice == "3":
            budget_menu()
        elif choice == "4":
            print("Exiting Personal Finance Manager. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


def user_menu():
    while True:
        print("\n--- User Menu ---")
        print("1. Create User")
        print("2. View All Users")
        print("3. Find User by Name")
        print("4. Delete User")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            name = input("Enter user name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            user = User(name=name)
            session.add(user)
            session.commit()
            print(f"User '{name}' created.")
        elif choice == "2":
            users = session.query(User).all()
            if users:
                print(tabulate([[u.id, u.name] for u in users], headers=["ID", "Name"]))
            else:
                print("No users found.")
        elif choice == "3":
            name = input("Enter name to search: ").strip()
            users = session.query(User).filter(User.name.ilike(f"%{name}%")).all()
            if users:
                print(tabulate([[u.id, u.name] for u in users], headers=["ID", "Name"]))
            else:
                print("No matching users.")
        elif choice == "4":
            try:
                user_id = int(input("Enter User ID to delete: "))
                user = session.get(User, user_id)
                if user:
                    session.delete(user)
                    session.commit()
                    print("User deleted.")
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid input. Please enter a numeric ID.")
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def transaction_menu():
    while True:
        print("\n--- Transaction Menu ---")
        print("1. Create Transaction")
        print("2. View All Transactions")
        print("3. View Transactions by User")
        print("4. Delete Transaction")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                user_id = int(input("Enter User ID: "))
                user = session.get(User, user_id)
                if not user:
                    print("User not found.")
                    continue
                amount = float(input("Enter amount: "))
                category = input("Enter category: ").strip()
                t_type = input("Enter type (income/expense): ").strip().lower()
                if t_type not in ["income", "expense"]:
                    print("Invalid type.")
                    continue
                tx = Transaction(amount=amount, category=category, type=t_type, user=user)
                session.add(tx)
                session.commit()
                print("Transaction recorded.")
            except ValueError:
                print("Invalid input. Amount must be a number.")
        elif choice == "2":
            txs = session.query(Transaction).all()
            if txs:
                print(tabulate(
                    [[t.id, t.user_id, t.amount, t.type, t.category, t.date] for t in txs],
                    headers=["ID", "User ID", "Amount", "Type", "Category", "Date"]
                ))
            else:
                print("No transactions found.")
        elif choice == "3":
            try:
                user_id = int(input("Enter User ID: "))
                txs = session.query(Transaction).filter_by(user_id=user_id).all()
                if txs:
                    print(tabulate(
                        [[t.id, t.amount, t.type, t.category, t.date] for t in txs],
                        headers=["ID", "Amount", "Type", "Category", "Date"]
                    ))
                else:
                    print("No transactions for this user.")
            except ValueError:
                print("Invalid input.")
        elif choice == "4":
            try:
                tx_id = int(input("Enter Transaction ID to delete: "))
                tx = session.get(Transaction, tx_id)
                if tx:
                    session.delete(tx)
                    session.commit()
                    print("Transaction deleted.")
                else:
                    print("Transaction not found.")
            except ValueError:
                print("Invalid input.")
        elif choice == "5":
            break
        else:
            print("Invalid option.")


def budget_menu():
    while True:
        print("\n--- Budget Menu ---")
        print("1. Set Budget")
        print("2. View All Budgets")
        print("3. View Budgets by User")
        print("4. Delete Budget")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                user_id = int(input("Enter User ID: "))
                user = session.get(User, user_id)
                if not user:
                    print("User not found.")
                    continue
                category = input("Enter budget category: ").strip()
                limit = float(input("Enter budget limit: "))
                budget = Budget(user=user, category=category, limit_amount=limit)
                session.add(budget)
                session.commit()
                print("Budget set.")
            except ValueError:
                print("Invalid input.")
        elif choice == "2":
            budgets = session.query(Budget).all()
            if budgets:
                print(tabulate(
                    [[b.id, b.user_id, b.category, b.limit_amount] for b in budgets],
                    headers=["ID", "User ID", "Category", "Limit"]
                ))
            else:
                print("No budgets found.")
        elif choice == "3":
            try:
                user_id = int(input("Enter User ID: "))
                budgets = session.query(Budget).filter_by(user_id=user_id).all()
                if budgets:
                    print(tabulate(
                        [[b.id, b.category, b.limit_amount] for b in budgets],
                        headers=["ID", "Category", "Limit"]
                    ))
                else:
                    print("No budgets for this user.")
            except ValueError:
                print("Invalid input.")
        elif choice == "4":
            try:
                b_id = int(input("Enter Budget ID to delete: "))
                budget = session.get(Budget, b_id)
                if budget:
                    session.delete(budget)
                    session.commit()
                    print("Budget deleted.")
                else:
                    print("Budget not found.")
            except ValueError:
                print("Invalid input.")
        elif choice == "5":
            break
        else:
            print("Invalid option.")
