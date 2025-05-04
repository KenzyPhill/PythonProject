import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
from datetime import datetime

# import database_setup # Importing the database_setup module to set up the database and tables
from database_setup import user_accounts_database # Importing the user_accounts_database function from the database_setup module
from database_setup import patients_database # Importing the patients_database function from the database_setup module


# Function to fetch user IDs and names from the database
# This function connects to the SQLite database, retrieves user IDs and names from the users table, and returns them as a list of tuples.
# It also handles any database errors that may occur during the process.
# The fetched data is used to populate the autocomplete suggestions for the Patient Lookup field in the GUI.
# The function returns a list of tuples, where each tuple contains the user ID and the full name of a user.
def fetch_user_info():
    # import sqlite3
    
    conn = sqlite3.connect("healthcare.db")  # Connect to the database
    cursor = conn.cursor()
    
    try:
        # Query the users table to fetch IDs and names
        # cursor.execute("SELECT user_id, first_name, last_name, date_of_birth, gender FROM users")
        cursor.execute("SELECT user_id, first_name, last_name, date_of_birth, gender, address, phone, email  FROM users WHERE role = 'Patient'")
        rows = cursor.fetchall()
        
        if not rows:  # Check if rows are empty
            print("No users or IDs found in the database.")
        else:
            print(f"Fetched data: {rows}")  # Debugging: Print fetched data
        
        return [(row[0], row[1] + " " + row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]  # Return list of tuples (ID, Name, DOB, Gender, Address, Phone, Email)
    
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
    def __init__(self, master=None, textvariable=None, user_id_var=None, patient_name_box=None, date_of_birth_var=None, gender_var=None, address_var=None, phone_var=None, email_var=None, **kwargs):
        super().__init__(master, textvariable=textvariable, **kwargs)
        self.suggestions = []  # List to hold autocomplete suggestions
        self.user_id_var = user_id_var  # Reference to the User ID variable
        self.date_of_birth_var = date_of_birth_var  # Reference to the Date of Birth variable
        self.gender_var = gender_var  # Reference to the Gender variable
        self.address_var = address_var  # Reference to the Address variable
        self.phone_var = phone_var  # Reference to the Phone variable
        self.email_var = email_var # Reference to the Email variable
        
        
        # self.user_id_box = user_id_box  # Reference to the User ID entry box
        # self.patient_id_box = patient_id_box  # Reference to the Patient ID entry box
        self.patient_name_box = patient_name_box  # Reference to the User ID entry box
        self.bind("<KeyRelease>", self.update_suggestions)

    def set_suggestions(self, suggestions):
        # `suggestions` should be a list of tuples (ID, Name, DOB, Gender), e.g., [(9, 'Zaynah Uddin', '06/06/2002', 'Female'), (10, 'Jane Smith', '18/08/1971', 'Non-binary')]
        self.suggestions = suggestions

    def update_suggestions(self, event=None):
        typed_text = self.get()
        if not typed_text:
            if hasattr(self, "listbox"):
                self.listbox.destroy()
            return

        # Filter suggestions based on typed text
        matches = [(uid, name, dob, gender, address, phone, email) for uid, name, dob, gender, address, phone, email in self.suggestions if typed_text.lower() in name.lower()]

        if hasattr(self, "listbox"):
            self.listbox.destroy()

        if matches:
            self.listbox = tk.Listbox(self.master, height=len(matches), width=self.winfo_width())
            self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())            
            self.listbox.bind("<<ListboxSelect>>", self.select_suggestion)

            # Insert matches with IDs and names into the Listbox
            for uid, name, dob, gender, address, phone, email in matches:
                # self.listbox.insert(tk.END, f"{uid} - {name}")
                self.listbox.insert(tk.END, f"{uid} - {name} - {dob} - {gender} - {address} - {phone} - {email}")

            # Place the listbox relative to the entry widget
            # self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

    def select_suggestion(self, event=None):
        if hasattr(self, "listbox"):
            selected = self.listbox.get(self.listbox.curselection())
            self.listbox.destroy()

            # Extract the ID and Name from the selected suggestion
            # uid, name = selected.split(" - ", 1)
            uid, name, dob, gender, address, phone, email = selected.split(" - ", 6)  # Split into ID, Name, DOB, and Gender
            uid = uid.strip()  # Remove leading/trailing whitespace
            name = name.strip()  # Remove leading/trailing whitespace

            # # Place the User ID in the User ID box
            # if self.user_id_box:
            #     self.user_id_box.delete(0, tk.END)
            #     self.user_id_box.insert(0, uid)

            # Place the User ID in the User ID var
            if self.user_id_var:
                self.user_id_var.set(uid)

            # Place the DOB in the DOB var
            if self.date_of_birth_var:
                self.date_of_birth_var.set(dob)

            # Place the Gender in the Gender var
            if self.gender_var:
                self.gender_var.set(gender)
            
            if self.address_var:
                self.address_var.set(address)

            if self.phone_var:
                self.phone_var.set(phone)

            if self.email_var:
                self.email_var.set(email)


            # # Place the Patient ID in the Patient ID box
            # if self.patient_id_box:
            #     self.patient_id_box.delete(0, tk.END)
            #     self.patient_id_box.insert(0, pid)


            # Place the User's Name in the Patient Name box
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

    # Check for duplicate User ID
    cursor.execute("SELECT COUNT(*) FROM patients WHERE user_id = ?", (user_id_var.get(),))
    duplicate_count = cursor.fetchone()[0]
    if duplicate_count > 0:
        messagebox.showerror("Error", "A patient with this User ID already exists!")
        conn.close()
        return

    # Insert new patient if no duplicate is found
    cursor.execute("INSERT INTO patients (user_id, patient_name, patient_dob, patient_gender, patient_address, patient_phone, patient_email, medical_history) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (user_id_var.get(), patient_name_var.get(), date_of_birth_var.get(), gender_var.get(), address_text.get("1.0", tk.END).strip(), phone_var.get(), email_var.get(), medical_history_text.get("1.0", tk.END).strip()))
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
# It also validates the input fields and checks for User ID integrity before updating the record in the database.
# If the User ID is changed, an error message is displayed and the record is not updated.
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
        SET user_id=?, patient_name=?, patient_dob=?, patient_gender=?, patient_address=?, patient_phone=?, patient_email=?, medical_history=?
        WHERE patient_id=?
    """, (user_id_var.get(), patient_name_var.get(), date_of_birth_var.get(), gender_var.get(), address_text.get("1.0", tk.END).strip(), phone_var.get(), email_var.get(), medical_history_text.get("1.0", tk.END).strip(), tree.item(selected[0])["values"][0]))
    conn.commit()
    conn.close()
    clear_fields()
    load_patients()
    messagebox.showinfo("Success", "Patient updated successfully!")


# Function to delete a selected patient record
# This function retrieves the selected record from the Treeview and displays a confirmation dialog before deleting it from the database.
# If the user confirms, the record is deleted and the Treeview is updated.
# If the user cancels the deletion, the record is not deleted.
# If no record is selected, a warning message is displayed.
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
    clear_fields()
    load_patients()
    messagebox.showinfo("Success", "Patient deleted successfully!")


# Function to clear all input fields
# This function resets all input fields to their default values, allowing the user to start fresh without any pre-filled data.
# It is called on demand or after adding, editing or deleting a patient record to ensure the form is empty for the next entry.
# The function also clears the original_record variable to reset the state of the form.
# It is important to note that the function does not clear the Treeview, which retains the displayed patient records.
def clear_fields():
    # Clear all input variables and entry fields
    # user_id_entry.delete(0, tk.END)
    # patient_lookup_entry.delete(0, tk.END)
    # patient_name_entry.delete(0, tk.END)

    user_id_var.set("")
    patient_lookup_var.set("")
    patient_name_var.set("")
    date_of_birth_var.set("")
    age_var.set("")
    gender_var.set("Select Gender")
    # address_var.set("")
    address_text.delete("1.0", tk.END)  # Clear previous text
    address_text.insert(tk.END, "")  # Insert empty string to clear the text box
    phone_var.set("")
    email_var.set("")
    # history_var.set("")
    medical_history_text.delete("1.0", tk.END)  # Clear previous text
    medical_history_text.insert(tk.END, "")  # Insert empty string to clear the text box

    # Clear the Treeview selection
    tree.selection_remove(tree.selection())

    global original_record
    original_record = ()  # Reset the original record variable
    add_button.configure(state="normal")  # Enable Add button


# Function to validate fields before adding or editing a patient
# This function checks if the input fields are filled correctly and shows error messages if not.
def validate_fields():
    if not patient_name_var.get().strip():
        messagebox.showerror("Error", "Name is required!")
        return False
    if not user_id_var.get().strip():
        messagebox.showerror("Error", "ID is required!")
        return False
    if not date_of_birth_var.get().strip() or date_of_birth_var.get() == "Date format: dd/mm/yyyy":
        messagebox.showerror("Error", "Date of Birth is required!")
        return False
    
        
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
        date_of_birth_var.set(values[3])
        gender_var.set(values[4])
        # address_var.set(values[5])
        address_text.delete("1.0", tk.END)  # Clear previous text
        address_text.insert(tk.END, values[5])  # Insert new address
        phone_var.set(values[6])
        email_var.set(values[7])
        # history_var.set(values[8])
        medical_history_text.delete("1.0", tk.END)  # Clear previous text
        medical_history_text.insert(tk.END, values[8])  # Insert new medical history
        
        # Disable the Add/Edit buttons initially
        add_button.configure(state="disabled")
        edit_button.configure(state="disabled")



# def populate_fields(event):
#     global original_record
#     # Get the selected row
#     selected = tree.selection()
#     if selected:

#         # patient_id = tree.item(selected[0])["values"][0]  # Get the patient_id from the selected row

#         conn = sqlite3.connect("healthcare.db")
#         cursor = conn.cursor()
#         cursor.execute("""
#         SELECT * FROM patients WHERE patient_id=?
#         """, (tree.item(selected[0])["values"][0],)
#         )
#         values = cursor.fetchone()
#         original_record = values  # Store the original record data

#         conn.close()

#         print(f"\nOriginal record: {original_record}")  # Debugging: Print original record

#         patient_lookup_var.set("")  # Clear the Patient Lookup field
        
#         # Populate the form field variables with the selected patient's data retrieved from the database rather than the Treeview
#         user_id_var.set(values[1])
#         patient_name_var.set(values[2])
#         date_of_birth_var.set(values[3])
#         gender_var.set(values[4])
#         # address_var.set(values[5])
#         address_text.delete("1.0", tk.END)  # Clear previous text
#         address_text.insert(tk.END, values[5])  # Insert new address

#         phone_var.set(values[6])
#         email_var.set(values[7])
#         # history_var.set(values[8])
#         medical_history_text.delete("1.0", tk.END)  # Clear previous text
#         medical_history_text.insert(tk.END, values[8])  # Insert new medical history
        
#         # Disable the Add/Edit buttons initially
#         add_button.configure(state="disabled")
#         edit_button.configure(state="disabled")




def check_data_changed(*args):
    global original_record

    # Check if original_record is None (no record selected)
    if not original_record:
        return
    
    # Compare the form data with the original record
    if (user_id_var.get().strip() == original_record[1].strip() and
        patient_name_var.get() == original_record[2] and
        date_of_birth_var.get() == original_record[3] and
        gender_var.get() == original_record[4] and
        # address_var.get() == original_record[5] and
        address_text.get("1.0", tk.END).strip() == str(original_record[5]).strip() and  # Compare with the text box content

        phone_var.get() == original_record[6] and
        email_var.get() == original_record[7] and
        # history_var.get() == original_record[8]
        medical_history_text.get("1.0", tk.END).strip() == str(original_record[8]).strip()
        ):  # Compare with the text box content
        
        add_button.configure(state="disabled")  # Disable Add button if data hasn't changed
        edit_button.configure(state="disabled")  # Disable Edit button if data hasn't changed

    elif user_id_var.get() != original_record[1]:
        add_button.configure(state="normal")  # Enable Add button
        edit_button.configure(state="disabled")  # Disable Edit button if User ID changes

    # elif (user_id_var.get() != original_record[1] or patient_name_var.get() != original_record[2]):
    #     add_button.configure(state="normal")  # Enable Add button
    #     edit_button.configure(state="disabled")  # Disable Edit button if User ID changes

    else:
        add_button.configure(state="normal")  # Enable Add button if data changes
        edit_button.configure(state="normal") # Enable Edit button if data changes


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








###########################################################################

# Tkinter UI Setup


# Create the main window and set its title and size
# patients_database() # Call the database setup function to create the database and tables
root = tk.Tk()
root.title("Patient Service Screen")
# root.wm_iconbitmap(r'icons\icon.ico')
root.geometry("1200x720")
# root.resizable(False, False)  # Disable resizing of the window
root.configure(bg="lightblue")  # Set the background color of the main window
# root.iconbitmap("icon.ico")  # Set the window icon






style = ttk.Style()
# style.theme_use("default")  # Modern theme
style.theme_use("clam")  # Modern theme
# style.theme_use("alt")  # Modern theme
# style.theme_use("classic")  # Modern theme
# style.theme_use("vista")  # Modern theme
# style.theme_use("xpnative")  # Modern theme
# style.configure("Frame", background="lightblue")
# style.configure("Label", background="lightblue", font=("Arial", 11), padding=15)
# style.configure("Button", background="lightgrey", font=("Arial", 11), padding=5)
style.configure("TButton", background="lightgrey", font=("Helvetica", 10), padding=5)

# style.configure("Combobox", background="lightgrey", font=("Arial", 11), padding=5)
# style.configure("Entry", font=("Arial", 20), background="lightgrey", padding=0)
style.configure("Treeview", font=("Arial", 10), rowheight=34, padding=0)
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
# style.map("Button", background=[("active", "lightgrey")])  # Change button color on hover
# style.map("Entry", background=[("focus", "white")])  # Change entry color on focus
# style.map("Combobox", background=[("focus", "white")])  # Change combobox color on focus
# style.map("Treeview", background=[("selected", "#347083")])  # Change treeview color on selection
# style.map("Treeview.Heading", background=[("active", "#347083")])  # Change treeview heading color on hover
# style.map("Treeview.Heading", foreground=[("active", "white")])
# style.map("Treeview.Heading", foreground=[("selected", "white")])






# Input variables for the form fields
# These variables will hold the data entered in the input fields
user_id_var = tk.StringVar()
patient_lookup_var = tk.StringVar()
patient_name_var = tk.StringVar()
date_of_birth_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
address_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
history_var = tk.StringVar()

# Bind the input fields to the check_data_changed function to monitor changes
user_id_var.trace_add("write", check_data_changed)
patient_name_var.trace_add("write", check_data_changed)
date_of_birth_var.trace_add("write", check_data_changed)
gender_var.trace_add("write", check_data_changed)
phone_var.trace_add("write", check_data_changed)
email_var.trace_add("write", check_data_changed)

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
input_frame = tk.Frame(root, padx=30, pady=15)
input_frame.grid(row=0, column=0, columnspan=3)
input_frame.configure(bg="lightblue")

search_frame = tk.Frame(root, padx=30, pady=5)
search_frame.grid(row=1, column=2, columnspan=5)
search_frame.configure(bg="lightblue")

datablock_frame = tk.Frame(root, padx=20, pady=5)
datablock_frame.grid(row=2, column=0, columnspan=5) 
datablock_frame.configure(bg="lightblue")

dataview_frame = tk.Frame(datablock_frame, padx=0, pady=0, bg="lightgrey", relief="ridge", bd=1)
dataview_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")



button_frame = tk.Frame(root, padx=20, pady=12)
button_frame.grid(row=3, column=0, sticky="ew", columnspan=5)
button_frame.configure(bg="lightblue")


search_var = tk.StringVar()
tk.Label(search_frame, text="Search:", background="lightblue", font=("Arial", 11)).grid(row=0, column=0, sticky="e", padx=0, pady=0)
tk.Entry(search_frame, textvariable=search_var, width=24, font=("Arial", 11)).grid(row=0, column=1, sticky="", padx=10, pady=0)

tk.Button(search_frame, text=" GO ", command=search_patients, width=7, font=("Arial", 9, "")).grid(row=0, column=2, sticky="e", padx=0, pady=0)

tk.Button(search_frame, text="  Clear  ", command=load_patients, font=("Arial", 9, "")).grid(row=0, column=3, sticky="e", padx=0, pady=0)

# tk.Button(search_frame, text="Refresh", command=load_patients).grid(row=0, column=4)





tk.Label(input_frame, text="Patient Name", background="lightblue", font=("Arial", 11)).grid(row=0, column=2, padx=0, pady=5, sticky="e")
patient_name_entry = tk.Entry(input_frame, textvariable=patient_name_var, width=26, font=("Arial", 11))
patient_name_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")





# ttk.Label(input_frame, text="User ID").grid(row=1, column=0, pady=5, sticky="w")
# # Create an Entry widget for the User ID entry
# # user_id_entry = ttk.Entry(input_frame, textvariable=user_id_var, show="*")
# user_id_entry = ttk.Entry(input_frame, textvariable=user_id_var, state="") # Set the state to "readonly" to prevent direct editing
# user_id_entry.grid(row=1, column=1, pady=5, sticky="w")
# # Set the width of the entry box
# user_id_entry.configure(width=10)




tk.Label(input_frame, text="Patient Lookup", background="lightblue", font=("Arial", 11)).grid(row=0, column=0, pady=5, sticky="w")
# AutocompleteEntry for user search
# patient_lookup_entry = AutocompleteEntry(input_frame, textvariable=patient_lookup_var, patient_id_box=user_id_entry)
patient_lookup_entry = AutocompleteEntry(
        input_frame,
        textvariable=patient_lookup_var,
        # user_id_box=user_id_entry,  # Pass the User ID entry box
        user_id_var=user_id_var,  # Pass the User ID variable
        date_of_birth_var=date_of_birth_var,  # Pass the Date of Birth variable
        gender_var=gender_var,
        address_var=address_var,
        phone_var=phone_var,
        email_var=email_var,
        # patient_id_box=patient_id_entry
        patient_name_box=patient_name_entry,  # Pass the Patient Name entry box
    )
# Set the width of the entry box
patient_lookup_entry.configure(width=26, font=("Arial", 11))
# Place the entry widget in the grid layout
patient_lookup_entry.grid(row=0, column=1, pady=5, sticky="w")


########## MOVED TO IF MAIN BELOW ##########
# # Fetch Users' IDs and names for Autocomplete from the database
# patient_data_var = fetch_user_info()  # Returns [(ID, Name), ...]
# # Set suggestions for the autocomplete entry
# patient_lookup_entry.set_suggestions(patient_data_var)  # Set patient name suggestions






tk.Label(input_frame, text="Date of Birth", background="lightblue", font=("Arial", 11)).grid(row=2, column=0, pady=5, sticky="w")
date_of_birth_entry = tk.Entry(input_frame, textvariable=date_of_birth_var, width=26, font=("Arial", 11)) 
date_of_birth_entry.grid(row=2, column=1, pady=5, sticky="w")




# Function to calculate age
def calculate_age():
    """Calculates age from entered date of birth."""
    try:
        dob = datetime.strptime(date_of_birth_var.get(), "%d/%m/%Y")  # Convert string to date object
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_var.set(str(age))  # Store age as a StringVar
    except ValueError:
        age_var.set("Date format: dd/mm/yyyy")  # Handles incorrect input


tk.Label(input_frame, text="Age", background="lightblue", font=("Arial", 11)).grid(row=2, column=2, padx=0, pady=5, sticky="e")
tk.Entry(input_frame, textvariable=age_var, width=26, font=("Arial", 11), background="lightblue").grid(row=2, column=3, padx=10, pady=5, sticky="w")

# Bind the Date of Birth entry to calculate age when the date is entered
# date_of_birth_entry.bind("<FocusOut>", lambda event: calculate_age())  # Calculate age when focus is lost

# Bind calculate_age to date_of_birth_var updates
date_of_birth_var.trace_add("write", lambda *args: calculate_age())  # Calculate age when date of birth is entered










# tk.Label(input_frame, text="Gender").grid(row=3, column=0)

# # Options for the dropdown
# gender_options = ["Male", "Female", "Other"]
# gender_var.set("Select Gender")  # Set the default value

# # Create a dropdown menu for gender
# gender_dropdown = tk.OptionMenu(input_frame, gender_var, *gender_options)
# gender_dropdown.grid(row=3, column=1)







tk.Label(input_frame, text="Gender", background="lightblue", font=("Arial", 11)).grid(row=3, column=0, pady=5, sticky="w")

# Options for the dropdown
gender_options = ["Male", "Female", "Non-binary", "Other"]

gender_dropdown = ttk.Combobox(input_frame, textvariable=gender_var, values=gender_options, state="readonly")
gender_dropdown.grid(row=3, column=1, pady=5, sticky="w")
gender_dropdown.set("Select Gender")  # Set the default value
gender_dropdown.configure(width=22, font=("Arial", 10))  # Set the width of the dropdown menu







# tk.Label(input_frame, text="Address", background="lightblue").grid(row=4, column=0, pady=5, sticky="w")
# tk.Entry(input_frame, textvariable=address_var, width=75).grid(row=4, column=1, columnspan=3, pady=5, sticky="w")

tk.Label(input_frame, text="Address", background="lightblue", font=("Arial", 11)).grid(row=4, column=0, pady=5, sticky="w")
# Multi-Line Text Box for Address
address_text = tk.Text(input_frame, width=26, height=3, font=("Arial", 11))  # Wider & taller text box
address_text.grid(row=4, column=1, columnspan=3, pady=5, sticky="w")
# address_text.insert(tk.END, "")  # Insert empty string to clear the text box
# address_text.bind("<FocusIn>", lambda event: address_text.delete("1.0", tk.END))  # Clear text on focus
# address_text.bind("<FocusOut>", lambda event: address_text.insert(tk.END, ""))  # Insert empty string to clear the text box
# address_text.bind("<KeyRelease>", lambda event: address_var.set(address_text.get("1.0", tk.END).strip()))  # Update address_var on key release
address_text.bind("<KeyRelease>", lambda event: check_data_changed())  # Check for data changes on key release

tk.Label(input_frame, text="Phone", background="lightblue", font=("Arial", 11)).grid(row=5, column=0, pady=5, sticky="w")
tk.Entry(input_frame, textvariable=phone_var, width=26, font=("Arial", 11)).grid(row=5, column=1, pady=5, sticky="w")

tk.Label(input_frame, text="Email", background="lightblue", font=("Arial", 11)).grid(row=5, column=2, padx=0, pady=5, sticky="e")
tk.Entry(input_frame, textvariable=email_var, width=26, font=("Arial", 11)).grid(row=5, column=3, padx=10, pady=5, sticky="w")

# tk.Label(input_frame, text="Medical History", background="lightblue").grid(row=6, column=0, pady=5, sticky="w")
# tk.Entry(input_frame, textvariable=history_var, width=26).grid(row=6, column=1, pady=5, sticky="w")

tk.Label(input_frame, text="Medical History", background="lightblue", font=("Arial", 11)).grid(row=0, column=4, pady=0, sticky="w")
# Multi-Line Text Box for Medical History
medical_history_text = tk.Text(input_frame, width=50, height=9, font=("Arial", 11))  # Wider & taller input field
medical_history_text.grid(row=1, column=4, columnspan=4, rowspan=5, pady=0, sticky="nsew")
medical_history_text.bind("<KeyRelease>", lambda event: check_data_changed())  # Check for data changes on key release
vert_scroll = tk.Scrollbar(input_frame, command=medical_history_text.yview)
vert_scroll.grid(row=1, column=9, rowspan=5, sticky="nsew")  # Place scrollbar to the right of text box
medical_history_text.config(yscrollcommand=vert_scroll.set)  # Link vertical scrollbar



# Treeview to display patients
# tree = ttk.Treeview(dataview_frame, columns=("ID", "UserID", "Name", "DOB", "Gender", "Address", "Phone", "Email", "MedicalHistory"), show="headings")
tree = ttk.Treeview(dataview_frame, columns=("ID", "UserID", "Name", "DOB", "Gender", "Address", "Phone", "Email"), show="headings")
# tree = ttk.Treeview(dataview_frame, columns=("ID", "UserID", "Name", "DOB", "Gender", "Address", "Phone"), show="headings")

tree.heading("ID", text="PID")
tree.heading("UserID", text="UID")
tree.heading("Name", text="Patient Name")
tree.heading("DOB", text="DOB")
tree.heading("Gender", text="Gender")
tree.heading("Address", text="Address")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
# tree.heading("MedicalHistory", text="Medical History")
tree.grid(row=0, column=0, columnspan=6, sticky="nsew")
tree.column("ID", width=60, anchor="center") # Set width of ID column
tree.column("UserID", width=60, anchor="center") # Set width of User ID column
tree.column("Name", width=180) # Set width of Name column
tree.column("DOB", width=130) # Set width of User ID column
tree.column("Gender", width=140) # Set width of User ID column
tree.column("Address", width=200)  # Set width of Address column
tree.column("Phone", width=120) # Set width of User ID column
tree.column("Email", width=260) # Set width of User ID column
# tree.column("MedicalHistory", width=180) # Set width of User ID column


# Binding the Treeview selection event to the populate_fields() function
tree.bind("<<TreeviewSelect>>", populate_fields)  # Populate fields when an item is selected

# tree.bind("<Double-1>", lambda event: some_function())  # Double-click to perform some action

tree.bind("<Delete>", lambda event: delete_patient())  # Delete patient with Delete key




# Add vertical scrollbar
vsb = ttk.Scrollbar(dataview_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# # Add horizontal scrollbar
# hsb = ttk.Scrollbar(dataview_frame, orient="horizontal", command=tree.xview)
# tree.configure(xscrollcommand=hsb.set)

# Positioning widgets
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
# hsb.grid(row=1, column=0, sticky="ew")

# Configure frame to expand
dataview_frame.columnconfigure(0, weight=1) # Allow the Treeview to expand horizontally
dataview_frame.rowconfigure(0, weight=1) # Allow the Treeview to expand vertically



# Buttons for CRUD operations
# These buttons will trigger the respective functions for adding, editing, deleting, and clearing patient records
add_button = ttk.Button(button_frame, text=" Add Patient ", command=add_patient)
add_button.grid(row=0, column=0)
edit_button = ttk.Button(button_frame, text=" Edit Patient ", command=edit_patient)
edit_button.grid(row=0, column=1)
ttk.Button(button_frame, text=" Delete Patient ", command=delete_patient).grid(row=0, column=2)
ttk.Button(button_frame, text=" Clear Fields ", command=clear_fields).grid(row=0, column=3)

ttk.Button(button_frame, text=" Export Data ", command=export_data).grid(row=0, column=4)
ttk.Button(button_frame, text=" Exit System ", command=root.quit).grid(row=0, column=5)





# Set the default focus to the Patient Name entry field
patient_lookup_entry.focus()








if __name__ == "__main__":
    # user_accounts_database() # Call the function to create the user accounts database
    # patients_database() # Call the function to create the patients database
    print("\nTeam 2 Database setup for Patient Screen complete.\n")

    # Fetch Users' IDs and names for Autocomplete from the database
    patient_data_var = fetch_user_info()  # Returns [(ID, Name, DOB, Gender), ...]

    # Set suggestions for the autocomplete entry
    patient_lookup_entry.set_suggestions(patient_data_var)  # Set patient name suggestions

    load_patients()  # Load the patients into the Treeview when the application starts

    # root = tk.Tk()  # Create the main window
    # root.geometry("600x400")  # Set the window size    
    root.mainloop()  # Start the Tkinter main loop

    # root.destroy()  # Close the main window when done
    # root.quit()  # Exit the application