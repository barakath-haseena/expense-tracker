from datetime import datetime
import json
import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import customtkinter as ctk
from tkinter import messagebox


def load_data():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r", encoding='utf-8') as file:
            try:
                return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                return {"expenses":[]}
    return {"expenses":[]}

def save_data(data): 
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)

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
        print("4. Return to Main Menu")

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
    expenses = data.get("expenses", [])

    if not expenses:
        messagebox.showinfo("No Data", "No expenses to display.")
        return

    view_window = ctk.CTkToplevel()
    view_window.title("All Expenses")
    view_window.geometry("700x500")

    scroll_frame = ctk.CTkScrollableFrame(view_window, width=680, height=450)
    scroll_frame.pack(pady=10)

    headers = ["ID", "Date", "Category", "Amount", "Description"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=5, pady=5)

    for row, exp in enumerate(expenses, start=1):
        ctk.CTkLabel(scroll_frame, text=str(exp["id"])).grid(row=row, column=0, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["date"]).grid(row=row, column=1, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["category"]).grid(row=row, column=2, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=f"₹{exp['amount']}").grid(row=row, column=3, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["description"]).grid(row=row, column=4, padx=5, pady=2)
        delete_btn = ctk.CTkButton(
            scroll_frame,
            text="🗑️",
            width=30,
            fg_color="transparent",
            text_color="red",
            command=lambda exid=exp["id"]: delete_expense_by_id(exid, view_window)
        )
        delete_btn.grid(row=row, column=5, padx=5)
    
    def delete_expense_by_id(exp_id, window):
        data = load_data()
        updated = [e for e in data["expenses"] if e["id"] != exp_id]

        data["expenses"] = updated
        save_data(data)
        messagebox.showinfo("Deleted", f"Expense with ID {exp_id} deleted.")
        window.destroy()
        view_expenses()


    text_widget.configure(state="disabled")

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

def summarize_expenses():
    data = load_data()
    expenses = data["expenses"] 

    if not expenses:
        print("No expenses recorded.")
        return

    print("\n=== Summarize Menu ===")
    print("1. By Category")
    print("2. By Month")
    print("3. By Year")
    print("4. By Month and Year")
    print("5. By Category and Year")
    print("6. Total Expenses Summary")

    choice = input("Enter your choice number: ")

    if choice == "1":
        category = input("Enter the category to summarize: ").strip()
        filtered = [exp for exp in data["expenses"] if exp.get("category", "General").lower() == category.lower()]

        if not filtered:
            print(f"No expenses found for category: {category}")
        else:
            total = sum(exp["amount"] for exp in filtered)
            print(f"\nSummary for Category: {category}")
            print(f"Total Expenses: ₹{total}")
            print(f"Number of Records: {len(filtered)}")
            for exp in filtered:
                print(f"  ID: {exp['id']} | ₹{exp['amount']} | {exp['date']} | {exp['description']}")

    elif choice == "2":
        while True:
            month_input = input("Enter the Month Number(e.g. 01 for January, 12 for December): ").strip()

            if not month_input.isdigit() or not (1 <= int(month_input)<= 12):
                print("Invalid month input. Please enter a valid number (01 to 12).")
                continue

            month_input = month_input.zfill(2)
            filtered = [exp for exp in expenses if exp.get("date","")[5:7] == month_input]

            if not filtered:
                print(f"No expenses recorded in month: {month_input} ")
                return
            else:
                total = sum(exp["amount"] for exp in filtered)
                print(f"Total expenses in month {month_input}: {total}")
                return

    elif choice == "3":
        while True:
            year_input = input("Enter the Year: ").strip()

            if not year_input.isdigit() or len(year_input) != 4:
                print("Invalid year format. Please enter a 4-digit year.")
                continue

            filtered = [exp for exp in expenses if exp.get("date", "")[:4] == year_input]

            if not filtered:
                print(f"No expenses recorded in year: {year_input}")
            else:
                total = sum(exp["amount"] for exp in filtered)
                print(f"Total expenses in year {year_input}: {total}")
                return

    elif choice == "4":
        while True:
            year_input = input("Enter a year (e.g., 2024): ").strip()
            month_input = input("Enter a month number (e.g., 01 for January): ").strip()

            if (not year_input.isdigit() or len(year_input) != 4) and (not month_input.isdigit() or not (1 <= int(month_input) <= 12)):
                print("Invalid year and month.")
                continue
            if not year_input.isdigit() or len(year_input) != 4:
                print("Invalid format. Please enter a 4-digit year.")
                continue
            if not month_input.isdigit() or not (1 <= int(month_input) <= 12):
                print("Invalid month. Please enter a number from 01 to 12.")
                continue
            month_input = month_input.zfill(2)
            filtered = [exp for exp in expenses if exp.get("date", "")[:4] == year_input and exp.get("date", "")[5:7] ==  month_input]

            if not filtered:
                print(f"No expenses found for {month_input}/{year_input}.")
                return
            else:
                total = sum(exp["amount"] for exp in filtered)
                print(f"Total expenses in {month_input}/{year_input}: {total}")
                return

    elif choice == "5":
        while True:
            all_categories = {exp.get("category", "General").lower() for exp in expenses}

            print("Available Categories: ")
            for cat in sorted(all_categories):
                print(f" - {cat}")

            category_input = input("Enter a category: ").strip()
            
            if category_input.lower() not in all_categories:
                print(f"No '{category_input}'' category exists.")
                continue

            year_input = input("Enter a year (e.g., 2024): ").strip()

            if not year_input.isdigit() or len(year_input) != 4:
                print("Invalid year. Please enter a 4-digit number such 2024.")
                continue

            filtered = [exp for exp in expenses if exp.get("category", "General").lower() == category_input and exp.get("date", "")[:4] == year_input]

            if not filtered:
                print(f"No expenses found under Category '{category_input}' - Year{year_input}.")
            else:
                total = sum(exp["amount"] for exp in filtered)
                print(f"Total expenses in category '{category_input}' for year {year_input}: {total}")
                return

    elif choice == "6":
        total_count = len(expenses)
        total_amount = sum(exp["amount"] for exp in expenses)
        average = total_amount / total_count

        print("\nExpense Summary: ")       
        print(f"Total number of expenses: {total_count}")
        print(f"Total number spent: ₹{total_amount:.2f}")
        print(f"Average expense amount: ₹{average:.2f}")
    
    input("\nPress Enter to return to the main menu...")

def search_by_keyword():
    data = load_data()
    keyword = input("Enter a keyword: ").strip().lower()

    matching_expenses = []
    for expense in data["expenses"]:
        if keyword in expense["description"].lower():
            matching_expenses.append(expense)

    if not matching_expenses:
        print("No matching expenses found.")
    else:
        print("\nMatching Expenses:")
        for expense in matching_expenses:
            print(f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}, Category: {expense.get('category', 'General')}")

    input("\nPress Enter to return to the main menu...")

def export_expenses_csv():
    expenses = load_data().get("expenses", [])    
    if not expenses:
        print("No expenses to export.")
        return

    filename = input("Enter filename to save as (e.g., expenses.csv): ").strip()
    if not filename:
        filename = f"expenses_{datetime.now().strftime('%Y%m%d')}.csv"
    elif not filename.endswith(".csv"):
        filename += ".csv"

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "description", "amount", "date", "category"])
            writer.writeheader()
            writer.writerows(expenses)
        print(f"Expenses exported successfully to {filename}")
    except Exception as e:
        print("An error occurred while exporting:", e)

def visualize_monthlysum():
    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        print("No expenses to visualize.")
        return
    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (01-12): ").strip().zfill(2)

    filtered = [exp for exp in expenses if exp.get("date", "").startswith(f"{year}-{month}")]

    if not filtered:
        print(f"No expenses for {month}/{year}.")
        return

    category_totals = defaultdict(float)
    for exp in filtered:
        category = exp.get("category", "General")
        category_totals[category] += exp['amount']

    labels = list(category_totals.keys())
    values = list(category_totals.values())


    def make_label(pct, allvals):
        total = sum(allvals)
        absolute = int(round(pct/100.*total))
        return f"{pct: .2f}%\n(₹{absolute})"

    colors = plt.cm.Paired.colors
    plt.figure(figsize=(8,8))
    
    wedges, texts, autotexts = plt.pie(
        values, labels=None, autopct= lambda pct: make_label(pct, values),
        startangle=90, colors=colors, textprops=dict(color="black")
        )
    plt.legend(wedges, labels, title="Categories", loc="best")
    
    plt.title(f"Expense Distribution - {month}/{year}")
    plt.tight_layout()
    plt.axis('equal')
    plt.show()


    add_expense(description, amount, date, category)
    result_label.configure(text="Expense added successfully!", text_color="green")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("600x900")

form_frame = ctk.CTkFrame(app)
form_frame.pack(pady=30)

ctk.CTkLabel(form_frame, text="Add New Expense", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)

ctk.CTkLabel(form_frame, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
desc_entry = ctk.CTkEntry(form_frame, width=300)
desc_entry.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
amt_entry = ctk.CTkEntry(form_frame, width=300)
amt_entry.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
date_entry = ctk.CTkEntry(form_frame, width=300)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
date_entry.grid(row=3, column=1, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Category:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
category_option = ctk.CTkOptionMenu(form_frame, values=["Home", "Work", "Food", "Entertainment", "Other"])
category_option.grid(row=4, column=1, padx=10, pady=5)



def submit_expense():
    description = desc_entry.get()
    amount = amt_entry.get()
    date = date_entry.get()
    category = category_option.get()

    if not description or not amount:
        result_label.configure(text="Description and Amount are required!", text_color="red")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            result_label.configure(text="Amount must be a positive number!", text_color="red")
            return
    except ValueError:
        result_label.configure(text="Amount must be a number!", text_color="red")
        return

    add_expense(description, amount, date, category)
    result_label.configure(text="Expense added successfully!", text_color="green")

    desc_entry.delete(0, 'end')
    amt_entry.delete(0, 'end')

result_label = ctk.CTkLabel(form_frame, text="")
result_label.grid(row=6, column=0, columnspan=2)

button_frame = ctk.CTkFrame(form_frame)
button_frame.grid(row=7, column=0, columnspan=2, pady=10)

submit_btn = ctk.CTkButton(button_frame, text="Add Expense", command=submit_expense)
submit_btn.pack(side="left", padx=10)

view_btn = ctk.CTkButton(button_frame, text="View Expenses", command=view_expenses)
view_btn.pack(side="left", padx=10)

app.mainloop()


def main():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete expense")
        print("4. Update expense")
        print("5. Filter Expenses")
        print("6. Search Expenses by Keyword in Description")
        print("7. Summarize Expenses")
        print("8. Export to CSV")
        print("9. Visualize Monthly Summary")
        print("10. Exit")

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
            search_by_keyword()
        elif choice == "7":
            summarize_expenses()
        elif choice == "8":
            export_expenses_csv()
        elif choice == "9":
            visualize_monthlysum()
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid Choice, please try again.")

if __name__ == "__main__":
    main()
    