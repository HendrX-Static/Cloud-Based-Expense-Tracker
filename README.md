# Expense Tracker

This is a simple Expense Tracker application built with Python and Tkinter for the GUI, and MySQL for the database. The application allows users to add, view, generate reports, and delete expense records.

## Features

- **Add Expense/Income:** Input details like date, category, amount, and type (Income/Expense).
- **View Records:** Display all the expense and income records.
- **Generate Report:** Generate a summary report of expenses by category.
- **Delete All Data:** Remove all records from the database.
- **Update Balance:** Display the current balance based on income and expenses.

## Prerequisites

- Python 3.x
- AWS (or any other cloud database provider)
- MySql (if not using cloud)
- Tkinter library (included with Python standard library)
- `mysql-connector-python` library

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/HendrX-Static/ExpenseTracker.git
    cd ExpenseTracker
    ```

2. **Install the MySQL connector library:**

    ```bash
    pip install mysql-connector-python
    ```

3. **Setup MySQL Database:**

    - Create a MySQL database named `python_GUI_project`.
    - Create a table named `expenses` with the following structure:

    ```sql
    CREATE TABLE expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        category VARCHAR(255) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        type VARCHAR(50) NOT NULL
    );
    ```

    - Do this on your cloud database if using one.

## Usage

Run the script to start the Expense Tracker application:

```bash
python expense_tracker.py
```

## Code Overview

### MySQL Connection Setup

```python
db_config = {
    'host': 'your-database-endpoint',
    'user': 'your-username',
    'password': 'your-password',
    'database': 'python_GUI_project'
}
```

### Functions

- `add_expense()`: Adds a new expense or income record to the database.
- `view_expenses()`: Fetches and displays all records from the database.
- `generate_report()`: Generates a summary report of expenses by category.
- `delete_all_data()`: Deletes all records from the database.
- `update_balance()`: Calculates and displays the current balance.
- `initialize_gui()`: Initializes and runs the Tkinter GUI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Tkinter for the GUI framework.
- MySQL for the database management.
- The Python community for continuous support and development.
