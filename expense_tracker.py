from datetime import datetime
import json

def load_data():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_id": 0, "expenses":[]}

def save_data(data):
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)


def valid_amount(amt_input):
    try:
        amt_input = float(amt_input)
        if amt_input > 0:
            return amt_input
        else:
            print("Amount must be a positive number.")
            return None
    except ValueError:
        print("Invalid amount. Please try again.")
        return None

def valid_date(date_input):
    try:
        if not date_input:
            return datetime.now().strftime("%Y-%m-%d")   
        else:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
    except ValueError:
        print("Invalid Date Format. Please try again.")
        return None


def add_expense(description, amount, date, category):
    data = load_data()

    existing_ids = [exp["id"] for exp in data["expenses"] if "id" in exp]
    new_id = max(existing_ids, default = 0) + 1

    data["last_id"] = new_id

    new_expense = {
    "id": new_id,
    "description": description,
    "amount": amount,
    "date": date,
    "category": category
    }

    data["expenses"].append(new_expense)
    save_data(data)

    print(f"Expense added successfully (ID: {new_id})")
    input("\nPress Enter to return to the main menu...")

def choose_category():
    categories = ["Home", "Work", "Food", "Entertainment", "Custom"]
    
    print("\nChoose a category: ")
    for i, item  in enumerate(categories, 1):
        print(f"{i}. {item}")

    while True:
        try:
            choice = input("Enter the number of your category choice: ")
            if choice.isdigit() and 1 <= int(choice) <= len(categories):
                choice = int(choice)
                if choice == len(categories):
                    custom_item = input("Enter your custom category: ").strip().title()
                    return custom_item if custom_item else "General"
                else:
                    return categories[choice - 1]
            else:
                print("Invalid choice, please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")

def filter_by_amount(expenses):
    print("\n=== Filter by Amount ===")
    print("1. More than a specific amount")
    print("2. Less than a specific amount")
    print("3. Between two amounts")
    print("4. Return to Main Menu")

    choice = input("Enter your choice: ").strip()
    try:
        choice = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return

    if choice == 1:
        while True:
            amount_input = input("Enter the amount: ").strip()
            try:
                amount_input = float(amount_input)
                break
            except ValueError:
                print("Please enter a valid number.")

        filtered = [exp for exp in expenses if exp["amount"] >= amount_input]
        label = f"Amounts greater than or equal to {amount_input}"

    elif choice == 2:
        while True:
            amount_input = input("Enter the amount: ").strip()
            try:
                amount_input = float(amount_input)
                break
            except ValueError:
                print("Please enter a valid number.")
        
        filtered = [exp for exp in expenses if exp["amount"] <= amount_input]
        label = f"Amounts lesser than or equal to {amount_input}"

    elif choice == 3:
        while True:
            try:
                lower = input("Enter the lower amount: ").strip()
                upper = input("Enter the upper amount: ").strip()
                lower = float(lower)
                upper = float(upper)
                if lower > upper:
                    lower, upper = upper, lower
                filtered = [exp for exp in expenses if lower <= exp["amount"] <= upper]
                label = f"Expenses between {lower} and {upper}"
                break
            except ValueError:
                print("Please enter valid number")

    elif choice == 4:
        return

    else:
        print("Invalid choice.")

    if not filtered:
        print(f"No expenses found under: {label}")
    else:
        print(f"\nExpenses under {label}: ")
        for exp in filtered:
            print(f"ID: {exp['id']}, Description: {exp['description']}, Amount: {exp['amount']}, Date: {exp['date']}")

    input("\nPress Enter to return to the filter menu...")

def filter_expenses():
    data = load_data()

    if not data["expenses"]:
        print("No expenses to filter.")
        input("\nPress Enter to return to the main menu...")
        return

    while True:
        print("\n=== Filter Expenses ===")
        print("1. By Category")
        print("2. By Date (YYYY-MM-DD)")
        print("3. By Month and Year")
        print("4. By Amount")
        print("5. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        filtered =[]

        if choice == "1":
            unique_categories = sorted(set(exp.get("category", "General") for exp in data["expenses"]))
            
            print("\nAvailable Categories: ")
            for i, cat in enumerate(unique_categories, 1):
                print(f"{i}. {cat}")
            while True: 
                try:
                    selected = int(input("Choose a category number: "))
                    if 1 <= selected <= len(unique_categories):
                        selected_category = unique_categories[selected - 1]
                        filtered = [exp for exp in data["expenses"] if exp.get("category", "General") ==  selected_category]
                        label = f"category '{selected_category}'"
                        break
                    else:
                        print("Invalid category choice.")
                except ValueError:
                    print("Please enter a valid number.")
            break

        elif choice == "2":
            while True:
                date = input("Enter the date (YYYY-MM-DD): ").strip()
                valid = valid_date(date)
                if valid:
                    filtered = [exp for exp in data["expenses"] if exp.get("date") == valid]
                    label = f"date '{valid}'"
                    break
            break

        elif choice == "3":
            while True:
                month_year = input("Enter month and year (YYYY-MM): ").strip()
                try:
                    datetime.strptime(month_year, "%Y-%m")
                    break
                except ValueError:
                    print("Invalid format. Please enter in YYYY-MM format.")
            filtered = [exp for exp in data["expenses"] if exp.get("date", "").startswith(month_year)]
            label = f"month-year '{month_year}'"
            break
        
        elif choice == "4":
            filter_by_amount(data["expenses"])
            return

        elif choice == "5":
            return

        else:
            print("Invalid choice.")
            continue

    if not filtered:
        print(f"No expenses found under: {label}")
    else:
        print(f"\nExpenses under {label}:")
        for exp in filtered:
            print(f"ID: {exp['id']}, Description: {exp['description']}, Amount: {exp['amount']}, Date: {exp['date']}")

    input("\nPress Enter to return to the main menu...")

def view_expenses():
    data = load_data()
    if len(data["expenses"]) == 0:
        print("No expenses recorded.")
    else:
        print("Expenses List:")
        for expense in data["expenses"]:
            print(f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}, Category: {expense.get('category', 'General')} ")
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

    input("\nPress Enter to return to the main menu...")

def update_expense():
    data = load_data()
    try:
        update_id = int(input("Enter the Expense ID to update: "))
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")  
        return


    for exp in data["expenses"]:
        if exp['id'] == update_id:
            print(f"Current details: Description: {exp['description']}, Amount: {exp['amount']}, Date: {exp['date']}, Category: {exp.get('category', 'None')}")

            new_description = input("Enter new description (if needed): ")            
            if new_description:
                exp['description'] = new_description

            new_category = input("Enter new category (if needed): ").strip().title()
            if new_category:
                exp['category'] = new_category

            while True:
                new_amount = input("Enter new amount(if needed): ")
                if new_amount:
                    new_amount = valid_amount(new_amount)
                    if new_amount is not None:
                        exp['amount'] = new_amount
                        break
                else:
                    break

            while True:
                new_date = input("Enter new date(if needed): ")
                if new_date:
                    new_date = valid_date(new_date)
                    if new_date:
                        exp['date'] = new_date
                        break
                else:
                    break

            save_data(data)
            print(f"Expense with ID {update_id} updated successfully.")
            break
    else:
        print(f"No expense found with the ID {update_id}.")
    
    input("\nPress Enter to return to the main menu...")

def main():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete expense")
        print("4. Update expense")
        print("5. Filter Expenses")
        print("6. Exit")

        choice = input("Enter Your Choice: ")

        if choice == "1":
            while True:
                description = input("Enter Expense Description: ").strip()   
                if description:
                    break
                else:
                    print("Description cannot be empty.")
            

            while True:
                amount = input("Enter Expense Amount: ")
                amount = valid_amount(amount)
                if amount is not None:
                    break

            while True:
                date = input("Enter expense date (YYYY-MM-DD) or press Enter for today's date: ")
                date = valid_date(date)
                if date:
                    break

            category = choose_category()

            add_expense(description, amount, date, category)

        elif choice == "2":
            view_expenses()    
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            update_expense()
        elif choice == "5":
            filter_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice, please try again.")

if __name__ == "__main__":
    main()
    