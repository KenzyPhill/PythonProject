import sqlite3

# connect to sqlite database
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

# Create user table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)

# Create patient table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            medical_history TEXT
        );
    """)

# Create appointments table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            user_id INTEGER,
            appointment_time TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        );
    """)

conn.commit()
conn.close()

print("SQLite database and tables created successfully ")