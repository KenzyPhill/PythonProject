import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
# import database_setup # Importing the database_setup module to set up the database and tables
from database_setup import user_accounts_database # Importing the user_accounts_database function from the database_setup module
from database_setup import patients_database # Importing the patients_database function from the database_setup module


# # Database Setup Function
# # This function sets up the SQLite database and creates a table for patient records if it doesn't exist.
# def patients_database():
#     # Connect to SQLite database (or create if it doesn't exist)
#     conn = sqlite3.connect("healthcare.db")
#     # Create a cursor object to execute SQL commands
#     cursor = conn.cursor()


#     # Only run this if you want to reset the database and start fresh.
#     cursor.execute("DROP TABLE IF EXISTS patients")  # Drop the table if it exists (for testing purposes)
#     # cursor.execute("DROP TABLE IF EXISTS users")  # Drop the table if it exists (for testing purposes)
#     # cursor.execute("DROP TABLE IF EXISTS appointments")  # Drop the table if it exists (for testing purposes)
#     # cursor.execute("DROP TABLE IF EXISTS doctors")  # Drop the table if it exists (for testing purposes)
    
#     # Create a table for patients if it doesn't exist
#     cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
#         patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER NOT NULL UNIQUE,
#         patient_name TEXT NOT NULL,
#         patient_age INTEGER NOT NULL,
#         patient_gender TEXT,
#         patient_phone TEXT,
#         patient_email TEXT,
#         medical_history TEXT,
#         FOREIGN KEY (user_id) REFERENCES users (user_id)
#     );""")
    

#     # Uncomment the following line to clear existing data in the 'patients' table
#     # This is for testing purposes only and should be commented out in production.
#     # cursor.execute("DELETE FROM patients")  # Clear existing data for testing purposes


#     # Sample data to insert into the 'patients' table for testing purposes
#     # Uncomment the following lines to insert sample data into the 'patients' table
#     # This is a one-time setup to create the table and insert sample data.
#     # Insert sample data into the 'patients' table
#     sample_data = [
#         ("6", "Sadia Jafreen", 28, "Female", "1234567890", "sadia@example.com", "Diabetes"),
#         ("7", "David Bieda", 75, "Male", "2345678901", "db@example.com", "Hypertension"),
#         ("8", "Jane Smith", 42, "Female", "3456789012", "jonh@example.com", "Asthma"),
#         ("9", "Zaynah Uddin", 26, "Female", "4567890123", None, "None"),
#         ("12", "Jazib Uddin", 18, "Male", "7890123456", "jaz@example.com", "Hypertension"),
#         ("10", "Zaynah Uddin", 32, "Female", "5678901234", "zu@example.com", "Migranes"),
#         ("11", "John Doe", 34, "Other", "", "", "Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes Migranes "),
#     ]

#     # Insert each record into the table
#     for data in sample_data:
#         cursor.execute("""INSERT OR IGNORE INTO patients (user_id, patient_name, patient_age, patient_gender, patient_phone, patient_email, medical_history)
#                         VALUES (?, ?, ?, ?, ?, ?, ?);""", data)


#     # Note: The 'INSERT OR IGNORE' statement will ignore the insertion if a record with the same primary key already exists.
#     # This prevents duplicate entries when running the script multiple times.
#     # To overwrite existing records, can use 'INSERT OR REPLACE' instead.

#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

#     # print("Sample data inserted into the 'patients' table.")

















# # Function to Fetch Patient Names from the Same Database
# def fetch_user_info():
#     conn = sqlite3.connect("healthcare.db")  # Using the same database file
#     cursor = conn.cursor()
#     cursor.execute("SELECT fullname FROM users")  # Querying the users table
#     names = [row[0] for row in cursor.fetchall()]
#     conn.close()
#     print(f"Fetched names: {names}")  # Debugging fetched names
#     return names




# # Autocomplete Entry Class for Patient Names
# class AutocompleteEntry(ttk.Entry):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.suggestions = []  # List to hold autocomplete suggestions
#         self.bind("<KeyRelease>", self.update_suggestions)

#     def set_suggestions(self, suggestions):
#         self.suggestions = suggestions

#     def update_suggestions(self, event=None):
#         typed_text = self.get()
#         if not typed_text:
#             if hasattr(self, "listbox"):
#                 self.listbox.destroy()
#             return

#         # Debug: Display typed text
#         # print(f"Typed text: {typed_text}")

#         matches = [s for s in self.suggestions if typed_text.lower() in s.lower()]

#         # Debug: Print matches found
#         # print(f"Matches: {matches}")

#         if hasattr(self, "listbox"):
#             self.listbox.destroy()

#         if matches:
#             self.listbox = tk.Listbox(self.master, height=len(matches))
#             # self.listbox = tk.Listbox(self.master, height=len(matches), bg="white", fg="black", borderwidth=1)

#             self.listbox.bind("<<ListboxSelect>>", self.select_suggestion)

#             for match in matches:
#                 self.listbox.insert(tk.END, match)

#             # Place listbox relative to the entry widget
#             self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

#             # Debug: Confirm Listbox placement
#             # print(f"Listbox placed at: {self.winfo_x()}, {self.winfo_y() + self.winfo_height()}")

#     def select_suggestion(self, event=None):
#         if hasattr(self, "listbox"):
#             self.delete(0, tk.END)
#             self.insert(0, self.listbox.get(self.listbox.curselection()))
#             self.listbox.destroy()





def fetch_user_info():
    # import sqlite3
    
    conn = sqlite3.connect("healthcare.db")  # Connect to the database
    cursor = conn.cursor()
    
    try:
        # Query the users table to fetch IDs and names
        cursor.execute("SELECT user_id, fullname FROM users")
        rows = cursor.fetchall()
        
        if not rows:  # Check if rows are empty
            print("No users or IDs found in the database.")
        else:
            print(f"Fetched data: {rows}")  # Debugging: Print fetched data
        
        return [(row[0], row[1]) for row in rows]  # Return list of tuples (ID, Name)
    
    except sqlite3.Error as e:  # Handle database errors
        print(f"Database error: {e}")
        return []
    
    finally:
        conn.close()  # Ensure connection is closed



# Autocomplete Entry Class
# This class extends the Entry widget to provide autocomplete functionality.
# It filters suggestions based on user input and displays them in a Listbox.
# The user can select a suggestion, which will populate the Patient Name field and the User ID field.
class AutocompleteEntry(ttk.Entry):
    def __init__(self, master=None, textvariable=None, user_id_var=None, patient_name_box=None, **kwargs):
        super().__init__(master, textvariable=textvariable, **kwargs)
        self.suggestions = []  # List to hold autocomplete suggestions
        self.user_id_var = user_id_var  # Reference to the User ID variable
        # self.user_id_box = user_id_box  # Reference to the User ID entry box
        # self.patient_id_box = patient_id_box  # Reference to the Patient ID entry box
        self.patient_name_box = patient_name_box  # Reference to the User ID entry box
        self.bind("<KeyRelease>", self.update_suggestions)

    def set_suggestions(self, suggestions):
        # `suggestions` should be a list of tuples (ID, Name), e.g., [(1, 'Alice'), (2, 'Bob')]
        self.suggestions = suggestions

    def update_suggestions(self, event=None):
        typed_text = self.get()
        if not typed_text:
            if hasattr(self, "listbox"):
                self.listbox.destroy()
            return

        # Filter suggestions based on typed text
        matches = [(pid, name) for pid, name in self.suggestions if typed_text.lower() in name.lower()]

        if hasattr(self, "listbox"):
            self.listbox.destroy()

        if matches:
            self.listbox = tk.Listbox(self.master, height=len(matches))
            self.listbox.bind("<<ListboxSelect>>", self.select_suggestion)

            # Insert matches with IDs and names into the Listbox
            for pid, name in matches:
                self.listbox.insert(tk.END, f"{pid} - {name}")

            # Place the listbox relative to the entry widget
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

    def select_suggestion(self, event=None):
        if hasattr(self, "listbox"):
            selected = self.listbox.get(self.listbox.curselection())
            self.listbox.destroy()

            # Extract the ID and Name from the selected suggestion
            uid, name = selected.split(" - ", 1)

            # # Place the User ID in the User ID box
            # if self.user_id_box:
            #     self.user_id_box.delete(0, tk.END)
            #     self.user_id_box.insert(0, uid)

            # Place the User ID in the User ID var
            if self.user_id_var:
                self.user_id_var.set(uid)

            # # Place the Patient ID in the Patient ID box
            # if self.patient_id_box:
            #     self.patient_id_box.delete(0, tk.END)
            #     self.patient_id_box.insert(0, pid)


            # Place the User Name in the Patient Name box
            if self.patient_name_box:
                self.patient_name_box.delete(0, tk.END)
                self.patient_name_box.insert(0, name)


            # Update the Entry field with the full selection
            if self.master and self.master.winfo_exists():
                self.delete(0, tk.END)
                self.insert(0, name)

                self.icursor(tk.END)  # Move cursor to the end of the entry
                self.focus()  # Set focus back to the entry widget


















# Functions for CRUD operations
def add_patient():
    if not validate_fields():
        return

    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    # # Check for duplicate Phone value
    # cursor.execute("SELECT COUNT(*) FROM patients WHERE patient_phone = ?", (phone_var.get(),))
    # duplicate_count = cursor.fetchone()[0]
    # if duplicate_count > 0:
    #     messagebox.showerror("Error", "A patient with this phone number already exists!")
    #     conn.close()
    #     return

    # # Check for duplicate Email value
    # cursor.execute("SELECT COUNT(*) FROM patients WHERE patient_email = ?", (email_var.get(),))
    # duplicate_count = cursor.fetchone()[0]
    # if duplicate_count > 0:
    #     messagebox.showerror("Error", "A patient with this email address already exists!")
    #     conn.close()
    #     return



    # Check for duplicate User ID
    cursor.execute("SELECT COUNT(*) FROM patients WHERE user_id = ?", (user_id_var.get(),))
    duplicate_count = cursor.fetchone()[0]
    if duplicate_count > 0:
        messagebox.showerror("Error", "A patient with this User ID already exists!")
        conn.close()
        return


    # Insert new patient if no duplicate is found
    cursor.execute("INSERT INTO patients (user_id, patient_name, patient_age, patient_gender, patient_phone, patient_email, medical_history) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (user_id_var.get(), patient_name_var.get(), age_var.get(), gender_var.get(), phone_var.get(), email_var.get(), history_var.get()))
    conn.commit()
    conn.close()
    clear_fields()
    load_patients()
    messagebox.showinfo("Success", "Patient added successfully!")

def load_patients():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    
    # Clear existing rows
    for row in tree.get_children():
        tree.delete(row)
    
    # Populate Treeview with patient records
    for row in rows:
        tree.insert("", tk.END, values=row)


# Function to edit a selected patient record
# This function retrieves the selected record from the Treeview, populates the input fields with its data, and allows the user to edit it.
def edit_patient():

    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a patient to edit.")
        return

    if not validate_fields():
        return

    if not user_id_var.get() == original_record[1]:
        messagebox.showerror("Error", "User ID changed! Record was not updated.")
        return

    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients 
        SET user_id=?, patient_name=?, patient_age=?, patient_gender=?, patient_phone=?, patient_email=?, medical_history=?
        WHERE patient_id=?
    """, (user_id_var.get(), patient_name_var.get(), age_var.get(), gender_var.get(), phone_var.get(), email_var.get(), history_var.get(), tree.item(selected[0])["values"][0]))
    conn.commit()
    conn.close()
    clear_fields()
    load_patients()
    messagebox.showinfo("Success", "Patient updated successfully!")

def delete_patient():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a patient to delete.")
        return
    
    # Get the selected row's values
    values = tree.item(selected[0], "values")
    record_details = f"ID: {values[0]} \nName: {values[1]} \nAge: {values[2]} \nGender: {values[3]} \nContact: {values[4]} \nMedical History: {values[5]}"
    
    # Display confirmation dialog
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the following record?\n\n{record_details}")
    if not confirm:
        return
    confirm = messagebox.askyesno("Warning", "Patient record will be parmanenty deleted. Proceed?")
    if not confirm:
        return

    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id=?", (tree.item(selected[0])["values"][0],))
    conn.commit()
    conn.close()
    load_patients()
    messagebox.showinfo("Success", "Patient deleted successfully!")

def clear_fields():
    # Clear all input variables and entry fields
    # user_id_entry.delete(0, tk.END)
    # patient_lookup_entry.delete(0, tk.END)
    # patient_name_entry.delete(0, tk.END)

    user_id_var.set("")
    patient_lookup_var.set("")
    patient_name_var.set("")
    age_var.set("")
    gender_var.set("Select Gender")
    phone_var.set("")
    email_var.set("")
    history_var.set("")


# Function to validate fields before adding or editing a patient
# This function checks if the input fields are filled correctly and shows error messages if not.
def validate_fields():
    if not patient_name_var.get().strip():
        messagebox.showerror("Error", "Name is required!")
        return False
    if not user_id_var.get().strip():
        messagebox.showerror("Error", "ID is required!")
        return False
    if not age_var.get().isdigit() or int(age_var.get()) <= 0:
        messagebox.showerror("Error", "Age must be a positive number!")
        return False
    
    # if gender_var.get().strip().lower() not in ("male", "female", "other"):
    #     messagebox.showerror("Error", "Gender must be 'Male', 'Female', or 'Other'!")
    #     return False

    # if gender_var.get() not in ("Male", "Female", "Other"):
    #     messagebox.showerror("Error", "Please select a valid gender from the dropdown!")
    #     return False
    
    if gender_var.get() == "Select Gender" or gender_var.get() == "":
        messagebox.showerror("Error", "Please select a valid gender from the dropdown!")
        return False

    # if not phone_var.get().strip():
    #     messagebox.showerror("Error", "Phone is required!")
    #     return False
    # if not email_var.get().strip():
    #     messagebox.showerror("Error", "Email is required!")
    #     return False
       
    return True

def populate_fields(event):
    global original_record
    # Get the selected row
    selected = tree.selection()
    if selected:
        # Get the values from the selected row
        values = tree.item(selected[0], "values")
        original_record = values  # Store the original record data

        print(f"\nOriginal record: {original_record}")  # Debugging: Print original record

        patient_lookup_var.set("")  # Clear the Patient Lookup field
        
        # Populate the form field variables with the selected row's data
        user_id_var.set(values[1])
        patient_name_var.set(values[2])
        age_var.set(values[3])
        gender_var.set(values[4])
        phone_var.set(values[5])
        email_var.set(values[6])
        history_var.set(values[7])
        
        # Disable the Add/Edit buttons initially
        add_button.config(state="disabled")
        edit_button.config(state="disabled")


def check_data_changed(*args):
    global original_record

    # Check if original_record is None (no record selected)
    if not original_record:
        return
    
    # Compare the form data with the original record
    if (user_id_var.get() == original_record[1] and
        patient_name_var.get() == original_record[2] and
        age_var.get() == original_record[3] and
        gender_var.get() == original_record[4] and
        phone_var.get() == original_record[5] and
        email_var.get() == original_record[6] and
        history_var.get() == original_record[7]):
        add_button.config(state="disabled")  # Disable Add button if data hasn't changed
        edit_button.config(state="disabled")  # Disable Edit button if data hasn't changed

    elif user_id_var.get() != original_record[1]:
        add_button.config(state="normal")  # Enable Add button
        edit_button.config(state="disabled")  # Disable Edit button if User ID changes

    # elif (user_id_var.get() != original_record[1] or patient_name_var.get() != original_record[2]):
    #     add_button.config(state="normal")  # Enable Add button
    #     edit_button.config(state="disabled")  # Disable Edit button if User ID changes

    else:
        add_button.config(state="normal")  # Enable Add button if data changes
        edit_button.config(state="normal") # Enable Edit button if data changes


def search_patients():
    query = search_var.get().strip().lower()
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE LOWER(patient_name) LIKE ?", (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Clear the search field after searching
    # search_var.set("")


# Function to export data to CSV
def export_data():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    
    with open("patients_export.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "User ID", "Patient Name", "Age", "Gender", "Phone", "Email", "Medical History"])
        writer.writerows(rows)
    
    messagebox.showinfo("Success", "Data exported to 'patients_export.csv'!")










# Tkinter UI Setup


# Create the main window and set its title and size
# patients_database() # Call the database setup function to create the database and tables
root = tk.Tk()
root.title("Patient Service Screen")
root.geometry("1200x600")

# Input variables for the form fields
# These variables will hold the data entered in the input fields
user_id_var = tk.StringVar()
patient_lookup_var = tk.StringVar()
patient_name_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
history_var = tk.StringVar()

# Bind the input fields to the check_data_changed function to monitor changes
user_id_var.trace_add("write", check_data_changed)
patient_name_var.trace_add("write", check_data_changed)
# patient_name_var.trace("w", check_data_changed)
age_var.trace("w", check_data_changed)
gender_var.trace("w", check_data_changed)
phone_var.trace("w", check_data_changed)
email_var.trace("w", check_data_changed)
history_var.trace("w", check_data_changed)

# Declare add_button and edit_button as global to access them in other functions
global add_button
global edit_button

# Declare original_record as global to access it in other functions
# This variable will hold the original record data when a patient is selected from the Treeview
# It will be used to compare with the current input data to determine if changes have been made.
global original_record 


# Initialize original_record to None
original_record = () # Initialize original_record to None


# Create frames for better organization of the UI elements
# Each frame will hold specific UI elements like input fields, buttons, and the Treeview
input_frame = tk.Frame(root, padx=20, pady=5)
input_frame.grid(row=0, column=0, columnspan=2)

search_frame = tk.Frame(root, padx=20, pady=5)
search_frame.grid(row=1, column=3, columnspan=2)

dataview_frame = tk.Frame(root, padx=20, pady=5)
dataview_frame.grid(row=2, column=0, columnspan=4)

button_frame = tk.Frame(root, padx=20, pady=5)
button_frame.grid(row=3, column=0, columnspan=4)


search_var = tk.StringVar()
tk.Label(search_frame, text="Search:").grid(row=0, column=0, sticky="e", padx=0, pady=0)
tk.Entry(search_frame, textvariable=search_var, width=24).grid(row=0, column=1, sticky="", padx=10, pady=0)

tk.Button(search_frame, text=" GO ", command=search_patients, width=7).grid(row=0, column=2, sticky="e", padx=0, pady=0)

tk.Button(search_frame, text="Clear Search", command=load_patients).grid(row=0, column=3, sticky="e", padx=0, pady=0)

# tk.Button(search_frame, text="Refresh", command=load_patients).grid(row=0, column=4)





tk.Label(input_frame, text="Patient Name to be stored").grid(row=0, column=2, pady=5, sticky="e")
patient_name_entry = tk.Entry(input_frame, textvariable=patient_name_var, width=30)
patient_name_entry.grid(row=0, column=3, pady=5, sticky="w")





# ttk.Label(input_frame, text="User ID").grid(row=1, column=0, pady=5, sticky="w")
# # Create an Entry widget for the User ID entry
# # user_id_entry = ttk.Entry(input_frame, textvariable=user_id_var, show="*")
# user_id_entry = ttk.Entry(input_frame, textvariable=user_id_var, state="") # Set the state to "readonly" to prevent direct editing
# user_id_entry.grid(row=1, column=1, pady=5, sticky="w")
# # Set the width of the entry box
# user_id_entry.config(width=10)




ttk.Label(input_frame, text="Patient Lookup").grid(row=0, column=0, pady=5, sticky="w")
# AutocompleteEntry for user search
# patient_lookup_entry = AutocompleteEntry(input_frame, textvariable=patient_lookup_var, patient_id_box=user_id_entry)
patient_lookup_entry = AutocompleteEntry(
        input_frame,
        textvariable=patient_lookup_var,
        # user_id_box=user_id_entry,  # Pass the User ID entry box
        user_id_var=user_id_var,  # Pass the User ID variable
        # patient_id_box=patient_id_entry
        patient_name_box=patient_name_entry,  # Pass the Patient Name entry box
    )
# Set the width of the entry box
patient_lookup_entry.config(width=30)
# Place the entry widget in the grid layout
patient_lookup_entry.grid(row=0, column=1, pady=5, sticky="w")

# # Fetch Users' IDs and names for Autocomplete from the database
# patient_data_var = fetch_user_info()  # Returns [(ID, Name), ...]
# # Set suggestions for the autocomplete entry
# patient_lookup_entry.set_suggestions(patient_data_var)  # Set patient name suggestions










tk.Label(input_frame, text="Age").grid(row=2, column=0, pady=5, sticky="w")
tk.Entry(input_frame, textvariable=age_var, width=30).grid(row=2, column=1, pady=5, sticky="w")


# tk.Label(input_frame, text="Gender").grid(row=3, column=0)

# # Options for the dropdown
# gender_options = ["Male", "Female", "Other"]
# gender_var.set("Select Gender")  # Set the default value

# # Create a dropdown menu for gender
# gender_dropdown = tk.OptionMenu(input_frame, gender_var, *gender_options)
# gender_dropdown.grid(row=3, column=1)







ttk.Label(input_frame, text="Gender").grid(row=3, column=0, pady=5, sticky="w")

# Options for the dropdown
gender_options = ["Male", "Female", "Other"]

gender_dropdown = ttk.Combobox(input_frame, textvariable=gender_var, values=gender_options, state="readonly")
gender_dropdown.grid(row=3, column=1, pady=5, sticky="w")
gender_dropdown.set("Select Gender")  # Set the default value
gender_dropdown.config(width=22)  # Set the width of the dropdown menu







tk.Label(input_frame, text="Phone").grid(row=4, column=0, pady=5, sticky="w")
tk.Entry(input_frame, textvariable=phone_var, width=30).grid(row=4, column=1, pady=5, sticky="w")

tk.Label(input_frame, text="Email").grid(row=5, column=0, pady=5, sticky="w")
tk.Entry(input_frame, textvariable=email_var, width=30).grid(row=5, column=1, pady=5, sticky="w")

tk.Label(input_frame, text="Medical History").grid(row=6, column=0, pady=5, sticky="w")
tk.Entry(input_frame, textvariable=history_var, width=30).grid(row=6, column=1, pady=5, sticky="w")



# Treeview to display patients
tree = ttk.Treeview(dataview_frame, columns=("ID", "UserID", "Name", "Age", "Gender", "Phone", "Email", "MedicalHistory"), show="headings")
tree.heading("ID", text="ID")
tree.heading("UserID", text="User ID")
tree.heading("Name", text="Patient Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.heading("MedicalHistory", text="Medical History")
tree.grid(row=7, column=0, columnspan=5, sticky="nsew")
tree.column("ID", width=50) # Set width of ID column
tree.column("UserID", width=60) # Set width of User ID column
tree.column("Age", width=60) # Set width of User ID column
tree.column("Gender", width=70) # Set width of User ID column
tree.column("Phone", width=180) # Set width of User ID column

# Binding the Treeview selection event to the populate_fields() function
tree.bind("<<TreeviewSelect>>", populate_fields)


style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
style.map("Treeview", background=[("selected", "#347083")])
style.map("Treeview.Heading", background=[("active", "#347083")])




# Buttons for CRUD operations
# These buttons will trigger the respective functions for adding, editing, deleting, and clearing patient records
add_button = tk.Button(button_frame, text="Add Patient", command=add_patient)
add_button.grid(row=0, column=0)
edit_button = tk.Button(button_frame, text="Edit Patient", command=edit_patient)
edit_button.grid(row=0, column=1)
tk.Button(button_frame, text="Delete Patient", command=delete_patient).grid(row=0, column=2)
tk.Button(button_frame, text="Clear Fields", command=clear_fields).grid(row=0, column=3)

tk.Button(button_frame, text="Export Data", command=export_data).grid(row=0, column=4)
tk.Button(button_frame, text="Exit System", command=root.quit).grid(row=0, column=5)





# Set the default focus to the Patient Name entry field
patient_lookup_entry.focus()








if __name__ == "__main__":
    user_accounts_database() # Call the function to create the user accounts database
    patients_database() # Call the function to create the patients database
    print("\nTeam 2 Patients Database setup complete.\n")

    # Fetch Users' IDs and names for Autocomplete from the database
    patient_data_var = fetch_user_info()  # Returns [(ID, Name), ...]

    # Set suggestions for the autocomplete entry
    patient_lookup_entry.set_suggestions(patient_data_var)  # Set patient name suggestions

    load_patients()  # Load the patients into the Treeview when the application starts

    # root = tk.Tk()  # Create the main window
    # root.geometry("600x400")  # Set the window size    
    root.mainloop()  # Start the Tkinter main loop

    # root.destroy()  # Close the main window when done
    # root.quit()  # Exit the application