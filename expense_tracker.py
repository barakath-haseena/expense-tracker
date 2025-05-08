from datetime import datetime
import json

def load_data():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"expenses":[]}

def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)

def add_expense(description, amount):
    data = load_data()

    expense_id = len(data["expenses"]) + 1
    date = datetime.now().strftime("%Y-%m-%d")

    expense = {
    "id": expense_id,
    "description": description,
    "amount": amount,
    "date": date
    }

    data["expenses"].append(expense)
    save_data(data)

    print(f"Expense added succesfully (ID: {expense_id})")

def view_expenses():
    data = load_data()
    if len(data["expenses"]) == 0:
        print("No expenses recorded.")
    else:
        print("Expenses List:")
        for expense in data["expenses"]:
            print(f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']} ")

def main():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            description = input("Enter Expense Description: ")
            amount = float(input("Enter Expense Amount: "))
            add_expense(description, amount)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice, please try again.")

if __name__ == "__main__":
    main()










