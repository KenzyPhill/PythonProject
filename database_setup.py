# This script sets up a SQLite database for a healthcare application.

import sqlite3 # Importing the sqlite3 module to interact with SQLite databases
from werkzeug.security import generate_password_hash # Importing the generate_password_hash function from werkzeug.security for password hashing






# This function sets up the SQLite database and creates a table for user roles if it doesn't exist and inserts sample data for testing purposes.
def user_roles_database():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS roles")  # Drop the table if it exists (for testing purposes)

    # Create the roles table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name VARCHAR(50) UNIQUE NOT NULL, -- Unique role name for each user role e.g. "admin", "doctor", "nurse", "receptionist", "patient"
            role_description TEXT -- Optional details about the role. TEXT type is used here for long text descriptions.
        );
    """)


    # Uncomment the following line to clear existing data in the 'roles' table
    # This is for testing purposes only and should be commented out in production.
    # cursor.execute("DELETE FROM roles")  # Clear existing data for testing 


    # Sample data to insert into the 'roles' table for testing purposes:
    # The sample data includes various user roles such as admin, doctor, nurse, receptionist, and patient.
    # This is a one-time setup to create the table and insert sample data.
    # Insert sample data into the 'roles' table
    sample_data = [
        ("Patient", "Individual receiving medical care."),
        ("Receptionist", "Handles patient appointments and administrative tasks."),
        ("Nurse", "Provides patient care and assists doctors in medical procedures."),
        ("Doctor", "Medical professional responsible for diagnosing and treating patients."),
        ("Pediatrician", "Specializes in the medical care of infants, children, and adolescents."),
        ("Surgeon", "Performs surgical procedures on patients."),
        ("Radiologist", "Specializes in interpreting medical images such as X-rays and MRIs."),
        ("Therapist", "Provides rehabilitation and therapy services to patients."),
        ("Dietitian", "Advises patients on nutrition and dietary plans."),

        ("Admin", "Manages system access and patient records."),
        ("Super Admin", "Has full access to all system features and settings."),
        ("User", "General user with limited access."),
        ("Guest", "Temporary user with minimal access.")

    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT INTO roles (role_name, role_description)
                        VALUES (?, ?);""", data)


    # Note: The 'INSERT OR IGNORE' statement will ignore the insertion if a record with the same primary key already exists.
    # This prevents duplicate entries when running the script multiple times.
    # To overwrite existing records, can use 'INSERT OR REPLACE' instead.


    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("\nSample data inserted into the 'roles' table.")




# This function sets up the SQLite database and creates a table for user records if it doesn't exist and inserts sample data for testing purposes.
def user_accounts_database():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")  # Drop the table if it exists (for testing purposes)

    # Create the users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        -- fullname TEXT NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,  -- Unique username for each user
        password VARCHAR(255) NOT NULL,    -- Hashed password for security
        role VARCHAR(50) NOT NULL,    -- "admin", "doctor", "nurse", "receptionist", "patient"
        status VARCHAR(20) NOT NULL, -- "active", "inactive", "suspended"
        title VARCHAR(15),  -- "Mr.", "Ms.", "Dr."
        first_name VARCHAR(50),
        middle_name VARCHAR(50),    -- Optional
        last_name VARCHAR(50),
        suffix VARCHAR(10),  -- "Jr.", "III", etc. (Optional)
        date_of_birth DATE,
        gender VARCHAR(20),
        address TEXT,  -- Optional
        phone TEXT, -- Optional
        email TEXT, -- Optional
        question1 TEXT, -- Optional security question 1
        answer1 TEXT, -- Optional answer to security question 1
        question2 TEXT, -- Optional security question 2
        answer2 TEXT, -- Optional answer to security question 2
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the record was created
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of when the record was last updated
        FOREIGN KEY (role) REFERENCES roles (role_name) -- Foreign key reference to the roles table
                   
    );
    """)


    # Uncomment the following line to clear existing data in the 'users' table
    # This is for testing purposes only and should be commented out in production.
    # cursor.execute("DELETE FROM users")  # Clear existing data for testing


    # Sample data to insert into the 'users' table for testing purposes:
    # The sample data includes various user roles such as admin, doctor, nurse, receptionist, and patient.
    # The function 'generate_password_hash' from the 'werkzeug.security' module is used to hash passwords for security.
    sample_data = [
        ("admin", generate_password_hash("admin123"), "Admin", "Active", "Mr","Admin", "middle_name", "last_name", "suffix", "04/01/1973", "Male", "17a", "07534894161", "admin@example.com", "question1", "answer1", "question2", "answer2"),
        ("doctor", generate_password_hash("doctor123"), "Doctor", "Active", "Dr","Doctor", "middle_name", "last_name", "suffix", "04/01/1974", "Female", "17a", "07956498479", "doc@example.com", "question1", "answer1", "question2", "answer2"),
        ("nurse", generate_password_hash("nurse123"), "Nurse", "Active", "Ms","Nurse", "middle_name", "last_name", "suffix", "04/01/1975", "Female", "17a", "07839874653", "nurse@example.com", "question1", "answer1", "question2", "answer2"),
        ("receptionist", generate_password_hash("receptionist123"), "Receptionist", "Active", "Ms","Receptionist", "middle_name", "last_name", "suffix", "04/01/1976", "Female", "17a", "07737654387", "recep@example.com", "question1", "answer1", "question2", "answer2"),
        ("user", generate_password_hash("user123"), "User", "Active", "","User", "middle_name", "last_name", "suffix", "04/01/1977", "Female", "17a", "07986785435", "user@example.com", "question1", "answer1", "question2", "answer2"),
        ("guest", generate_password_hash("guest123"), "Guest", "Active", "","Guest", "middle_name", "last_name", "suffix", "04/01/1978", "Female", "17a", "07384756356", "guest@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient1", generate_password_hash("patient123"), "Patient", "Active", "Ms","Sadia", "", "Jafreen", "", "21/12/1975", "Female", "17a", "07850405639", "sadia@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient2", generate_password_hash("patient123"), "Patient", "Active", "Mr","David", "Anthony", "Bieda", "Sr.", "23/11/1945", "Male", "17a", "02074973703", "david@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient3", generate_password_hash("patient123"), "Patient", "Active", "Ms","Zaynah", "", "Uddin", "MInstP", "06/06/2002", "Female", "17a", "02074973706", "zaynah@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient4", generate_password_hash("patient123"), "Patient", "Active", "Ms","Jane", "", "Smith", "IV", "18/08/1971", "Non-binary", "17a", "02074973704", "jane@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient5", generate_password_hash("patient123"), "Patient", "Active", "Ms","Zaynah", "Zay", "Uddin", "", "10/11/2002", "Female", "17a", "02074973707", "zay@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient6", generate_password_hash("patient123"), "Patient", "Active", "Mr","Jazib", "", "Uddin", "suffix", "30/07/2007", "Other", "17a", "02074973708", "jazib@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient7", generate_password_hash("patient123"), "Patient", "Active", "Ms","Patient", "", "Seven", "7", "21/02/1964", "Non-binary", "17a", "02074973709", "7@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient8", generate_password_hash("patient123"), "Patient", "Active", "Mr","Patient", "", "Eight", "8", "08/05/1040", "Female", "17a", "02074973710", "8@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient9", generate_password_hash("patient123"), "Patient", "Active", "Ms","Patient", "", "Nine", "9", "12/04/1958", "Other", "17a", "02074973711", "9@example.com", "question1", "answer1", "question2", "answer2"),
        ("patient10", generate_password_hash("patient123"), "Patient", "Active", "Mr","Patient", "", "Ten", "10", "09/04/1932", "Male", "17a", "02074973712", "10@example.com", "question1", "answer1", "question2", "answer2")
    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT INTO users (username, password, role, status, title, first_name, middle_name, last_name, suffix, date_of_birth, gender, address, phone, email, question1, answer1, question2, answer2)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", data)


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
        patient_dob INTEGER NOT NULL,
        patient_gender TEXT,
        patient_address TEXT,
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
        ("7", "Sadia Jafreen", "21/12/1975", "Female", "Address", "1234567890", "sadia@example.com", "Diabetes"),
        ("8", "David Bieda", "23/11/1945", "Male", "Address", "2345678901", "db@example.com", "Hypertension"),
        ("9", "Zaynah Uddin", "06/06/2002", "Female", "Address", "4567890123", "None", "None"),
        ("10", "Jane Smith", "18/08/1971", "Female", "Address", "3456789012", "jonh@example.com", "Asthma"),
        ("11", "Zaynah Uddin", "10/11/2002", "Female", "Address", "5678901234", "zu@example.com", "Migranes"),
        ("12", "Jazib Uddin", "30/07/2007", "Male", "Address", "7890123456", "jaz@example.com", "Hypertension")
    ]

    # Insert each record into the table
    for data in sample_data:
        cursor.execute("""INSERT OR IGNORE INTO patients (user_id, patient_name, patient_dob, patient_gender, patient_address, patient_phone, patient_email, medical_history)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", data)


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
    user_roles_database()
    user_accounts_database()
    patients_database()
    appointments_database()
    print("\n**Team 2 Database setup complete.**\n")