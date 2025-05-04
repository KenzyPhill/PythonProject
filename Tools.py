import tkinter as tk
from tkinter import ttk, messagebox
# from tkinter import messagebox
import sqlite3
from tkcalendar import Calendar
# import database_setup # Importing the database_setup module
from database_setup import patients_database # Importing the patients_database function from the database_setup module
from database_setup import appointments_database # Importing the appointments_database function from the database_setup module




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





#####################################################################################

# appointments_database()
root = tk.Tk()  # Create the main window
# root.geometry("600x400")  # Set the window size
root.title("Tools Screen")  # Set the window title
root.configure(bg="lightblue")  # Set the background color of the main window
# root.iconbitmap("icon.ico")  # Set the window icon



style = ttk.Style()
style.theme_use("clam")  # Modern theme
style.configure("TFrame", background="lightblue")
style.configure("TLabel", background="lightblue", font=("Helvetica", 10))
style.configure("TButton", background="lightgrey", font=("Helvetica", 10), padding=5)
style.configure("TCombobox", background="lightgrey", font=("Helvetica", 10))
style.configure("TEntry", font=("Helvetica", 10))
# style.configure("Treeview", font=("Helvetica", 11), rowheight=30)
# style.configure("TTreeview.Heading", font=("Helvetica", 10, "bold"))
style.map("TButton", background=[("active", "lightgrey")])  # Change button color on hover
style.map("TEntry", background=[("focus", "white")])  # Change entry color on focus
style.map("TCombobox", background=[("focus", "white")])  # Change combobox color on focus
style.map("TTreeview", background=[("selected", "#347083")])  # Change treeview color on selection
style.map("TTreeview.Heading", background=[("active", "#347083")])  # Change treeview heading color on hover
style.map("TTreeview.Heading", foreground=[("active", "white")])
style.map("TTreeview.Heading", foreground=[("selected", "white")])



weight_var = tk.StringVar()  # StringVar to hold the weight
height_var = tk.StringVar()  # StringVar to hold the height
systolic_var = tk.StringVar()  # StringVar to hold the systolic blood pressure
diastolic_var = tk.StringVar()  # StringVar to hold the diastolic blood pressure



# Diagnostic Tools Frame
# This frame will hold the diagnostic tools widgets (BMI Calculator, Blood Pressure Tracker, etc.)
frame_tools = tk.Frame(root, padx=20, pady=5)
frame_tools.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
frame_tools.configure(bg="lightblue")  # Set the background color of the frame



# BMI Calculator
ttk.Label(frame_tools, text="BMI Calculator", font="Arial 12 bold").grid(row=0, column=0, pady=10, sticky="w")

ttk.Label(frame_tools, text="Weight (kg):").grid(row=1, column=0, pady=5)
weight_var = tk.StringVar()
ttk.Entry(frame_tools, textvariable=weight_var).grid(row=1, column=1, pady=5)

ttk.Label(frame_tools, text="Height (cm):").grid(row=2, column=0, pady=5)
height_var = tk.StringVar()
ttk.Entry(frame_tools, textvariable=height_var).grid(row=2, column=1, pady=5)

ttk.Button(frame_tools, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=10)

# Blood Pressure Tracker
ttk.Label(frame_tools, text="Blood Pressure Tracker", font="Arial 12 bold").grid(row=4, column=0, pady=10, sticky="w")

ttk.Label(frame_tools, text="Systolic (mmHg):").grid(row=5, column=0, pady=5)
systolic_var = tk.StringVar()
ttk.Entry(frame_tools, textvariable=systolic_var).grid(row=5, column=1, pady=5)

ttk.Label(frame_tools, text="Diastolic (mmHg):").grid(row=6, column=0, pady=5)
diastolic_var = tk.StringVar()
ttk.Entry(frame_tools, textvariable=diastolic_var).grid(row=6, column=1, pady=5)

ttk.Button(frame_tools, text="Check Blood Pressure", command=check_bp).grid(row=7, column=0, columnspan=2, pady=10)






if __name__ == "__main__":
    # root = tk.Tk()  # Create the main window
    # root.geometry("600x400")  # Set the window size    
    root.mainloop()  # Start the Tkinter main loop

    # root.destroy()  # Close the main window when done
    # root.quit()  # Exit the application