import sqlite3

def connect_db():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    ''')
    connection.commit()
    return connection

def add_expense(date, category, amount):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)", (date, category, amount))
    connection.commit()
    connection.close()

def get_expenses():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    connection.close()
    return expenses
