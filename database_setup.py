# This script sets up a SQLite database for a healthcare application.

import sqlite3 # Importing the sqlite3 module to interact with SQLite databases
from werkzeug.security import generate_password_hash # Importing the generate_password_hash function from werkzeug.security for password hashing


# This function sets up the SQLite database and creates a table for user records if it doesn't exist and inserts sample data for testing purposes.
def user_accounts_database():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")  # Drop the table if it exists (for testing purposes)

    # Create the users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT
    )
    """)


    # Uncomment the following line to clear existing data in the 'users' table
    # This is for testing purposes only and should be commented out in production.
    # cursor.execute("DELETE FROM users")  # Clear existing data for testing


    # Sample data to insert into the 'users' table for testing purposes:
    # The sample data includes various user roles such as admin, doctor, nurse, receptionist, and patient.
    # The function 'generate_password_hash' from the 'werkzeug.security' module is used to hash passwords for security.
    sample_data = [
        ("Admin User", "admin", generate_password_hash("admin123"), "admin"),
        ("Doctor User", "doctor", generate_password_hash("doctor123"), "doctor"),
        ("Nurse User", "nurse", generate_password_hash("nurse123"), "nurse"),
        ("Receptionist User", "receptionist", generate_password_hash("receptionist123"), "receptionist"),
        ("User User", "user1", generate_password_hash("user123"), "user"),
        ("Sadia Jafreen", "patient1", generate_password_hash("patient123"), "patient"),
        ("David Bieda", "patient2", generate_password_hash("patient123"), "patient"),
        ("Jane Smith", "patient3", generate_password_hash("patient123"), "patient"),
        ("Zaynah Uddin", "patient4", generate_password_hash("patient123"), "patient"),
        ("Zaynah Uddin", "patient5", generate_password_hash("patient123"), "patient"),
        ("John Doe", "patient6", generate_password_hash("patient123"), "patient"),
        ("Jazib Uddin", "patient7", generate_password_hash("patient123"), "patient"),
        ("Patient Eight", "patient8", generate_password_hash("patient123"), "patient"),
        ("Patient Nine", "patient9", generate_password_hash("patient123"), "patient"),
        ("Patient Ten", "patient10", generate_password_hash("patient123"), "patient")
    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT INTO users (fullname, username, password, role)
                        VALUES (?, ?, ?, ?);""", data)


    # Note: The 'INSERT OR IGNORE' statement will ignore the insertion if a record with the same primary key already exists.
    # This prevents duplicate entries when running the script multiple times.
    # To overwrite existing records, can use 'INSERT OR REPLACE' instead.


    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("\nSample data inserted into the 'users' table.")




# This function sets up the SQLite database and creates a table for patient records if it doesn't exist and inserts sample data for testing purposes.
def patients_database():
    # Connect to SQLite database (or create if it doesn't exist)
    conn = sqlite3.connect("healthcare.db")
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS patients")  # Drop the table if it exists (for testing purposes)
    
    # Create a table for patients if it doesn't exist
    # This table will store patient records, including their personal information and medical history.
    # The 'user_id' column is a foreign key referencing the 'user_id' in the 'users' table.
    cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL UNIQUE,
        patient_name TEXT NOT NULL,
        patient_age INTEGER NOT NULL,
        patient_gender TEXT,
        patient_phone TEXT,
        patient_email TEXT,
        medical_history TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    );""")
    

    # Uncomment the following line to clear existing data in the 'patients' table
    # This is for testing purposes only and should be commented out in the final.
    # cursor.execute("DELETE FROM patients")  # Clear existing data for testing purposes


    # Sample data to insert into the 'patients' table for testing purposes
    # This is a one-time setup to create the table and insert sample data.
    # Insert sample data into the 'patients' table
    sample_data = [
        ("6", "Sadia Jafreen", 28, "Female", "1234567890", "sadia@example.com", "Diabetes"),
        ("7", "David Bieda", 75, "Male", "2345678901", "db@example.com", "Hypertension"),
        ("8", "Jane Smith", 42, "Female", "3456789012", "jonh@example.com", "Asthma"),
        ("9", "Zaynah Uddin", 26, "Female", "4567890123", None, "None"),
        ("12", "Jazib Uddin", 18, "Male", "7890123456", "jaz@example.com", "Hypertension"),
        ("10", "Zaynah Uddin", 32, "Female", "5678901234", "zu@example.com", "Migranes"),
        ("11", "John Doe", 34, "Other", "", "", "Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes "),
    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT OR IGNORE INTO patients (user_id, patient_name, patient_age, patient_gender, patient_phone, patient_email, medical_history)
                        VALUES (?, ?, ?, ?, ?, ?, ?);""", data)


    # Note: The 'INSERT OR IGNORE' statement will ignore the insertion if a record with the same primary key already exists.
    # This prevents duplicate entries when running the script multiple times.
    # To overwrite existing records, can use 'INSERT OR REPLACE' instead.

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("\nSample data inserted into the 'patients' table.")




# This function sets up the SQLite database and creates a table for appointment records if it doesn't exist.
def appointments_database():
    # Connect to SQLite database (or create if it doesn't exist)
    conn = sqlite3.connect("healthcare.db")
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS appointments")  # Drop the table if it exists (for testing purposes)
    
    # # Version 1: Create a table for appointments without foreign key reference to patients table
    # # Create a table for appointments
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS appointments (
    #         ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #         patient_name TEXT NOT NULL,
    #         appointment_date TEXT NOT NULL,
    #         appointment_time TEXT NOT NULL,
    #         provider_name TEXT NOT NULL
    #     );
    # """)

    # # Version 2: Create a table for appointments with foreign key references to users and patients tables
    # # Create a table for appointments
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS appointments (
    #         appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         user_id INTEGER,
    #         patient_id INTEGER,
    #         patient_name TEXT NOT NULL,
    #         appointment_date TEXT NOT NULL,
    #         appointment_time TEXT NOT NULL,
    #         provider_name TEXT NOT NULL,
    #         FOREIGN KEY (user_id) REFERENCES users (user_id),
    #         FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
    #     );
    # """)


    # Version 3: Create a table for appointments with foreign key reference to patients table only
    # Create a table for appointments if it doesn't exist
    # This table will store appointment records for patients
    # The 'patient_id' column is a foreign key referencing the 'patient_id' in the 'patients' table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            patient_name TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            provider_name TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        );
    """)


    # Sample data to insert into the 'appointments' table for testing purposes
    # This is a one-time setup to create the table and insert sample data.
    # Insert sample data into the 'appointments' table
    sample_data = [
        ("1", "Sadia Jafreen", "30/04/2025" , "09:00 AM", "Dr. John Smith"),
        ("1", "Sadia Jafreen", "30/04/2025" , "10:00 AM", "Dr. John Smith"),
        ("2", "David Bieda", "30/04/2025", "09:00 AM", "Dr. Emily Brown"),
        ("3", "Jane Smith", "30/04/2025", "10:00 AM", "Dr. Emily Brown"),
        ("4", "Zaynah Uddin", "30/04/2025", "11:00 AM", "Dr. Emily Brown"),
        ("6", "Zaynah Uddin", "30/04/2025", "12:00 PM", "Dr. Emily Brown"),
        ("7", "John Doe", "30/04/2025", "09:00 AM", "Dr. Michael Lee"),
        ("5", "Jazib Uddin", "01/05/2025", "09:00 AM", "Dr. Sarah Davis"),
    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT OR IGNORE INTO appointments (patient_id, patient_name, appointment_date, appointment_time, provider_name)
                        VALUES (?, ?, ?, ?, ?);""", data)


    # Note: The 'INSERT OR IGNORE' statement will ignore the insertion if a record with the same primary key already exists.
    # This prevents duplicate entries when running the script multiple times.
    # To overwrite existing records, can use 'INSERT OR REPLACE' instead.

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("\nSample data inserted into the 'appointments' table.")


# Main block to execute the database setup function
# This block will only run if the script is executed directly, not if it's imported as a module.
# Call the setup_database function to create the database and table
if __name__ == "__main__":
    user_accounts_database()
    patients_database()
    appointments_database()
    print("\n**Team 2 Database setup complete.**\n")