import sqlite3

def init_db():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        join_date TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        amount REAL,
        product TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")

    # Insert Mock Data
    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?,?,?,?)", [
        (1, 'Alice Smith', 'Engineer', '2023-01-15'),
        (2, 'Bob Jones', 'Manager', '2022-05-11'),
        (3, 'Charlie Brown', 'Sales', '2024-02-01')
    ])

    cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?)", [
        (101, 1, 150.00, 'Laptop Stand'),
        (102, 3, 1200.00, 'Enterprise Software'),
        (103, 1, 45.50, 'Wireless Mouse')
    ])

    conn.commit()
    conn.close()
    print("Database 'company.db' initialized successfully.")

if __name__ == "__main__":
    init_db()
