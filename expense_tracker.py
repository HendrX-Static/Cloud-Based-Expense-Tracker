import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime

# MySQL connection setup
db_config = {
    'host': 'your-database-endpoint',
    'user': 'your-username',
    'password': 'your-password',
    'database': 'python_GUI_project'
}

# Functions
def add_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    type_ = combo_type.get()
    
    # Validate inputs
    if not all([date, category, amount, type_]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
        return

    # Validate amount
    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Amount Error", "Amount must be a number.")
        return

    # If all validations pass, proceed with adding the expense
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, amount, type) VALUES (%s, %s, %s, %s)",
                       (date, category, amount, type_))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
        entry_date.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        combo_type.set('')
        update_balance()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def view_expenses():
    listbox.delete(*listbox.get_children())
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        records = cursor.fetchall()
        for record in records:
            listbox.insert("", "end", values=record)
        update_balance()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def generate_report():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE type='Expense' GROUP BY category")
        records = cursor.fetchall()
        report_text = "Expense Report:\n\n"
        for record in records:
            report_text += f"Category: {record[0]}, Total Amount: {record[1]}\n"
        messagebox.showinfo("Expense Report", report_text)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_all_data():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses")
        conn.commit()
        messagebox.showinfo("Success", "All data deleted successfully!")
        update_balance()
        view_expenses()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def update_balance():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='Income'")
        income = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE type='Expense'")
        expense = cursor.fetchone()[0] or 0
        balance = income - expense
        label_balance.config(text=f"Balance: ₹{balance:.2f}")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def initialize_gui():
    global entry_date, entry_category, entry_amount, combo_type, listbox, label_balance

    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("1010x540")

    tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(root, text="Category").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(root, text="Amount").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(root, text="Type").grid(row=3, column=0, padx=5, pady=5)

    entry_date = ttk.Entry(root, font=("Arial", 10))
    entry_category = ttk.Entry(root, font=("Arial", 10))
    entry_amount = ttk.Entry(root, font=("Arial", 10))
    combo_type = ttk.Combobox(root, values=["Income", "Expense"], font=("Arial", 10))

    entry_date.grid(row=0, column=1, padx=5, pady=5)
    entry_category.grid(row=1, column=1, padx=5, pady=5)
    entry_amount.grid(row=2, column=1, padx=5, pady=5)
    combo_type.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(root, text="Add Record", command=add_expense).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(root, text="View Records", command=view_expenses).grid(row=5, column=0, columnspan=2, pady=5)
    ttk.Button(root, text="Generate Report", command=generate_report).grid(row=6, column=0, columnspan=2, pady=5)
    ttk.Button(root, text="Delete All Data", command=delete_all_data).grid(row=7, column=0, columnspan=2, pady=5)

    columns_ = ("ID", "Date", "Category", "Amount", "Type")
    listbox = ttk.Treeview(root, columns=columns_, show="headings")
    for col in columns_:
        listbox.heading(col, text=col)
    listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    label_balance = ttk.Label(root, text="Balance: ₹0.00", font=("Arial", 12, "bold"))
    label_balance.grid(row=9, column=0, columnspan=2, pady=5)

    update_balance()
    root.update_idletasks()
    root.mainloop()

initialize_gui()
