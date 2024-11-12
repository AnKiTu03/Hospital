import tkinter as tk
from tkcalendar import Calendar
import mysql.connector
from tkinter import messagebox
from ttkbootstrap import Style, ttk
from PIL import Image, ImageTk  # For loading icons

from mysql.connector import Error

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="Ankit@16113", 
        database="hospital_db"
    )

# Homepage GUI using ttkbootstrap
class HomePage:
    def __init__(self, root):
        # Apply the ttkbootstrap theme
        style = Style(theme="flatly")
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")  # Light background color for the main window

        # Header frame for the title
        header_frame = tk.Frame(root, bg="#003f73", bd=0)
        header_frame.pack(fill="x", pady=(0, 20))

        # Title label with larger text and centered alignment in header frame
        title_label = ttk.Label(header_frame, text="Welcome to Ryan's Hospital", font=("Arial", 24, "bold"), foreground="white", anchor="center", background="#003f73")
        title_label.pack(pady=20)

        # Load button icons with quality adjustment
        self.patient_icon = ImageTk.PhotoImage(Image.open("/Users/ankitupatil1/Downloads/hospital-building-for-healthcare-background-illustration-with-ambulance-car-doctor-patient-nurses-and-medical-clinic-exterior-free-vector.jpg").resize((30, 30), Image.LANCZOS))
        self.doctor_icon = ImageTk.PhotoImage(Image.open("/Users/ankitupatil1/Downloads/hospital-building-for-healthcare-background-illustration-with-ambulance-car-doctor-patient-nurses-and-medical-clinic-exterior-free-vector.jpg").resize((30, 30), Image.LANCZOS))
        self.appointment_icon = ImageTk.PhotoImage(Image.open("/Users/ankitupatil1/Downloads/hospital-building-for-healthcare-background-illustration-with-ambulance-car-doctor-patient-nurses-and-medical-clinic-exterior-free-vector.jpg").resize((30, 30), Image.LANCZOS))

        # Button styles with larger fonts and padding
        style.configure("Large.TButton",
                        font=("Arial", 16, "bold"), 
                        padding=10, 
                        background="#5a9bd5",  
                        foreground="white")

        # Hover effect configuration
        style.map("Large.TButton",
                  background=[("active", "#003f73")],
                  foreground=[("active", "white")])

        # Frame for buttons to keep them organized and centered
        button_frame = ttk.Frame(root, padding=20, style="TFrame")
        button_frame.pack(expand=True)

        # Buttons with icons, tooltip, hover effects, and padding
        self.patient_button = ttk.Button(button_frame, text=" PATIENT MANAGEMENT", image=self.patient_icon, compound="left", style="Large.TButton", command=self.patient_segment)
        self.patient_button.pack(pady=10, ipadx=10, ipady=10, anchor="center")
        self.patient_button.bind("<Enter>", lambda e: self.show_tooltip("Manage patient records, admissions, and histories."))
        
        self.doctor_button = ttk.Button(button_frame, text=" DOCTOR MANAGEMENT", image=self.doctor_icon, compound="left", style="Large.TButton", command=self.doctor_segment)
        self.doctor_button.pack(pady=10, ipadx=10, ipady=10, anchor="center")
        self.doctor_button.bind("<Enter>", lambda e: self.show_tooltip("Manage doctor profiles, specializations, and schedules."))
        
        self.appointment_button = ttk.Button(button_frame, text=" APPOINTMENT MANAGEMENT", image=self.appointment_icon, compound="left", style="Large.TButton", command=self.appointment_segment)
        self.appointment_button.pack(pady=10, ipadx=10, ipady=10, anchor="center")
        self.appointment_button.bind("<Enter>", lambda e: self.show_tooltip("Manage patient appointments and schedules."))

        # Tooltip label (hidden by default)
        self.tooltip_label = tk.Label(root, text="", font=("Arial", 10), fg="gray", bg="#f0f4f8")
        self.tooltip_label.pack_forget()

    def show_tooltip(self, text):
        """Display tooltip text near buttons on hover."""
        self.tooltip_label.config(text=text)
        self.tooltip_label.pack(pady=5)

    def hide_tooltip(self, event=None):
        """Hide the tooltip text."""
        self.tooltip_label.pack_forget()

    def patient_segment(self):
        patient_window = tk.Toplevel(self.root)
        PatientSegment(patient_window)

    def doctor_segment(self):
        doctor_window = tk.Toplevel(self.root)
        DoctorSegment(doctor_window)

    def appointment_segment(self):
        appointment_window = tk.Toplevel(self.root)
        AppointmentSegment(appointment_window)




import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Assuming connect_db() is defined elsewhere in your code
# from your_database_module import connect_db

class PatientSegment:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Segment")
        self.root.geometry("800x600")
        self.root.configure(bg="#ffffe0")  # Light yellow background for a pleasant look

        # Configure style for a modern look
        style = ttk.Style()
        style.theme_use("clam")  # Using 'clam' theme for consistency across platforms

        # Set styles for widgets
        style.configure("TFrame", background="#ffffe0")
        style.configure("TNotebook", background="#ffffe0")
        style.configure("TNotebook.Tab", font=("Calibri", 12, "bold"))
        style.configure("TLabel", background="#ffffe0", font=("Calibri", 12))
        style.configure("TCombobox", font=("Calibri", 12))
        style.configure("TButton", font=("Calibri", 12, "bold"), foreground="white")
        style.map("TButton",
                  background=[('!disabled', '#4CAF50'), ('active', '#45a049')],
                  foreground=[('!disabled', 'white')])

        # Notebook widget (tabs)
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        # Create Tabs for Add, Update, View, All Patients
        self.add_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.all_patients_tab = ttk.Frame(notebook)
        self.setup_all_patients_tab()

        notebook.add(self.add_tab, text="Add Patient")
        notebook.add(self.update_tab, text="Update Patient")
        notebook.add(self.view_tab, text="View Patient by ID")
        notebook.add(self.all_patients_tab, text="All Patients")

        # Add Patient Tab Widgets
        self.add_frame = ttk.LabelFrame(self.add_tab, text="Add New Patient", background="#ffffe0")
        self.add_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(7):
            self.add_frame.rowconfigure(i, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=2)

        # Patient Name
        ttk.Label(self.add_frame, text="Patient Name:", background="#ffffe0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_frame = tk.Frame(self.add_frame, bg='black')
        name_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(name_frame, bd=0, font=("Calibri", 12))
        self.name_entry.pack(padx=3, pady=3)  # Increased padding for thicker border

        # Age
        ttk.Label(self.add_frame, text="Age:", background="#ffffe0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        age_frame = tk.Frame(self.add_frame, bg='black')
        age_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.age_entry = tk.Entry(age_frame, bd=0, font=("Calibri", 12))
        self.age_entry.pack(padx=3, pady=3)  # Increased padding

        # Gender
        ttk.Label(self.add_frame, text="Gender:", background="#ffffe0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.gender_combobox = ttk.Combobox(self.add_frame, state="readonly", font=("Calibri", 12))
        self.gender_combobox['values'] = ("Male", "Female", "Other")
        self.gender_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Contact
        ttk.Label(self.add_frame, text="Contact:", background="#ffffe0").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        contact_frame = tk.Frame(self.add_frame, bg='black')
        contact_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.contact_entry = tk.Entry(contact_frame, bd=0, font=("Calibri", 12))
        self.contact_entry.pack(padx=3, pady=3)  # Increased padding

        # House Number
        ttk.Label(self.add_frame, text="House Number:", background="#ffffe0").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        hno_frame = tk.Frame(self.add_frame, bg='black')
        hno_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.hno_entry = tk.Entry(hno_frame, bd=0, font=("Calibri", 12))
        self.hno_entry.pack(padx=3, pady=3)  # Increased padding

        # Locality
        ttk.Label(self.add_frame, text="Locality:", background="#ffffe0").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        locality_frame = tk.Frame(self.add_frame, bg='black')
        locality_frame.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.locality_entry = tk.Entry(locality_frame, bd=0, font=("Calibri", 12))
        self.locality_entry.pack(padx=3, pady=3)  # Increased padding

        # Pincode
        ttk.Label(self.add_frame, text="Pincode:", background="#ffffe0").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        pincode_frame = tk.Frame(self.add_frame, bg='black')
        pincode_frame.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.pincode_entry = tk.Entry(pincode_frame, bd=0, font=("Calibri", 12))
        self.pincode_entry.pack(padx=3, pady=3)  # Increased padding

        # Add Patient Button
        self.add_button = ttk.Button(self.add_tab, text="Add Patient", padding=10, command=self.add_patient)
        self.add_button.pack(pady=10)

        # Update Patient Tab Widgets
        self.update_frame = ttk.LabelFrame(self.update_tab, text="Update Patient Information", background="#ffffe0")
        self.update_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(3):
            self.update_frame.rowconfigure(i, weight=1)
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=2)

        # Patient ID
        ttk.Label(self.update_frame, text="Patient ID:", background="#ffffe0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        id_frame = tk.Frame(self.update_frame, bg='black')
        id_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.patient_id_entry = tk.Entry(id_frame, bd=0, font=("Calibri", 12))
        self.patient_id_entry.pack(padx=3, pady=3)  # Increased padding

        # Field to Update
        ttk.Label(self.update_frame, text="Field to Update:", background="#ffffe0").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.field_combobox = ttk.Combobox(self.update_frame, state="readonly", font=("Calibri", 12))
        self.field_combobox['values'] = ("Name", "Age", "Gender", "Phone Number", "House Number", "Locality", "Pincode")
        self.field_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # New Value
        ttk.Label(self.update_frame, text="New Value:", background="#ffffe0").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        new_value_frame = tk.Frame(self.update_frame, bg='black')
        new_value_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.new_value_entry = tk.Entry(new_value_frame, bd=0, font=("Calibri", 12))
        self.new_value_entry.pack(padx=3, pady=3)  # Increased padding

        # Update Button
        self.update_button = ttk.Button(self.update_tab, text="Update", padding=10, command=self.perform_update)
        self.update_button.pack(pady=10)

        # View Patient by ID Widgets
        self.view_frame = ttk.LabelFrame(self.view_tab, text="Search Patient", background="#ffffe0")
        self.view_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.columnconfigure(1, weight=2)

        # Enter Patient ID
        ttk.Label(self.view_frame, text="Enter Patient ID:", background="#ffffe0").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        search_id_frame = tk.Frame(self.view_frame, bg='black')
        search_id_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.search_id_entry = tk.Entry(search_id_frame, bd=0, font=("Calibri", 12))
        self.search_id_entry.pack(padx=3, pady=3)  # Increased padding

        # Search Button
        self.search_button = ttk.Button(self.view_frame, text="Search Patient", padding=10, command=self.view_patient_by_id)
        self.search_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Patient Details Frame
        self.patient_details_frame = ttk.LabelFrame(self.view_tab, text="Patient Details", background="#ffffe0")
        self.patient_details_frame.pack(padx=20, pady=10, fill='both', expand=True)

        details_labels = ["ID:", "Name:", "Age:", "Gender:", "Phone Number:", "House Number:", "Locality:", "Pincode:"]
        self.patient_detail_labels = []
        for i, label_text in enumerate(details_labels):
            label = ttk.Label(self.patient_details_frame, text=label_text, background="#ffffe0")
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            value_label = ttk.Label(self.patient_details_frame, text="", background="#ffffe0")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.patient_detail_labels.append(value_label)

        # Configure grid layout for patient details
        self.patient_details_frame.columnconfigure(0, weight=1)
        self.patient_details_frame.columnconfigure(1, weight=2)

    def setup_all_patients_tab(self):
        columns = ("ID", "Name", "Age", "Gender", "Phone Number", "House Number", "Locality", "Pincode")
        self.patient_tree = ttk.Treeview(self.all_patients_tab, columns=columns, show="headings")
        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=100, anchor="center")

        self.patient_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(self.all_patients_tab, orient="vertical", command=self.patient_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.patient_tree.configure(yscrollcommand=scrollbar.set)

        load_button = ttk.Button(self.all_patients_tab, text="Load All Patients", padding=10, command=self.load_all_patients)
        load_button.pack(pady=10)

    def add_patient(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_combobox.get()
        contact = self.contact_entry.get()
        hno = self.hno_entry.get()
        locality = self.locality_entry.get()
        pincode = self.pincode_entry.get()

        # Check if all fields are filled
        if not name or not age or not gender or not contact or not hno or not locality or not pincode:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        # Additional input validations
        if any(char.isdigit() for char in name):
            messagebox.showerror("Input Error", "Name cannot contain numbers or special characters.")
            return

        try:
            age_int = int(age)
            if not (0 <= age_int < 120):
                messagebox.showerror("Input Error", "Enter a valid age.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a number.")
            return

        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Input Error", "Phone number must be 10 digits.")
            return

        if not pincode.isdigit() or len(pincode) != 6:
            messagebox.showerror("Input Error", "Pincode must be 6 digits.")
            return

        # Insert into database
        try:
            db = connect_db()
            cursor = db.cursor()
            query = '''INSERT INTO patient_det (name, age, gender, phone_number, house_number, locality, pincode)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, (name, age, gender, contact, hno, locality, pincode))
            db.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
            db.close()

            # Clear input fields after successful insertion
            self.name_entry.delete(0, tk.END)
            self.age_entry.delete(0, tk.END)
            self.gender_combobox.set('')
            self.contact_entry.delete(0, tk.END)
            self.hno_entry.delete(0, tk.END)
            self.locality_entry.delete(0, tk.END)
            self.pincode_entry.delete(0, tk.END)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add patient: {e}")

    def perform_update(self):
        patient_id = self.patient_id_entry.get()
        field_to_update = self.field_combobox.get()
        new_value = self.new_value_entry.get()

        if not patient_id or not field_to_update or not new_value:
            messagebox.showerror("Error", "Please enter all details")
            return

        # Map field names to database column names
        field_map = {
            "Name": "name",
            "Age": "age",
            "Gender": "gender",
            "Phone Number": "phone_number",
            "House Number": "house_number",
            "Locality": "locality",
            "Pincode": "pincode"
        }
        db_column = field_map.get(field_to_update)

        # Perform the update operation
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(f"UPDATE patient_det SET {db_column} = %s WHERE id = %s", (new_value, patient_id))
            db.commit()

            # Check if update was successful
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"{field_to_update} updated successfully!")
            else:
                messagebox.showerror("Error", "Patient ID not found or update failed")

            db.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to update patient: {e}")

    def view_patient_by_id(self):
        patient_id = self.search_id_entry.get()
        if not patient_id:
            messagebox.showerror("Error", "Please enter a Patient ID")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM patient_det WHERE id = %s", (patient_id,))
            patient = cursor.fetchone()
            db.close()

            if patient:
                # Update labels with patient details
                for i, value in enumerate(patient):
                    self.patient_detail_labels[i].config(text=str(value))
            else:
                messagebox.showinfo("Not Found", "No patient found with the given ID")
                # Clear labels if patient not found
                for label in self.patient_detail_labels:
                    label.config(text="")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to retrieve patient: {e}")

    def load_all_patients(self):
        # Clear the Treeview
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        # Connect to the database and fetch all patient data
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM patient_det")
            patients = cursor.fetchall()
            db.close()

            # Insert each patient's details into the Treeview
            for patient in patients:
                self.patient_tree.insert("", "end", values=patient)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load patients: {e}")



# Doctor Segment with Tabs
class DoctorSegment:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Segment")

        # Create Notebook (tabs) widget
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=10, expand=True)

        # Create Tabs for Add, Update, View
        self.add_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.all_doctors_tab = ttk.Frame(notebook)
        self.setup_all_doctors_tab()
        # Add tabs to notebook
        notebook.add(self.add_tab, text="Add Doctor")
        notebook.add(self.update_tab, text="Update Doctor")
        notebook.add(self.view_tab, text="View Doctor by ID")
        notebook.add(self.all_doctors_tab, text="All Doctors")

        # Add Doctor Tab Widgets
        self.name_label = ttk.Label(self.add_tab, text="Doctor Name")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = ttk.Entry(self.add_tab, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.department_label = ttk.Label(self.add_tab, text="Department")
        self.department_label.grid(row=1, column=0, padx=10, pady=5)
        self.department_entry = ttk.Entry(self.add_tab, width=30)
        self.department_entry.grid(row=1, column=1, padx=10, pady=5)

        self.DOB_label = ttk.Label(self.add_tab, text="Date of Birth[YYYY-MM-DD]")
        self.DOB_label.grid(row=2, column=0, padx=10, pady=5)
        self.DOB_entry = ttk.Entry(self.add_tab, width=30)
        self.DOB_entry.grid(row=2, column=1, padx=10, pady=5)

        self.gender_label = ttk.Label(self.add_tab, text="Gender") 
        self.gender_label.grid(row=3, column=0, padx=10, pady=5)

        # Dropdown for selecting gender
        self.gender_combobox = ttk.Combobox(self.add_tab, width=27, state="readonly")
        self.gender_combobox['values'] = ("Male", "Female", "Other")  # Gender options
        self.gender_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.contact_label = ttk.Label(self.add_tab, text="Contact")
        self.contact_label.grid(row=4, column=0, padx=10, pady=5)
        self.contact_entry = ttk.Entry(self.add_tab, width=30)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=5)

        self.hno_label = ttk.Label(self.add_tab, text="House Number")
        self.hno_label.grid(row=5, column=0, padx=10, pady=5)
        self.hno_entry = ttk.Entry(self.add_tab, width=30)
        self.hno_entry.grid(row=5, column=1, padx=10, pady=5)

        self.locality_label = ttk.Label(self.add_tab, text="Locality")
        self.locality_label.grid(row=6, column=0, padx=10, pady=5)
        self.locality_entry = ttk.Entry(self.add_tab, width=30)
        self.locality_entry.grid(row=6, column=1, padx=10, pady=5)

        self.pincode_label = ttk.Label(self.add_tab, text="Pincode")
        self.pincode_label.grid(row=7, column=0, padx=10, pady=5)
        self.pincode_entry = ttk.Entry(self.add_tab, width=30)
        self.pincode_entry.grid(row=7, column=1, padx=10, pady=5)

        self.qualifications_label = ttk.Label(self.add_tab, text="Qualifications")
        self.qualifications_label.grid(row=8, column=0, padx=10, pady=5)
        self.qualifications_entry = ttk.Entry(self.add_tab, width=30)
        self.qualifications_entry.grid(row=8, column=1, padx=10, pady=5)

        self.experience_label = ttk.Label(self.add_tab, text="Experience [years]")
        self.experience_label.grid(row=9, column=0, padx=10, pady=5)
        self.experience_entry = ttk.Entry(self.add_tab, width=30)
        self.experience_entry.grid(row=9, column=1, padx=10, pady=5)

        self.aadhar_label = ttk.Label(self.add_tab, text="Aadhar No.")
        self.aadhar_label.grid(row=10, column=0, padx=10, pady=5)
        self.aadhar_entry = ttk.Entry(self.add_tab, width=30)
        self.aadhar_entry.grid(row=10, column=1, padx=10, pady=5)
        self.add_button = ttk.Button(self.add_tab, text="Add Doctor", bootstyle="primary", command=self.add_doctor)
        self.add_button.grid(row=11, column=0, columnspan=2, pady=10)
        
       
        # Update Doctor Tab Widgets
        self.doctor_id_label = ttk.Label(self.update_tab, text="Doctor ID:")
        self.doctor_id_label.grid(row=0, column=0, padx=10, pady=5)
        self.doctor_id_entry = ttk.Entry(self.update_tab, width=30)
        self.doctor_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.field_label = ttk.Label(self.update_tab, text="Field to Update:")
        self.field_label.grid(row=1, column=0, padx=10, pady=5)
        self.field_combobox = ttk.Combobox(self.update_tab, width=27, state="readonly")
        self.field_combobox['values'] = ("Name", "Department", "DOB", "Gender", "Contact", "House Number", "Locality", "Pincode","Qualifications","Experience","Aadhar Number")
        self.field_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.field_combobox.set("Select Field")

        # Entry for New Value
        self.new_value_label = ttk.Label(self.update_tab, text="New Value:")
        self.new_value_label.grid(row=2, column=0, padx=10, pady=5)
        self.new_value_entry = ttk.Entry(self.update_tab, width=30)
        self.new_value_entry.grid(row=2, column=1, padx=10, pady=5)

        # Update Button
        update_button = ttk.Button(self.update_tab, text="Update", command=self.perform_update)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

        #view by id
        self.search_id_label = ttk.Label(self.view_tab, text="Enter Doctor ID:")
        self.search_id_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_id_entry = ttk.Entry(self.view_tab, width=30)
        self.search_id_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = ttk.Button(self.view_tab, text="Search Doctor", command=self.view_doctor_by_id)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.doctor_details_frame = ttk.LabelFrame(self.view_tab, text="Doctor Details", width=40)
        self.doctor_details_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Labels for displaying patient details
        self.doctor_id_label = ttk.Label(self.doctor_details_frame, text="ID: ")
        self.doctor_id_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        self.doctor_name_label = ttk.Label(self.doctor_details_frame, text="Name: ")
        self.doctor_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        
        self.doctor_department_label = ttk.Label(self.doctor_details_frame, text="Department: ")
        self.doctor_department_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)
        
        self.doctor_dob_label = ttk.Label(self.doctor_details_frame, text="Date of Birth: ")
        self.doctor_dob_label.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        self.doctor_gender_label = ttk.Label(self.doctor_details_frame, text="Gender: ")
        self.doctor_gender_label.grid(row=4, column=0, sticky="w", padx=10, pady=2)
        
        self.doctor_contact_label = ttk.Label(self.doctor_details_frame, text="Phone Number: ")
        self.doctor_contact_label.grid(row=5, column=0, sticky="w", padx=10, pady=2)

        self.doctor_hno_label = ttk.Label(self.doctor_details_frame, text="House Number: ")
        self.doctor_hno_label.grid(row=6, column=0, sticky="w", padx=10, pady=2)

        self.doctor_locality_label = ttk.Label(self.doctor_details_frame, text="Locality: ")
        self.doctor_locality_label.grid(row=7, column=0, sticky="w", padx=10, pady=2)

        self.doctor_pincode_label = ttk.Label(self.doctor_details_frame, text="Pincode: ")
        self.doctor_pincode_label.grid(row=8, column=0, sticky="w", padx=10, pady=2)

        self.doctor_qualification_label = ttk.Label(self.doctor_details_frame, text="Qualifications: ")
        self.doctor_qualification_label.grid(row=9, column=0, sticky="w", padx=10, pady=2)

        self.doctor_experience_label = ttk.Label(self.doctor_details_frame, text="Experience: ")
        self.doctor_experience_label.grid(row=10, column=0, sticky="w", padx=10, pady=2)

        self.doctor_aadhar_label = ttk.Label(self.doctor_details_frame, text="Aadhar Number: ")
        self.doctor_aadhar_label.grid(row=11, column=0, sticky="w", padx=10, pady=2)

    def setup_all_doctors_tab(self):
        # Treeview widget for displaying all doctors
        self.doctor_tree = ttk.Treeview(self.all_doctors_tab, columns=("ID", "Name", "Department", "DOB", "Gender", "Contact", "House Number", "Locality", "Pincode","Qualifications","Experience","Aadhar"), show="headings")
        self.doctor_tree.heading("ID", text="ID")
        self.doctor_tree.heading("Name", text="Name")
        self.doctor_tree.heading("Department", text="Department")
        self.doctor_tree.heading("DOB", text="DOB")
        self.doctor_tree.heading("Gender", text="Gender")
        self.doctor_tree.heading("Contact", text="Contact")
        self.doctor_tree.heading("House Number", text="House No")
        self.doctor_tree.heading("Locality", text="Locality")
        self.doctor_tree.heading("Pincode", text="Pincode")
        self.doctor_tree.heading("Qualifications", text="Qualifications")
        self.doctor_tree.heading("Experience", text="Experience")
        self.doctor_tree.heading("Aadhar", text="Aadhar Number")

        # Set column widths for better readability
        for col in self.doctor_tree["columns"]:
            self.doctor_tree.column(col, width=100, anchor="center")

        # Place the Treeview widget on the tab with scrollbar
        self.doctor_tree.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.all_doctors_tab, orient="vertical", command=self.doctor_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.doctor_tree.configure(yscrollcommand=scrollbar.set)

        # Button to load data
        load_button = ttk.Button(self.all_doctors_tab, text="Load All Doctors", command=self.load_all_doctors)
        load_button.pack(pady=10)



    def add_doctor(self):
        name = self.name_entry.get()
        department = self.department_entry.get()
        DOB = self.DOB_entry.get()
        gender = self.gender_combobox.get()
        contact=self.contact_entry.get()
        hno=self.hno_entry.get()
        locality=self.locality_entry.get()
        pincode = self.pincode_entry.get()
        qualifications = self.qualifications_entry.get()
        experience = self.experience_entry.get()
        aadhar = self.aadhar_entry.get()

        if not name or not DOB or not gender or not contact or not hno or not locality or not pincode or not DOB or not department or not qualifications or not experience or not aadhar:
            messagebox.showwarning("Input Error", "All fields are required")
            return
    
        if any(char.isdigit() for char in name):
            messagebox.showerror("Input Error", "Name cannot contain numbers or special characters.")
            return
        if any(char.isdigit() for char in department):
            messagebox.showerror("Input Error", "Department cannot contain numbers or special characters.")
            return
        
        if any(char.isalpha() for char in DOB):
            messagebox.showerror("Input Error", "DOB cannot contain Alphabets.")

        if len(str(contact)) != 10:
            messagebox.showerror("Input Error", "Phone number must be 10 digits.")
            return
        
        if len(str(pincode)) != 6:
            messagebox.showerror("Input Error", "Pincode must be 6 digits.")
            return
        if any(char.isdigit() for char in qualifications):
            messagebox.showerror("Input Error", "Qualifications cannot contain numbers or special characters.")
            return
        if len(str(aadhar)) != 12:
            messagebox.showerror("Input Error", "Aadhar number must be 12 digits.")
            return
        
        try:
            db = connect_db()
            cursor = db.cursor()
            query = '''INSERT INTO doctor_det (name, department, DOB, gender, phone_number, house_number, locality, pincode, qualification,experience,aadhar)
                       VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)'''
            cursor.execute(query, (name, department, DOB, gender, contact, hno, locality, pincode,qualifications, experience,aadhar))
            db.commit()
            messagebox.showinfo("Success", "Doctor added successfully!")
            db.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to add doctor: {e}")
    def perform_update(self):
        doctor_id = self.doctor_id_entry.get()
        field_to_update = self.field_combobox.get()
        new_value = self.new_value_entry.get()

        if not doctor_id or not field_to_update or not new_value:
            messagebox.showerror("Error", "Please enter all details")
            return

        # Map field names to database column names
        field_map = {
            "Name": "name",
            "Department": "department",
            "DOB": "dob",
            "Gender": "gender",
            "Phone Number":"phone_number",
            "House Number":"house_number",
            "Locality":"locality",
            "Pincode":"pincode",
            "Qualifications": "qualification",
            "Experience": "experience",
            "Aadhar": "aadhar",
        }
        db_column = field_map.get(field_to_update)

        # Perform the update operation
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE doctor_det SET {db_column} = %s WHERE id = %s", (new_value, doctor_id))
        db.commit()

        # Check if update was successful
        if cursor.rowcount > 0:
            messagebox.showinfo("Success", f"{field_to_update} updated successfully!")
        else:
            messagebox.showerror("Error", "Doctor ID not found or update failed")

        db.close()


    def view_doctor_by_id(self):
        doctor_id = self.search_id_entry.get()
        if not doctor_id:
            messagebox.showerror("Error", "Please enter a Doctor ID")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doctor_det WHERE id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        db.close()

        if doctor:
            # Update labels with patient details
            self.doctor_id_label.config(text=f"ID: {doctor[0]}")
            self.doctor_name_label.config(text=f"Name: {doctor[1]}")
            self.doctor_department_label.config(text=f"Department: {doctor[2]}")
            self.doctor_dob_label.config(text=f"DOB: {doctor[3]}")
            self.doctor_gender_label.config(text=f"Gender: {doctor[4]}")
            self.doctor_contact_label.config(text=f"Phone Number: {doctor[5]}")
            self.doctor_hno_label.config(text=f"House Number: {doctor[6]}")
            self.doctor_locality_label.config(text=f"Locality: {doctor[7]}")
            self.doctor_pincode_label.config(text=f"Pincode: {doctor[8]}")
            self.doctor_qualification_label.config(text=f"Qualifications: {doctor[9]}")
            self.doctor_experience_label.config(text=f"Experience: {doctor[10]}")
            self.doctor_aadhar_label.config(text=f"Aadhar: {doctor[11]}")
        else:
            # Clear labels if patient not found
            self.doctor_id_label.config(text="ID: Not Found")
            self.doctor_name_label.config(text="Name: Not Found")
            self.doctor_department_label.config(text="Department: Not Found")
            self.doctor_dob_label.config(text="DOB: Not Found")
            self.doctor_gender_label.config(text="Gender: Not Found")
            self.doctor_contact_label.config(text="Phone Number: Not Found")
            self.doctor_hno_label.config(text="House Number: Not Found")
            self.doctor_locality_label.config(text="Locality: Not Found")
            self.doctor_pincode_label.config(text="Pincode: Not Found")
            self.doctor_qualification_label.config(text="Qualifications: Not Found")
            self.doctor_experience_label.config(text="Experience: Not Found")
            self.doctor_aadhar_label.config(text="Aadhar: Not Found")
    def load_all_doctors(self):
        # Clear the Treeview
        for item in self.doctor_tree.get_children():
                self.doctor_tree.delete(item)

        # Connect to the database and fetch all patient data
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doctor_det")
        doctors = cursor.fetchall()
        db.close()

        # Insert each patient's details into the Treeview
        for doctor in doctors:
            self.doctor_tree.insert("", "end", values=doctor)


# Appointment Segment
class AppointmentSegment:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Segment")

        # Create Notebook widget (tabs)
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=10, expand=True)

        # Create Tabs for Create, Delete, and View appointments
        self.create_tab = ttk.Frame(notebook)
        self.delete_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        notebook.add(self.create_tab, text="Create Appointment")
        notebook.add(self.delete_tab, text="Delete Appointment")
        notebook.add(self.view_tab, text="View Appointments")

        self.setup_create_appointment_tab()
        self.setup_delete_appointment_tab()
        self.setup_view_appointments_tab()

    def setup_create_appointment_tab(self):
        # Department Dropdown
        self.department_label = ttk.Label(self.create_tab, text="Department:")
        self.department_label.grid(row=0, column=0, padx=10, pady=5)
        self.department_combobox = ttk.Combobox(self.create_tab, width=30, state="readonly")
        self.department_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.department_combobox.bind("<<ComboboxSelected>>", self.update_doctor_dropdown)
        
        # Doctor Dropdown
        self.doctor_label = ttk.Label(self.create_tab, text="Doctor:")
        self.doctor_label.grid(row=1, column=0, padx=10, pady=5)
        self.doctor_combobox = ttk.Combobox(self.create_tab, width=30, state="readonly")
        self.doctor_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.doctor_combobox.bind("<<ComboboxSelected>>", self.update_time_slots)

        self.patient_label = ttk.Label(self.create_tab, text="Patient ID:")
        self.patient_label.grid(row=2, column=0, padx=10, pady=5)
        self.patient_entry = ttk.Entry(self.create_tab, width=30)
        self.patient_entry.grid(row=2, column=1, padx=10, pady=5)

        self.date_label = ttk.Label(self.create_tab, text="Appointment Date:")
        self.date_label.grid(row=3, column=0, padx=10, pady=5)
        # Create the calendar widget with the custom style
        
        
        self.date_label = ttk.Label(self.create_tab, text="Appointment Date (YYYY-MM-DD):")
        self.date_label.grid(row=3, column=0, padx=10, pady=5)
        self.date_entry = ttk.Entry(self.create_tab, width=30)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Bind the FocusOut event to manually trigger date-based actions
        self.date_entry.bind("<FocusOut>", self.update_time_slots)

        # Available Time Slots Dropdown
        self.time_label = ttk.Label(self.create_tab, text="Available Time Slots:")
        self.time_label.grid(row=4, column=0, padx=10, pady=5)
        self.time_combobox = ttk.Combobox(self.create_tab, width=30, state="readonly")
        self.time_combobox.grid(row=4, column=1, padx=10, pady=5)

        self.create_button = ttk.Button(self.create_tab, text="Create Appointment", command=self.create_appointment)
        self.create_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.load_departments()

    def setup_delete_appointment_tab(self):
        # Create widgets for deleting an appointment
        self.appointment_id_label = ttk.Label(self.delete_tab, text="Appointment ID:")
        self.appointment_id_label.grid(row=0, column=0, padx=10, pady=5)
        self.appointment_id_entry = ttk.Entry(self.delete_tab, width=30)
        self.appointment_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def setup_view_appointments_tab(self):
        # Treeview widget to display appointments
        self.appointment_tree = ttk.Treeview(self.view_tab, columns=("ID", "Patient ID", "Doctor ID","Doctor Name", "Department","Date", "Time"), show="headings")
        self.appointment_tree.heading("ID", text="ID")
        self.appointment_tree.heading("Patient ID", text="Patient ID")
        self.appointment_tree.heading("Doctor ID", text="Doctor ID")
        self.appointment_tree.heading("Doctor Name", text="Doctor Name")
        self.appointment_tree.heading("Department", text="Department")
        self.appointment_tree.heading("Date", text="Date")
        self.appointment_tree.heading("Time", text="Time")

        # Set column widths for better readability
        for col in self.appointment_tree["columns"]:
            self.appointment_tree.column(col, width=100, anchor="center")

        # Place the Treeview widget on the tab with scrollbar
        self.appointment_tree.pack(fill="both", expand=True)
        scrollbar = ttk.Scrollbar(self.view_tab, orient="vertical", command=self.appointment_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.appointment_tree.configure(yscrollcommand=scrollbar.set)

        # Button to load all appointments
        load_button = ttk.Button(self.view_tab, text="Load All Appointments", command=self.load_all_appointments)
        load_button.pack(pady=10)

    def load_departments(self):
        # Fetch departments from the doctor_det table
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT department FROM doctor_det")
        departments = cursor.fetchall()
        db.close()

        # Populate the department dropdown
        department_list = [dept[0] for dept in departments]
        self.department_combobox['values'] = department_list

    def update_doctor_dropdown(self, event):
        # Fetch doctors based on selected department
        selected_department = self.department_combobox.get()

        if not selected_department:
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT name, id FROM doctor_det WHERE department = %s", (selected_department,))
        doctors = cursor.fetchall()
        db.close()

        # Populate the doctor dropdown and map doctor names to IDs
        doctor_list = [doctor[0] for doctor in doctors]
        self.doctor_combobox['values'] = doctor_list
        self.doctor_id_dict = {doctor[0]: doctor[1] for doctor in doctors}

    def update_time_slots(self, event):
        # Fetch available time slots for selected doctor and date
        selected_doctor = self.doctor_combobox.get()
        selected_date = self.date_entry.get()

        if not selected_doctor or not selected_date:
            self.time_combobox['values'] = []
            return

        doctor_id = self.doctor_id_dict[selected_doctor]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT time_slot FROM available_slots
            WHERE doctor_id = %s AND date = %s
        """, (doctor_id, selected_date))
        slots = cursor.fetchall()
        db.close()

        # Populate time slots dropdown
        time_slots = [slot[0] for slot in slots]
        self.time_combobox['values'] = time_slots

    def create_appointment(self):
        patient_id = self.patient_entry.get()
        doctor_name = self.doctor_combobox.get()
        department = self.department_combobox.get()
        appointment_date = self.date_entry.get()
        appointment_time = self.time_combobox.get()

        if not patient_id or not doctor_name or not department or not appointment_date or not appointment_time:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        db = connect_db()
        cursor = db.cursor()

        # Fetch the doctor_id based on the selected doctor name
        cursor.execute("SELECT id FROM doctor_det WHERE name = %s", (doctor_name,))
        result = cursor.fetchone()
        if result:
            doctor_id = result[0]
        else:
            messagebox.showerror("Error", "Selected doctor not found.")
            return

        # Insert the appointment into the database
       # Revised query and execution
        query = '''INSERT INTO appointments 
                   (patient_id, doctor_id,doctor_name, department, appointment_date, appointment_time) 
                   VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, (patient_id, doctor_id, doctor_name, department, appointment_date, appointment_time))

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Appointment created successfully!")


    def delete_appointment(self):
        appointment_id = self.appointment_id_entry.get()

        if not appointment_id:
            messagebox.showwarning("Input Error", "Appointment ID is required")
            return

        # Delete the appointment from the database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Appointment deleted successfully!")

    def load_all_appointments(self):
        # Clear the Treeview
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        # Connect to the database and fetch all appointments
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
        db.close()

        # Insert each appointment into the Treeview
        for appointment in appointments:
            self.appointment_tree.insert("", "end", values=appointment)

# Main function to run the Tkinter app
def main():
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Initialize the HomePage class to show the homepage
    home_page = HomePage(root)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
