import tkinter as tk
from tkinter import ttk, messagebox
# from tkinter import messagebox
import sqlite3
from tkcalendar import Calendar
# import database_setup # Importing the database_setup module
from database_setup import patients_database # Importing the patients_database function from the database_setup module
from database_setup import appointments_database # Importing the appointments_database function from the database_setup module


# Global Variables
global edit_button  # Keep reference to the button to remove it later

global original_record  # Variable to store the original record data
original_record = None # Initialize to None

patient_id_var = None  # Initialize patient_id_var to None
patient_name_var = None  # Initialize patient_name_var to None
date_var = None  # Initialize date_var to None
time_var = None  # Initialize time_var to None
provider_var = None  # Initialize provider_var to None



# Function to fetch patient names and IDs from the database
# This function connects to the SQLite database and retrieves patient names and IDs from the patients table.
# It returns a list of tuples containing the patient ID and name.
# If there are no patients in the database, it returns an empty list.
# If there is a database error, it prints the error message and returns an empty list.
# This function is used to populate the autocomplete entry with patient names and IDs.
# It is called when the application starts to load the patient data into the autocomplete entry.
def fetch_patient_info():
    # import sqlite3
    
    conn = sqlite3.connect("healthcare.db")  # Connect to the database
    cursor = conn.cursor()
    
    try:
        # Query the patients table to fetch names and IDs
        cursor.execute("SELECT patient_id, patient_name FROM patients")
        rows = cursor.fetchall()
        
        if not rows:  # Check if rows are empty
            print("No patient names or IDs found in the database.")
        else:
            print(f"Fetched data: {rows}")  # Debugging: Print fetched data
        
        return [(row[0], row[1]) for row in rows]  # Return list of tuples (ID, Name)
    
    except sqlite3.Error as e:  # Handle database errors
        print(f"Database error: {e}")
        return []
    
    finally:
        conn.close()  # Ensure connection is closed






class AutocompleteEntry(ttk.Entry):
    def __init__(self, master=None, textvariable=None, patient_id_var=None, **kwargs):
        super().__init__(master, textvariable=textvariable, **kwargs)
        self.suggestions = []  # List to hold autocomplete suggestions
        # self.user_id_box = user_id_box  # Reference to the User ID entry box
        self.patient_id_var = patient_id_var  # Reference to the Patient ID entry box
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
            pid, name = selected.split(" - ", 1)

            # # Place the User ID in the User ID box
            # if self.user_id_box:
            #     self.user_id_box.delete(0, tk.END)
            #     self.user_id_box.insert(0, uid)

            # # Place the Patient ID in the Patient ID box
            # if self.patient_id_box:
            #     self.patient_id_box.delete(0, tk.END)
            #     self.patient_id_box.insert(0, pid)

            # Place the User ID in the User ID var
            if self.patient_id_var:
                self.patient_id_var.set(pid)

            # if self.email_var:
            #     self.email_var.set(email)

            # Update the Entry field with the full selection
            if self.master and self.master.winfo_exists():
                self.delete(0, tk.END)
                self.insert(0, name)

                self.icursor(tk.END)  # Move cursor to the end of the entry
                self.focus()  # Set focus back to the entry widget










# Functions for Appointment Scheduling
def load_appointments():
    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    rows = cursor.fetchall()
    conn.close()

    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)




def book_appointment():
    if not patient_id_var.get() or not patient_name_var.get() or not date_entry.get() or not time_var.get() or time_var.get() == "Select a time" or not provider_var.get() or provider_var.get() == "Select a provider":
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()

    # Check for conflicts in the database
    cursor.execute("""
    SELECT * FROM appointments WHERE patient_id=? AND appointment_date=? AND appointment_time=?
    """, (patient_id_var.get(), date_entry.get(), time_var.get())
    )
    conflict_patient = cursor.fetchone()

    cursor.execute("""
    SELECT * FROM appointments WHERE appointment_date=? AND appointment_time=? AND provider_name=?
    """, (date_entry.get(), time_var.get(), provider_var.get())
    )
    conflict_provider = cursor.fetchone()

    if conflict_patient:
        messagebox.showerror("Error", "This patient is already booked at this time!")
    elif conflict_provider:
        messagebox.showerror("Error", "This provider is already booked at this time!")
    else:
        cursor.execute("""
        INSERT INTO appointments (patient_id, patient_name, appointment_date, appointment_time, provider_name)
        VALUES (?, ?, ?, ?, ?)
        """, (patient_id_var.get(), patient_name_var.get(), date_entry.get(), time_var.get(), provider_var.get()))
        conn.commit()
        load_appointments()
        messagebox.showinfo("Success", "Appointment booked successfully!")
    conn.close()








def populate_fields(event):
    global original_record
    # Get the selected row
    selected = tree.selection()
    if selected:
        # Get the values from the selected row
        values = tree.item(selected[0], "values")
        original_record = values  # Store the original record data

        # Populate the form fields with the selected row's data
        patient_id_var.set(values[1])
        patient_name_var.set(values[2])
        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[3])
        time_var.set(values[4])
        provider_var.set(values[5])

      




# def edit_appointment():

#         # Destroy the update button after editing
#         update_appointment_button.destroy()

#     # Create an Update button temporarily
#     update_appointment_button = ttk.Button(frame_appointments, text="Update Appointment", command=update_appointment)
#     update_appointment_button.grid(row=4, column=2, pady=10)











def edit_appointment():

    def update_appointment():

        if not messagebox.askyesno("Confirmation", "Are you sure you want to update this appointment?"):
            return

        # conn = sqlite3.connect("healthcare.db")
        # cursor = conn.cursor()
        # Update the appointment in the database
        cursor.execute("""
        UPDATE appointments
        SET patient_id=?, patient_name=?, appointment_date=?, appointment_time=?, provider_name=?
        WHERE appointment_id=?
        """, (patient_id_var.get(), patient_name_var.get(), date_entry.get(), time_var.get(), provider_var.get(), tree.item(selected[0])["values"][0] ))
                    
        conn.commit()
        # conn.close()
        # Reload the appointments in the Treeview
        load_appointments()
        messagebox.showinfo("Success", "Appointment updated successfully!")
        # clear_fields() # Clear the fields after updating

    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select an appointment to edit.")
        return


    # Check if all fields are filled
    if not patient_id_var.get() or not patient_name_var.get() or not date_entry.get() or not time_var.get() or time_var.get() == "Select a time" or not provider_var.get() or provider_var.get() == "Select a provider":
        messagebox.showerror("Error", "All fields are required!")
        return

    # # Prevents allocating the selected appointment to a different Patient
    # if not patient_id_var.get() == original_record[1]:
    #     messagebox.showerror("Error", "Patient selection changed! Record was not updated.")
    #     return


    # Check for conflicts in the database
    if patient_id_var.get() == original_record[1] and date_entry.get() == original_record[3] and time_var.get() == original_record[4] and provider_var.get() == original_record[5]:
        messagebox.showerror("Error", "No changes made to the appointment!")
        return
    
    elif patient_id_var.get() == original_record[1] and date_entry.get() == original_record[3] and time_var.get() == original_record[4] and provider_var.get() != original_record[5]:
        # Check for conflicts with the new provider
        conn = sqlite3.connect("healthcare.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM appointments WHERE appointment_date=? AND appointment_time=? AND provider_name=?
        """, (date_entry.get(), time_var.get(), provider_var.get())
        )
        conflict_provider = cursor.fetchone()
        if conflict_provider:
            messagebox.showerror("Error", "This provider is not available at this time!")
            conn.close()
            # return
        else:
            # Update the appointment in the database
            update_appointment()
            conn.close()

    elif patient_id_var.get() != original_record[1] and date_entry.get() == original_record[3] and time_var.get() == original_record[4] and provider_var.get() == original_record[5]:
        # Check for conflicts with the new patient
        conn = sqlite3.connect("healthcare.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM appointments WHERE patient_id=? AND appointment_date=? AND appointment_time=?
        """, (patient_id_var.get(), date_entry.get(), time_var.get())
        )
        patient_conflict = cursor.fetchone()
        if patient_conflict:
            messagebox.showerror("Error", "This patient is already booked at this time!")
            conn.close()
            # return
        else:
            # Update the appointment in the database
            update_appointment()
            conn.close()

    else:
        conn = sqlite3.connect("healthcare.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM appointments WHERE patient_id=? AND appointment_date=? AND appointment_time=?
        """, (patient_id_var.get(), date_entry.get(), time_var.get())
        )
        patient_conflict = cursor.fetchone()

        cursor.execute("""
        SELECT * FROM appointments WHERE appointment_date=? AND appointment_time=? AND provider_name=?
        """, (date_entry.get(), time_var.get(), provider_var.get())
        )
        conflict_provider = cursor.fetchone()

        if patient_conflict:
            messagebox.showerror("Error", "This patient is already booked at this time!")
            conn.close()
            # return
        
        elif conflict_provider:
            messagebox.showerror("Error", "This provider is not available at this time!")
            conn.close()
            # return
        
        else:
            # Update the appointment in the database
            update_appointment()
            conn.close()





def delete_appointment():
    # Get the selected item
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "No appointment selected!")
        return

    # Confirmation dialog
    if not messagebox.askyesno("Confirmation", "Are you sure you want to delete this appointment?"):
        return

    conn = sqlite3.connect("healthcare.db")
    cursor = conn.cursor()
    # Delete the appointment from the database
    cursor.execute("DELETE FROM appointments WHERE appointment_id=?", (tree.item(selected[0])["values"][0],))
    conn.commit()
    conn.close()

    load_appointments()
    messagebox.showinfo("Success", "Appointment deleted successfully!")


def clear_fields():
    patient_name_var.set("")
    date_entry.delete(0, tk.END)
    time_var.set("")
    provider_var.set("")
    patient_id_var.set("")  # Clear the Patient ID entry


def show_calendar():
    calendar_window = tk.Toplevel(root)
    calendar_window.title("Select a Date")

    def select_date():
        selected_date = cal.get_date()
        date_entry.delete(0, tk.END)
        date_entry.insert(0, selected_date)
        calendar_window.destroy()

    cal = Calendar(calendar_window, selectmode='day', date_pattern='dd/mm/yyyy')
    cal.pack(pady=0, padx=0)
    ttk.Button(calendar_window, text="Select", command=select_date).pack(pady=5)





def calculate_bmi():
    try:
        weight = float(weight_var.get())
        height = float(height_var.get()) / 100  # Convert cm to meters
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            status = "Underweight"
        elif 18.5 <= bmi < 25:
            status = "Normal weight"
        elif 25 <= bmi < 30:
            status = "Overweight"
        else:
            status = "Obese"
        # Display the result in a message box
        messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f} ({status})")
    except ValueError:
        # Handle invalid input
        messagebox.showerror("Error", "Please enter valid weight and height.")

def check_bp():
    try:
        systolic = int(systolic_var.get())
        diastolic = int(diastolic_var.get())
        if systolic < 120 and diastolic < 80:
            status = "Normal"
        elif 120 <= systolic < 130 and diastolic < 80:
            status = "Elevated"
        elif 130 <= systolic < 140 or 80 <= diastolic < 90:
            status = "High Blood Pressure (Stage 1)"
        else:
            status = "High Blood Pressure (Stage 2)"
        messagebox.showinfo("Blood Pressure Result", f"Your blood pressure is {systolic}/{diastolic} mmHg ({status})")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for blood pressure.")




# def show_dropdown():
#     typed_text = entry.get()
#     if hasattr(entry, "listbox"):
#         entry.listbox.destroy()  # Destroy existing dropdown if any

#     # Example items for dropdown
#     items = ["Option 1", "Option 2", "Option 3", "Option 4"]
#     matches = [item for item in items if typed_text.lower() in item.lower()]

#     if matches:
#         entry.listbox = tk.Listbox(root, height=len(matches))
#         for match in matches:
#             entry.listbox.insert(tk.END, match)

#         # Place the dropdown directly below and touching the text box
#         x = entry.winfo_x()
#         y = entry.winfo_y() + entry.winfo_height()
#         entry.listbox.place(x=x, y=y)





#####################################################################################

# # Tkinter UI Setup

# appointments_database()
root = tk.Tk()  # Create the main window
# root.geometry("600x400")  # Set the window size
root.title("Appointment Screen")  # Set the window title
root.configure(bg="lightblue")  # Set the background color of the main window
# root.iconbitmap("icon.ico")  # Set the window icon



style = ttk.Style()
style.theme_use("clam")  # Modern theme
style.configure("TFrame", background="lightblue")
style.configure("TLabel", background="lightblue", font=("Helvetica", 10))
style.configure("TButton", background="lightgrey", font=("Helvetica", 10), padding=5)
style.configure("TCombobox", background="lightgrey", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))
style.configure("Treeview", font=("Helvetica", 11), rowheight=30)
style.configure("TTreeview.Heading", font=("Helvetica", 10, "bold"))
style.map("TButton", background=[("active", "lightgrey")])  # Change button color on hover
style.map("TEntry", background=[("focus", "white")])  # Change entry color on focus
style.map("TCombobox", background=[("focus", "white")])  # Change combobox color on focus
style.map("TTreeview", background=[("selected", "#347083")])  # Change treeview color on selection
style.map("TTreeview.Heading", background=[("active", "#347083")])  # Change treeview heading color on hover
style.map("TTreeview.Heading", foreground=[("active", "white")])
style.map("TTreeview.Heading", foreground=[("selected", "white")])



# user_id_var = tk.StringVar()  # StringVar to hold the user ID
patient_id_var = tk.StringVar()  # StringVar to hold the patient ID
patient_name_var = tk.StringVar()  # StringVar to hold the patient name
date_var = tk.StringVar()  # StringVar to hold the date
time_var = tk.StringVar()  # StringVar to hold the time
provider_var = tk.StringVar()  # StringVar to hold the provider name

weight_var = tk.StringVar()  # StringVar to hold the weight
height_var = tk.StringVar()  # StringVar to hold the height
systolic_var = tk.StringVar()  # StringVar to hold the systolic blood pressure
diastolic_var = tk.StringVar()  # StringVar to hold the diastolic blood pressure




# Appointment Form Frame
# This frame will hold the appointment form widgets
frame_appointments = tk.Frame(root, padx=20, pady=5)
frame_appointments.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
frame_appointments.configure(bg="lightblue")  # Set the background color of the frame

# Data Area Frame
# This frame will hold the Treeview and other data-related widgets columnspan=6, 
frame_dataarea = tk.Frame(root, padx=20, pady=0)
frame_dataarea.grid(row=1, column=0, sticky="ew", padx=10, pady=0)
frame_dataarea.configure(bg="lightblue") # Set the background color of the frame

# Buttons Frame
# This frame will hold the buttons for booking, clearing, and editing appointments
frame_buttons = tk.Frame(root, padx=20, pady=5)
frame_buttons.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
frame_buttons.configure(bg="lightblue")  # Set the background color of the frame



# label for the patient ID entry
ttk.Label(frame_appointments, text="Patient ID", font=("Arial", 11)).grid(row=0, column=4, pady=5)
patient_id_entry = ttk.Entry(frame_appointments, textvariable=patient_id_var)
patient_id_entry.configure(state="readonly")  # Make the entry read-only
patient_id_entry.grid(row=0, column=5, pady=5)


# Label for the patient name entry
ttk.Label(frame_appointments, text="Patient Name").grid(row=0, column=0, pady=5, sticky="w")
# patient_name_entry = ttk.Entry(frame_appointments, textvariable=patient_name_var)
# patient_name_entry.grid(row=1, column=3, padx=5)

# AutocompleteEntry for patient search
# patient_entry = AutocompleteEntry(frame_appointments, textvariable=patient_name_var, patient_id_box=patient_id_entry)
patient_entry = AutocompleteEntry(
        frame_appointments,
        textvariable=patient_name_var,
        # user_id_box=user_id_entry,
        # patient_id_box=patient_id_entry
        patient_id_var=patient_id_var
    )
# Set the width of the entry box
patient_entry.configure(width=30)
# Place the entry widget in the grid layout
patient_entry.grid(row=0, column=1, pady=5, sticky="w")


ttk.Label(frame_appointments, text="Date").grid(row=1, column=0, pady=5, sticky="w")
date_entry = ttk.Entry(frame_appointments, width=20, textvariable=date_var)
date_entry.grid(row=1, column=1, pady=5, sticky="w")
ttk.Button(frame_appointments, text="Pick a Date", command=show_calendar).grid(row=1, column=2)


# Predefined time slots
time_slots = ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"]


ttk.Label(frame_appointments, text="Time Slot").grid(row=2, column=0, pady=5, sticky="w")
time_var = tk.StringVar()
time_dropdown = ttk.Combobox(frame_appointments, textvariable=time_var, values=time_slots, state="readonly")
time_dropdown.grid(row=2, column=1, pady=5, sticky="w")
time_dropdown.set("Select a time")



# Predefined provider names
provider_names = ["Dr. John Smith", "Dr. Emily Brown", "Dr. Michael Lee", "Dr. Sarah Davis", "Dr. David Wilson"]

# Update UI to include dropdown menu for provider names
ttk.Label(frame_appointments, text="Provider Name").grid(row=3, column=0, pady=5, sticky="w")
provider_var = tk.StringVar()
provider_dropdown = ttk.Combobox(frame_appointments, textvariable=provider_var, values=provider_names, state="readonly")
provider_dropdown.grid(row=3, column=1, pady=5, sticky="w")
provider_dropdown.set("Select a provider")



ttk.Button(frame_buttons, text="Book Appointment", command=book_appointment).grid(row=4, column=0, pady=10)
ttk.Button(frame_buttons, text="Clear Fields", command=clear_fields).grid(row=4, column=1)

# Add "Edit" and "Delete" Buttons to the GUI
ttk.Button(frame_buttons, text="Update Appointment", command=edit_appointment).grid(row=4, column=3, pady=10)
ttk.Button(frame_buttons, text="Delete Appointment", command=delete_appointment).grid(row=4, column=4, pady=10)


dataview_frame = tk.Frame(frame_dataarea, padx=0, pady=0, bg="lightgrey", relief="ridge", bd=1)
dataview_frame.grid(row=0, column=0, columnspan=4)

tree = ttk.Treeview(dataview_frame, columns=(
    "appointment_id", 
    # "user_id", 
    "patient_id", 
    "patient_name", 
    "appointment_date", 
    "appointment_time", 
    "provider_name"
), show="headings")

tree.heading("appointment_id", text="APPT ID")
# tree.heading("user_id", text="USER ID")
tree.heading("patient_id", text="Patient ID")
tree.heading("patient_name", text="Patient Name")
tree.heading("appointment_date", text="Date")
tree.heading("appointment_time", text="Time")
tree.heading("provider_name", text="Provider")
tree.grid(row=5, column=0, columnspan=3, pady=0)
tree.column("appointment_id", width=80, anchor="center")
# tree.column("user_id", width=80, anchor="center")
tree.column("patient_id", width=80, anchor="center")
tree.column("appointment_date", width=130, anchor="w")
tree.column("appointment_time", width=130, anchor="w")

tree.column("provider_name", width=180, anchor="w")
tree.column("patient_name", width=180, anchor="w")


# Binding the Treeview selection event to the populate_fields() function
tree.bind("<<TreeviewSelect>>", populate_fields)  # Populate fields when an item is selected

# tree.bind("<Double-1>", lambda event: some_function())  # Double-click to perform an action

tree.bind("<Delete>", lambda event: delete_appointment())  # Delete appointment with Delete key



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

dataview_frame.grid_rowconfigure(0, weight=1)  # Allow the Treeview to expand vertically
dataview_frame.grid_columnconfigure(0, weight=1)  # Allow the Treeview to expand horizontally





if __name__ == "__main__":
    # patients_database() # Call the function to create the patients database
    # appointments_database() # Call the function to create the appointments database
    print("\nTeam 2 Database setup for Appointment Screen complete.\n")

    # Fetch patient IDs and names for Autocomplete from the database
    patient_data_var = fetch_patient_info()  # Returns [(ID, Name), ...]

    # Set suggestions for the autocomplete entry
    patient_entry.set_suggestions(patient_data_var)  # Set patient name suggestions

    load_appointments() # Load appointments into the Treeview on startup

    # root = tk.Tk()  # Create the main window
    # root.geometry("600x400")  # Set the window size    
    root.mainloop()  # Start the Tkinter main loop

    # root.destroy()  # Close the main window when done
    # root.quit()  # Exit the application