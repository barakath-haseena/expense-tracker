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
    date_input = input("Enter expense date (YYYY-MM-DD) or press Enter for today's date: ")

    if not date_input:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = date_input

    expense_id = len(data["expenses"]) + 1

    expense = {
    "id": expense_id,
    "description": description,
    "amount": amount,
    "date": date
    }

    data["expenses"].append(expense)
    save_data(data)

    print(f"Expense added succesfully (ID: {expense_id})")
    input("\nPress Enter to return to the main menu...")


def view_expenses():
    data = load_data()
    if len(data["expenses"]) == 0:
        print("No expenses recorded.")
    else:
        print("Expenses List:")
        for expense in data["expenses"]:
            print(f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']} ")
    input("\nPress Enter to return to the main menu...")

def delete_expense():
    data = load_data()

    try:
        delete_id = int(input("Enter The Expense ID to delete: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return

    org_length = len(data["expenses"])
    data["expenses"] = [exp for exp in data["expenses"] if exp['id'] != delete_id]

    if len(data["expenses"]) < org_length:
        save_data(data)
        print(f"Expense with ID {delete_id} deleted successfully.")
    else:
       print(f"No expense found with the ID {delete_id}.")   

    input("\nPress Enter to return to the main menu")

def update_expense():
    data = load_data()
    try:
        update_id = int(input("Enter the Expense ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")  
        return

    expense_found = False
    for exp in data["expenses"]:
        if exp['id'] == update_id:
            expense_found =  True
            print(f"Current details: Description: {exp['description']}, Amount: {exp['amount']}, Date: {exp['date']}")

            new_description = input("Enter new description (if needed): ")
            new_amount = input("Enter new amount(if needed): ")
            new_date = input("Enter new date(if needed): ")
            
            if new_description:
                exp['description'] = new_description
            if new_amount:
                try:
                    new_amount_value =  float(new_amount)
                    if new_amount_value < 0:
                        print("Amount must be a positive number.")
                    else:
                        exp['amount'] = new_amount_value
                except ValueError:
                    print("Invalid amount input. Keeping the original amount.")
            if new_date:
                while True:
                    try:
                        datetime.strptime(new_date, "%Y-%m-%d")
                        exp['date'] = new_date
                        break
                    except ValueError:
                        print("Invalid date format. Please use YYYY-MM-DD format.")
                        new_date = input("Enter a valid new date or press Enter to keep the old date: ")
                        if not new_date:
                            break

            save_data(data)
            print(f"Expense with ID {update_id} updated successfully.")
            break
    if not expense_found:
        print(f"No expense found with the ID {update_id}.")
    
    input("\nPress Enter to return to the main menu...")

def main():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete expense")
        print("4. Update expense")
        print("5. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            description = input("Enter Expense Description: ")
            while True:
                try:
                    amount = float(input("Enter Expense Amount: "))
                    if amount < 0:
                        print("Amount must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            add_expense(description, amount)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            update_expense() 
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice, please try again.")

if __name__ == "__main__":
    main()










