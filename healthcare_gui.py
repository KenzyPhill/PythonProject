import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- DB Helper Functions ---
def connect_db():
    return sqlite3.connect('healthcare.db')

def get_patients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    conn.close()
    return data

def add_patient(name, age, gender, contact, history):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, gender, contact, medical_history)
        VALUES (?, ?, ?, ?, ?)
    """, (name, age, gender, contact, history))
    conn.commit()
    conn.close()

def add_appointment(patient_id, appointment_time):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_id, appointment_time)
        VALUES (?, ?)
    """, (patient_id, appointment_time))
    conn.commit()
    conn.close()

def get_appointments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, patient_id, appointment_time FROM appointments")
    data = cursor.fetchall()
    conn.close()
    return data

# --- GUI Setup ---
app = tk.Tk()
app.title("Healthcare System")
app.geometry("700x500")

# Tabs
notebook = ttk.Notebook(app)
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
notebook.add(tab1, text='Add Patient')
notebook.add(tab2, text='View Patients')
notebook.add(tab3, text='Appointments')
notebook.pack(expand=1, fill="both")

# --- Tab 1: Add Patient ---
tk.Label(tab1, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
tk.Label(tab1, text="Age:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
tk.Label(tab1, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
tk.Label(tab1, text="Contact:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
tk.Label(tab1, text="Medical History:").grid(row=4, column=0, padx=10, pady=5, sticky='e')

entry_name = tk.Entry(tab1)
entry_age = tk.Entry(tab1)
entry_gender = tk.Entry(tab1)
entry_contact = tk.Entry(tab1)
entry_history = tk.Entry(tab1)

entry_name.grid(row=0, column=1)
entry_age.grid(row=1, column=1)
entry_gender.grid(row=2, column=1)
entry_contact.grid(row=3, column=1)
entry_history.grid(row=4, column=1)

def save_patient():
    try:
        add_patient(entry_name.get(), entry_age.get(), entry_gender.get(), entry_contact.get(), entry_history.get())
        messagebox.showinfo("Success", "Patient added successfully!")
        entry_name.delete(0, 'end')
        entry_age.delete(0, 'end')
        entry_gender.delete(0, 'end')
        entry_contact.delete(0, 'end')
        entry_history.delete(0, 'end')
        load_patients()
        refresh_patient_dropdown()
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(tab1, text="Add Patient", command=save_patient).grid(row=5, column=1, pady=10)

# --- Tab 2: View Patients ---
tree = ttk.Treeview(tab2, columns=("ID", "Name", "Age", "Gender", "Contact", "History"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack(expand=True, fill="both")

def load_patients():
    for i in tree.get_children():
        tree.delete(i)
    for row in get_patients():
        tree.insert('', 'end', values=row)

load_patients()

# --- Tab 3: Appointments ---
tk.Label(tab3, text="Select Patient:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
tk.Label(tab3, text="Appointment Time:").grid(row=1, column=0, padx=10, pady=5, sticky='e')

selected_patient = tk.StringVar()
patient_dropdown = ttk.Combobox(tab3, textvariable=selected_patient, state="readonly")
patient_dropdown.grid(row=0, column=1)

entry_time = tk.Entry(tab3)
entry_time.grid(row=1, column=1)

def refresh_patient_dropdown():
    patients = get_patients()
    formatted = [f"{p[0]} - {p[1]}" for p in patients]
    patient_dropdown['values'] = formatted

def save_appointment():
    try:
        patient_id = int(selected_patient.get().split(" - ")[0])
        time = entry_time.get()
        add_appointment(patient_id, time)
        messagebox.showinfo("Success", "Appointment added!")
        entry_time.delete(0, 'end')
        load_appointments()
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(tab3, text="Save Appointment", command=save_appointment).grid(row=2, column=1, pady=10)

appt_tree = ttk.Treeview(tab3, columns=("ID", "Patient ID", "Time"), show='headings')
for col in appt_tree["columns"]:
    appt_tree.heading(col, text=col)
appt_tree.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

def load_appointments():
    for i in appt_tree.get_children():
        appt_tree.delete(i)
    for row in get_appointments():
        appt_tree.insert('', 'end', values=row)

# Initial dropdown & appointment load
refresh_patient_dropdown()
load_appointments()

# Run app
app.mainloop()
