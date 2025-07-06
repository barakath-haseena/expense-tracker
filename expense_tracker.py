from datetime import datetime
import json
import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar


# ------------------- Data Handling -------------------
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

# ------------------- Expense Logic -------------------
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

# ------------------- Validation -------------------
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

# ------------------- Choose Category -------------------
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

# ------------------- Filtering -------------------
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

# ------------------- View GUI/Summarize -------------------
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
         
def delete_expense_by_id(exp_id, window):
    data = load_data()
    updated = [e for e in data["expenses"] if e["id"] != exp_id]

    data["expenses"] = updated
    save_data(data)
    messagebox.showinfo("Deleted", f"Expense with ID {exp_id} deleted.")
    window.destroy()

    if window.title() == "All Expenses":
        view_expenses()
    elif window.title() == "Modify Expenses":
        modify_expense_gui()

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
                total = sum(float(exp.get("amount", 0)) for exp in filtered)
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

# ------------------- Searching -------------------
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

# ------------------- Exporting -------------------
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

# ------------------- Visuals -------------------
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

    colors = [
        "#8B4513",
        "#C1B18B",
        "#800020",
        "#0A1172",
        "#556B2F",
        "#DAA520",
        "#4B0082",
        "#5D3A00",
    ]
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

# ------------------- GUI Functions-------------------
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

def open_search_window():
    search_window = ctk.CTkToplevel()
    search_window.title("Search Expenses")
    search_window.geometry("700X600")

    ctk.CTkLabel(search_window, text="Enter keyword to search in description:").pack(pady=10)
    keyword_entry = ctk.CTkEntry(search_window, width=300)
    keyword_entry.pack(pady=5)

    result_box = ctk.CTkTextbox(search_window, width=480, height=280)
    result_box.pack(pady=10)


    def perform_search():
        keyword = keyword_entry.get().strip().lower()
        result_box.configure(state="normal")
        result_box.delete("1.0", "end")

        if not keyword:
            result_box.insert("end", "Please enter a keyword to search.\n")
        else:
            data = load_data()
            matches = [exp for exp in data["expenses"] if keyword in exp["description"].lower()]

            if not matches:
                result_box.insert("end", "No matching expenses found.\n")
            else:
                for exp in matches:
                    line = f"ID: {exp['id']} | {exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['description']}\n"
                    result_box.insert("end", line)

        result_box.configure(state="disabled")
    
    search_button = ctk.CTkButton(search_window, text="Search", command=perform_search)
    search_button.pack()    

def export_to_csv_gui():
    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        messagebox.showinfo("No Data", "No expenses to export.")
        return

    try:
        with open("expenses_export.csv", "w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "description", "amount", "date", "category"])
            writer.writeheader()
            writer.writerows(expenses)

        messagebox.showinfo("Success", "Expenses exported to 'expenses_export.csv'.")
    except Exception as e:
        messagebox.showerror("Error", f"Export failed: {e}")    

def open_summary_window():
    summary_window = ctk.CTkToplevel()
    summary_window.title("Visualize Monthly Summary")
    summary_window.geometry("400x250")

    ctk.CTkLabel(summary_window, text="Enter Year (YYYY):").pack(pady=5)
    year_entry = ctk.CTkEntry(summary_window, width=200)
    year_entry.pack()

    ctk.CTkLabel(summary_window, text="Enter Month (1-12):").pack(pady=5)
    month_entry = ctk.CTkEntry(summary_window, width=200)
    month_entry.pack()

    def show_chart():
        year = year_entry.get().strip()
        month = month_entry.get().strip().zfill(2)

        data = load_data()
        expenses = data.get("expenses", [])
        filtered = [exp for exp in expenses if exp.get("date", "").startswith(f"{year}-{month}")]
        
        if not filtered:
            messagebox.showinfo("No Data", f"No expenses found for {year}-{month}.")
            return   

        category_totals = defaultdict(float)
        
        for exp in filtered:
            category = exp.get("category", "General")
            category_totals[category] += float(exp["amount"])

        labels = list(category_totals.keys())
        values = list(category_totals.values())

        def make_label(pct, allvals):
            total = sum(allvals)
            absolute = int(round(pct/100.*total))
            return f"{pct: .2f}%\n(₹{absolute})"

        colors = [
            "#8B4513",
            "#C1B18B",
            "#800020",
            "#0A1172",
            "#556B2F",
            "#DAA520",
            "#4B0082",
            "#5D3A00",
        ]
        plt.figure(figsize=(8, 8))
        wedges, texts, autotexts = plt.pie(
            values, labels=None,
            autopct=lambda pct: make_label(pct, values),
            startangle=90, colors=colors,
            textprops=dict(color="black")
        )
        plt.legend(wedges, labels, title="Categories", loc="best")
        plt.title(f"Expenses - {month}/{year}")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    ctk.CTkButton(summary_window, text="Show Chart", command=show_chart).pack(pady=15)

def open_update_popup(expense, parent_window):
    popup = ctk.CTkToplevel()
    popup.title("Update Expense")
    popup.geometry("450x450")

    calendar_widget = [None]

    def toggle_calendar():
        if calendar_widget[0]:
            calendar_widget[0].destroy()
            calendar_widget[0] = None
        else:
            cal = Calendar(content_frame, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False)
            cal.grid(row=4, column=1, columnspan=2, pady=(5, 10))
            calendar_widget[0] = cal

            def on_select(event=None):
                selected_date = cal.get_date()
                date_entry.delete(0, "end")
                date_entry.insert(0, selected_date)
                cal.destroy()
                calendar_widget[0] = None

            cal.bind("<<CalendarSelected>>", on_select)

    # Frame to center everything inside popup
    content_frame = ctk.CTkFrame(popup)
    content_frame.pack(pady=30)

    # --- Title ---
    title_label = ctk.CTkLabel(content_frame, text="Update Expense", font=ctk.CTkFont(size=18, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # --- Description ---
    ctk.CTkLabel(content_frame, text="Description:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    desc_entry = ctk.CTkEntry(content_frame, width=250)
    desc_entry.insert(0, expense["description"])
    desc_entry.grid(row=1, column=1, padx=10, pady=5)

    # --- Amount ---
    ctk.CTkLabel(content_frame, text="Amount:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    amt_entry = ctk.CTkEntry(content_frame, width=250)
    amt_entry.insert(0, str(expense["amount"]))
    amt_entry.grid(row=2, column=1, padx=10, pady=5)

    # --- Date ---
    ctk.CTkLabel(content_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e", padx=10, pady=5)

    date_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    date_frame.grid(row=3, column=1, sticky="w")

    date_entry = ctk.CTkEntry(date_frame, width=190)
    date_entry.insert(0, expense["date"])
    date_entry.pack(side="left", padx=(0, 5))

    cal_btn = ctk.CTkButton(date_frame, text="📅", width=40, command=toggle_calendar)
    cal_btn.pack(side="left")

    # --- Category ---
    ctk.CTkLabel(content_frame, text="Category:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
    category_option = ctk.CTkOptionMenu(content_frame, values=["Home", "Work", "Food", "Entertainment", "Other"])
    category_option.set(expense.get("category", "Other"))
    category_option.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    # --- Result Label ---
    result_label = ctk.CTkLabel(content_frame, text="", text_color="red")
    result_label.grid(row=6, column=0, columnspan=2, pady=(10, 5))

    # --- Save Button ---
    def save_changes():
        new_desc = desc_entry.get().strip()
        new_amt = amt_entry.get().strip()
        new_date = date_entry.get().strip()
        new_category = category_option.get()

        if not new_desc or not new_amt:
            result_label.configure(text="Description and amount are required.")
            return

        try:
            new_amt = float(new_amt)
            if new_amt <= 0:
                raise ValueError
        except ValueError:
            result_label.configure(text="Enter a valid positive amount.")
            return

        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            result_label.configure(text="Invalid date format.")
            return

        data = load_data()
        for exp in data["expenses"]:
            if exp["id"] == expense["id"]:
                exp["description"] = new_desc
                exp["amount"] = new_amt
                exp["date"] = new_date
                exp["category"] = new_category
                break

        save_data(data)
        messagebox.showinfo("Success", "Expense updated successfully!")
        popup.destroy()
        parent_window.destroy()
        modify_expenses_gui()

    save_btn = ctk.CTkButton(content_frame, text="Save Changes", command=save_changes)
    save_btn.grid(row=7, column=0, columnspan=2, pady=15)

def modify_expenses_gui():
    data = load_data()
    expenses = data.get("expenses", [])

    if not expenses:
        messagebox.showinfo("No Data", "No expenses to modify.")
        return

    modify_window = ctk.CTkToplevel()
    modify_window.title("Modify Expenses")
    modify_window.geometry("800x550")

    scroll_frame = ctk.CTkScrollableFrame(modify_window, width=780, height=500)
    scroll_frame.pack(pady=10)

    headers = ["ID", "Date", "Category", "Amount", "Description"]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=5, pady=5)

    label = ctk.CTkLabel(scroll_frame, text="Actions", font=ctk.CTkFont(weight="bold"))
    label.grid(row=0, column=5, columnspan=2, padx=5, pady=5)

    for row, exp in enumerate(expenses, start=1):
        ctk.CTkLabel(scroll_frame, text=str(exp["id"])).grid(row=row, column=0, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["date"]).grid(row=row, column=1, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["category"]).grid(row=row, column=2, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=f"₹{exp['amount']}").grid(row=row, column=3, padx=5, pady=2)
        ctk.CTkLabel(scroll_frame, text=exp["description"]).grid(row=row, column=4, padx=5, pady=2)

        # 🗑️ Delete Button
        delete_btn = ctk.CTkButton(
            scroll_frame,
            text="🗑️",
            width=40,
            fg_color="transparent",
            text_color="red",
            command=lambda exid=exp["id"]: delete_expense_by_id(exid, modify_window)
        )
        delete_btn.grid(row=row, column=5, padx=5, sticky="e")

        # ✏️ Update Button
        update_btn = ctk.CTkButton(
            scroll_frame,
            text="✏️",
            width=40,
            fg_color="transparent",
            text_color="green",
            command=lambda ex=exp: open_update_popup(ex, modify_window)
        )
        update_btn.grid(row=row, column=6, padx=(5, 5), sticky="w")

# ------------------- Main GUI-------------------
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("1000x620")

calendar_widget_home = [None]

# ------------------- Top Bar with Theme Toggle ------------------- #
def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Light":
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")

top_bar = ctk.CTkFrame(app, fg_color="transparent")
top_bar.pack(fill="x", padx=20, pady=(10, 0))

theme_toggle_btn = ctk.CTkButton(
    top_bar, text="🌗 Toggle Theme", command=toggle_theme, width=130
)
theme_toggle_btn.pack(side="right", anchor="ne")

# ------------------- Combined Main Layout -------------------

main_content_wrapper = ctk.CTkFrame(app)
main_content_wrapper.pack(padx=20, pady=20, fill="both", expand=True)

left_main_area = ctk.CTkFrame(main_content_wrapper)
left_main_area.pack(side="left", fill="both", expand=True)

# ------------------- Add Expense Form -------------------

form_frame = ctk.CTkFrame(left_main_area)
form_frame.pack(pady=10)
form_frame.pack_propagate(False) 

ctk.CTkLabel(form_frame, text="Add New Expense", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)

ctk.CTkLabel(form_frame, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
desc_entry = ctk.CTkEntry(form_frame, width=300)
desc_entry.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
amt_entry = ctk.CTkEntry(form_frame, width=300)
amt_entry.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(form_frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="e")

date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
date_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")

date_entry = ctk.CTkEntry(date_frame, width=240)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
date_entry.pack(side="left", padx=(0, 5))

calendar_widget_home = [None]

def toggle_calendar_home():
    if calendar_widget_home[0]:
        calendar_widget_home[0].destroy()
        calendar_widget_home[0] = None
    else:
        cal = Calendar(
            master=form_frame,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            showweeknumbers=False
        )
        calendar_widget_home[0] = cal

        cal.place(x=320, y=140)

        def on_select(event=None):
            selected_date = cal.get_date()
            date_entry.delete(0, "end")
            date_entry.insert(0, selected_date)
            cal.destroy()
            calendar_widget_home[0] = None

        cal.bind("<<CalendarSelected>>", on_select)


ctk.CTkButton(date_frame, text="📅", width=40, command=toggle_calendar_home).pack(side="left")

ctk.CTkLabel(form_frame, text="Category:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
category_option = ctk.CTkOptionMenu(form_frame, values=["Home", "Work", "Food", "Entertainment", "Other"])
category_option.grid(row=4, column=1, padx=10, pady=5)

result_label = ctk.CTkLabel(form_frame, text="")
result_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))

button_frame = ctk.CTkFrame(form_frame)
button_frame.grid(row=7, column=0, columnspan=2, pady=10)

search_btn = ctk.CTkButton(form_frame, text="Search by Description", command=open_search_window)
search_btn.grid(row=7, column=0, columnspan=2, pady=10, sticky="n")

submit_btn = ctk.CTkButton(button_frame, text="Add Expense", command=submit_expense)
submit_btn.pack(side="left", padx=10)

view_btn = ctk.CTkButton(button_frame, text="View Expenses", command=view_expenses)
view_btn.pack(side="left", padx=10)

export_btn = ctk.CTkButton(button_frame, text="Export to CSV", command=export_to_csv_gui)
export_btn.pack(side="left", padx=10)

summary_btn = ctk.CTkButton(button_frame, text="Visualize Summary", command=open_summary_window)
summary_btn.pack(side="left", padx=10)

modify_btn = ctk.CTkButton(button_frame, text="Modify Expense", command=modify_expenses_gui)
modify_btn.pack(side="left", padx=10)


# ------------------- Dashboard Summary -------------------

right_summary_panel = ctk.CTkFrame(
    main_content_wrapper,
    width=260,
    corner_radius=15,
    fg_color="transparent"  # Or leave default
)
right_summary_panel.pack(side="right", padx=(15, 0), fill="y")

scrollable_dashboard = ctk.CTkScrollableFrame(
    right_summary_panel,
    width=240,
    corner_radius=0,
    fg_color="transparent"
)
scrollable_dashboard.pack(fill="both", expand=True, pady=10, padx=10)

# Dashboard Title
ctk.CTkLabel(
    scrollable_dashboard,
    text="📊 Dashboard Summary",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(pady=(10, 15))

card_row = ctk.CTkFrame(scrollable_dashboard, fg_color="transparent")
card_row.pack()

from collections import Counter
data = load_data()
expenses = data.get("expenses", [])

# ---- Dashboard Metrics ----
total_spent = sum(exp["amount"] for exp in expenses)
total_entries = len(expenses)
categories = set(exp.get("category", "General") for exp in expenses)
total_categories = len(categories)
avg_expense = total_spent / total_entries if total_entries > 0 else 0

category_counts = Counter(exp.get("category", "General") for exp in expenses)
top_category = category_counts.most_common(1)[0][0] if category_counts else "N/A"

highest_expense = max((exp["amount"] for exp in expenses), default=0)
highest_expense_entry = next((exp for exp in expenses if exp["amount"] == highest_expense), None)
costliest_day = highest_expense_entry.get("date") if highest_expense_entry else "N/A"

least_used_category = (
    min(category_counts.items(), key=lambda x: x[1])[0] if category_counts else "N/A"
)

lowest_expense = min((exp["amount"] for exp in expenses), default=0)

date_counts = Counter(exp.get("date", "Unknown") for exp in expenses)
most_active_day = date_counts.most_common(1)[0] if date_counts else ("N/A", 0)

desc_counts = Counter(exp.get("description", "").strip().lower() for exp in expenses)
recurring_desc = desc_counts.most_common(1)[0][0].title() if desc_counts else "N/A"

# -------- All Dashboard Cards --------
cards = [
    ("💰 Total", f"₹{total_spent:.2f}"),
    ("📂 Categories", str(total_categories)),
    ("🧾 Entries", str(total_entries)),
    ("📉 Avg", f"₹{avg_expense:.2f}"),
    ("💸 Top Category", top_category),
    ("🔝 Highest Expense", f"₹{highest_expense:.2f}"),
    ("📆 Costliest Day", costliest_day),
    ("🧍‍♀️ Least Used", least_used_category),
    ("📉 Lowest Expense", f"₹{lowest_expense:.2f}"),
    ("🗓️ Most Active Day", f"{most_active_day[0]} ({most_active_day[1]} records)"),
    ("🔁 Recurring Entry", recurring_desc)
]


def create_stat_card(parent, title, value):
    card = ctk.CTkFrame(
        parent, width=220, height=80, corner_radius=10
    )
    card.pack_propagate(False)
    title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=13))
    value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=18, weight="bold"))
    title_label.pack(pady=(10, 3))
    value_label.pack()
    card.pack(pady=10)

for title, value in cards:
    create_stat_card(card_row, title, value)

app.mainloop()
