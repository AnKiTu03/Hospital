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
        self.patient_icon = ImageTk.PhotoImage(Image.open("d:\\Downloads\\dsa-notes-main\\3e666e50854f4069c37150d7e8c9bdc.jpg").resize((30, 30), Image.LANCZOS))
        self.doctor_icon = ImageTk.PhotoImage(Image.open("d:\\Downloads\\dsa-notes-main\\3e666e50854f4069c37150d7e8c9bdc.jpg").resize((30, 30), Image.LANCZOS))
        self.appointment_icon = ImageTk.PhotoImage(Image.open("d:\\Downloads\\dsa-notes-main\\3e666e50854f4069c37150d7e8c9bdc.jpg").resize((30, 30), Image.LANCZOS))

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




class PatientSegment:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Segment")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")  # Light blue background for a pleasant look

        # Configure style for a modern look
        style = ttk.Style()
        style.theme_use("clam")  # Using 'clam' theme for consistency across platforms

        # Set styles for widgets
        style.configure("TFrame", background="#e6f2ff")
        style.configure("TNotebook", background="#e6f2ff")
        style.configure("TNotebook.Tab", font=("Calibri", 12, "bold"))
        style.configure("TLabel", background="#e6f2ff", font=("Calibri", 12))
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
        self.add_frame = ttk.LabelFrame(self.add_tab, text="Add New Patient")
        self.add_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(7):
            self.add_frame.rowconfigure(i, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=2)

        # Patient Name
        ttk.Label(self.add_frame, text="Patient Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_frame = tk.Frame(self.add_frame, bg='black')
        name_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.name_entry = tk.Entry(name_frame, bd=0, font=("Calibri", 12))
        self.name_entry.pack(padx=3, pady=3)  # Increased padding for thicker border

        # Age
        ttk.Label(self.add_frame, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        age_frame = tk.Frame(self.add_frame, bg='black')
        age_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.age_entry = tk.Entry(age_frame, bd=0, font=("Calibri", 12))
        self.age_entry.pack(padx=3, pady=3)  # Increased padding

        # Gender
        ttk.Label(self.add_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.gender_combobox = ttk.Combobox(self.add_frame, state="readonly", font=("Calibri", 12))
        self.gender_combobox['values'] = ("Male", "Female", "Other")
        self.gender_combobox.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Contact
        ttk.Label(self.add_frame, text="Contact:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        contact_frame = tk.Frame(self.add_frame, bg='black')
        contact_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.contact_entry = tk.Entry(contact_frame, bd=0, font=("Calibri", 12))
        self.contact_entry.pack(padx=3, pady=3)  # Increased padding

        # House Number
        ttk.Label(self.add_frame, text="House Number:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        hno_frame = tk.Frame(self.add_frame, bg='black')
        hno_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.hno_entry = tk.Entry(hno_frame, bd=0, font=("Calibri", 12))
        self.hno_entry.pack(padx=3, pady=3)  # Increased padding

        # Locality
        ttk.Label(self.add_frame, text="Locality:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        locality_frame = tk.Frame(self.add_frame, bg='black')
        locality_frame.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.locality_entry = tk.Entry(locality_frame, bd=0, font=("Calibri", 12))
        self.locality_entry.pack(padx=3, pady=3)  # Increased padding

        # Pincode
        ttk.Label(self.add_frame, text="Pincode:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        pincode_frame = tk.Frame(self.add_frame, bg='black')
        pincode_frame.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.pincode_entry = tk.Entry(pincode_frame, bd=0, font=("Calibri", 12))
        self.pincode_entry.pack(padx=3, pady=3)  # Increased padding

        # Add Patient Button
        self.add_button = ttk.Button(self.add_tab, text="Add Patient", padding=10, command=self.add_patient)
        self.add_button.pack(pady=10)

        # Update Patient Tab Widgets
        self.update_frame = ttk.LabelFrame(self.update_tab, text="Update Patient Information")
        self.update_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(3):
            self.update_frame.rowconfigure(i, weight=1)
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=2)

        # Patient ID
        ttk.Label(self.update_frame, text="Patient ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        id_frame = tk.Frame(self.update_frame, bg='black')
        id_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.patient_id_entry = tk.Entry(id_frame, bd=0, font=("Calibri", 12))
        self.patient_id_entry.pack(padx=3, pady=3)  # Increased padding

        # Field to Update
        ttk.Label(self.update_frame, text="Field to Update:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.field_combobox = ttk.Combobox(self.update_frame, state="readonly", font=("Calibri", 12))
        self.field_combobox['values'] = ("Name", "Age", "Gender", "Contact", "House Number", "Locality", "Pincode")
        self.field_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # New Value
        ttk.Label(self.update_frame, text="New Value:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        new_value_frame = tk.Frame(self.update_frame, bg='black')
        new_value_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.new_value_entry = tk.Entry(new_value_frame, bd=0, font=("Calibri", 12))
        self.new_value_entry.pack(padx=3, pady=3)  # Increased padding

        # Update Button
        self.update_button = ttk.Button(self.update_tab, text="Update", padding=10, command=self.perform_update)
        self.update_button.pack(pady=10)

        # View Patient by ID Widgets
        self.view_frame = ttk.LabelFrame(self.view_tab, text="Search Patient")
        self.view_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.columnconfigure(1, weight=2)

        # Enter Patient ID
        ttk.Label(self.view_frame, text="Enter Patient ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        search_id_frame = tk.Frame(self.view_frame, bg='black')
        search_id_frame.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.search_id_entry = tk.Entry(search_id_frame, bd=0, font=("Calibri", 12))
        self.search_id_entry.pack(padx=3, pady=3)  # Increased padding

        # Search Button
        self.search_button = ttk.Button(self.view_frame, text="Search Patient", padding=10, command=self.view_patient_by_id)
        self.search_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Patient Details Frame
        self.patient_details_frame = ttk.LabelFrame(self.view_tab, text="Patient Details")
        self.patient_details_frame.pack(padx=20, pady=10, fill='both', expand=True)

        details_labels = ["ID:", "Name:", "Age:", "Gender:", "Contact:", "House Number:", "Locality:", "Pincode:"]
        self.patient_detail_labels = []
        for i, label_text in enumerate(details_labels):
            label = ttk.Label(self.patient_details_frame, text=label_text)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            value_label = ttk.Label(self.patient_details_frame, text="")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=5)
            self.patient_detail_labels.append(value_label)

        # Configure grid layout for patient details
        self.patient_details_frame.columnconfigure(0, weight=1)
        self.patient_details_frame.columnconfigure(1, weight=2)

    def setup_all_patients_tab(self):
        columns = ("ID", "Name", "Age", "Gender", "Contact", "House Number", "Locality", "Pincode")
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
        
        if not name or not age or not gender or not contact or not hno or not locality or not pincode:
            messagebox.showwarning("Input Error", "All fields are required")
            return
        
        if any(char.isdigit() for char in name):
            messagebox.showerror("Input Error", "Name cannot contain numbers or special characters.")
            return
        
        if not (0 <= int(age) < 120):
            messagebox.showerror("Input Error", "Enter a valid age.")
            return

        if len(str(contact)) != 10:
            messagebox.showerror("Input Error", "Phone number must be 10 digits.")
            return
        
        if len(str(pincode)) != 6:
            messagebox.showerror("Input Error", "Pincode must be 6 digits.")
            return
        
        try:
            db = connect_db()
            cursor = db.cursor()
            query = '''INSERT INTO patient_det (name, age, gender, phone_number, house_number, locality, pincode)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(query, (name, age, gender, contact, hno, locality, pincode))
            db.commit()
            messagebox.showinfo("Success", "Patient added successfully!")
            db.close()
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
            "Contact": "phone_number",
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
        self.root.geometry("900x700")
        self.root.configure(bg="#e6f2ff")  # Light blue background

        # Configure style for a modern look
        style = ttk.Style()
        style.theme_use("clam")  # Using 'clam' theme for consistency

        # Set styles for widgets
        style.configure("TFrame", background="#e6f2ff")
        style.configure("TNotebook", background="#e6f2ff", tabposition='n')
        style.configure("TNotebook.Tab", font=("Calibri", 12, "bold"))
        style.configure("TLabelFrame", background="#e6f2ff")
        style.configure("TLabelFrame.Label", font=("Calibri", 14, "bold"))
        style.configure("TLabel", background="#e6f2ff", font=("Calibri", 12))
        style.configure("TEntry", font=("Calibri", 12))
        style.configure("TCombobox", font=("Calibri", 12))
        style.configure("TButton", font=("Calibri", 12, "bold"), foreground="white")
        style.map("TButton",
                  background=[('!disabled', '#4CAF50'), ('active', '#45a049')],
                  foreground=[('!disabled', 'white')])

        # Notebook widget (tabs)
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, padx=10, fill='both', expand=True)

        # Create Tabs for Add, Update, View, All Doctors
        self.add_tab = ttk.Frame(notebook)
        self.update_tab = ttk.Frame(notebook)
        self.view_tab = ttk.Frame(notebook)
        self.all_doctors_tab = ttk.Frame(notebook)
        self.setup_all_doctors_tab()

        notebook.add(self.add_tab, text="Add Doctor")
        notebook.add(self.update_tab, text="Update Doctor")
        notebook.add(self.view_tab, text="View Doctor by ID")
        notebook.add(self.all_doctors_tab, text="All Doctors")

        # Add Doctor Tab Widgets
        self.add_frame = ttk.LabelFrame(self.add_tab, text="Add New Doctor")
        self.add_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(12):
            self.add_frame.rowconfigure(i, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=2)

        # Doctor Name
        ttk.Label(self.add_frame, text="Doctor Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Department
        ttk.Label(self.add_frame, text="Department:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.department_entry = ttk.Entry(self.add_frame)
        self.department_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Date of Birth
        ttk.Label(self.add_frame, text="Date of Birth [YYYY-MM-DD]:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.DOB_entry = ttk.Entry(self.add_frame)
        self.DOB_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Gender
        ttk.Label(self.add_frame, text="Gender:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.gender_combobox = ttk.Combobox(self.add_frame, state="readonly")
        self.gender_combobox['values'] = ("Male", "Female", "Other")
        self.gender_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Contact
        ttk.Label(self.add_frame, text="Contact:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.contact_entry = ttk.Entry(self.add_frame)
        self.contact_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # House Number
        ttk.Label(self.add_frame, text="House Number:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.hno_entry = ttk.Entry(self.add_frame)
        self.hno_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Locality
        ttk.Label(self.add_frame, text="Locality:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.locality_entry = ttk.Entry(self.add_frame)
        self.locality_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Pincode
        ttk.Label(self.add_frame, text="Pincode:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.pincode_entry = ttk.Entry(self.add_frame)
        self.pincode_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Qualifications
        ttk.Label(self.add_frame, text="Qualifications:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.qualifications_entry = ttk.Entry(self.add_frame)
        self.qualifications_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        # Experience
        ttk.Label(self.add_frame, text="Experience [years]:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
        self.experience_entry = ttk.Entry(self.add_frame)
        self.experience_entry.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # Aadhar Number
        ttk.Label(self.add_frame, text="Aadhar No.:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
        self.aadhar_entry = ttk.Entry(self.add_frame)
        self.aadhar_entry.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        # Add Doctor Button
        self.add_button = ttk.Button(self.add_tab, text="Add Doctor", command=self.add_doctor)
        self.add_button.pack(pady=10)

        # Update Doctor Tab Widgets
        self.update_frame = ttk.LabelFrame(self.update_tab, text="Update Doctor Information")
        self.update_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(3):
            self.update_frame.rowconfigure(i, weight=1)
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=2)

        # Doctor ID
        ttk.Label(self.update_frame, text="Doctor ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.doctor_id_entry = ttk.Entry(self.update_frame)
        self.doctor_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Field to Update
        ttk.Label(self.update_frame, text="Field to Update:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.field_combobox = ttk.Combobox(self.update_frame, state="readonly")
        self.field_combobox['values'] = ("Name", "Department", "DOB", "Gender", "Contact", "House Number", "Locality", "Pincode", "Qualifications", "Experience", "Aadhar Number")
        self.field_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # New Value
        ttk.Label(self.update_frame, text="New Value:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.new_value_entry = ttk.Entry(self.update_frame)
        self.new_value_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Update Button
        update_button = ttk.Button(self.update_tab, text="Update", command=self.perform_update)
        update_button.pack(pady=10)

        # View Doctor by ID Widgets
        self.view_frame = ttk.LabelFrame(self.view_tab, text="Search Doctor")
        self.view_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.columnconfigure(1, weight=2)

        # Enter Doctor ID
        ttk.Label(self.view_frame, text="Enter Doctor ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.search_id_entry = ttk.Entry(self.view_frame)
        self.search_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Search Button
        search_button = ttk.Button(self.view_frame, text="Search Doctor", command=self.view_doctor_by_id)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Doctor Details Frame
        self.doctor_details_frame = ttk.LabelFrame(self.view_tab, text="Doctor Details")
        self.doctor_details_frame.pack(padx=20, pady=10, fill='both', expand=True)

        # Labels for displaying doctor details
        details_labels = ["ID:", "Name:", "Department:", "DOB:", "Gender:", "Contact:", "House Number:", "Locality:", "Pincode:", "Qualifications:", "Experience:", "Aadhar Number:"]
        self.doctor_detail_labels = []
        for i, label_text in enumerate(details_labels):
            ttk.Label(self.doctor_details_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            value_label = ttk.Label(self.doctor_details_frame, text="")
            value_label.grid(row=i, column=1, sticky="w", padx=10, pady=2)
            self.doctor_detail_labels.append(value_label)

    def setup_all_doctors_tab(self):
        # Treeview widget for displaying all doctors
        columns = ("ID", "Name", "Department", "DOB", "Gender", "Contact", "House Number", "Locality", "Pincode", "Qualifications", "Experience", "Aadhar")
        self.doctor_tree = ttk.Treeview(self.all_doctors_tab, columns=columns, show="headings")
        for col in columns:
            self.doctor_tree.heading(col, text=col)
            self.doctor_tree.column(col, width=100, anchor="center")

        # Place the Treeview widget on the tab with scrollbar
        self.doctor_tree.pack(fill="both", expand=True, padx=10, pady=10)
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

from tkinter import Canvas, PhotoImage, ttk

from PIL import Image, ImageTk  # You'll need to install Pillow: `pip install pillow`

class AppointmentSegment:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Segment")
        self.root.geometry("800x600")

        # Load the original background image
        self.original_image = Image.open("d:\\Downloads\\dsa-notes-main\\FDF5C4_600x600_crop_center.png")

        # Create a Canvas widget
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Bind the resize event to a function
        self.root.bind("<Configure>", self.resize_background)

        # Configure style for a modern look
        style = ttk.Style()
        style.theme_use("clam")  # Using 'clam' theme for consistency

        # Set styles for widgets
        style.configure("TFrame", background="#e6f2ff")
        style.configure("TNotebook", background="#e6f2ff", tabposition='n')
        style.configure("TNotebook.Tab", font=("Calibri", 12, "bold"))
        style.configure("TLabelFrame", background="#e6f2ff")
        style.configure("TLabelFrame.Label", font=("Calibri", 14, "bold"))
        style.configure("TLabel", background="#e6f2ff", font=("Calibri", 12))
        style.configure("TEntry", font=("Calibri", 12))
        style.configure("TCombobox", font=("Calibri", 12))
        style.configure("TButton", font=("Calibri", 12, "bold"), foreground="white")
        style.map("TButton",
                  background=[('!disabled', '#4CAF50'), ('active', '#45a049')],
                  foreground=[('!disabled', 'white')])

        # Notebook widget (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.place(in_=self.canvas, x=10, y=10, relwidth=0.96, relheight=0.9)  # Place notebook on canvas

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

    def resize_background(self, event):
        # Resize the image to fit the new window size
        resized_image = self.original_image.resize((event.width, event.height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Update the canvas background image
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        self.canvas.lower("all")  # Ensure the image is in the background

    def setup_create_appointment_tab(self):
        self.create_frame = ttk.LabelFrame(self.create_tab, text="Create New Appointment")
        self.create_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        for i in range(6):
            self.create_frame.rowconfigure(i, weight=1)
        self.create_frame.columnconfigure(0, weight=1)
        self.create_frame.columnconfigure(1, weight=2)

        # Department Dropdown
        ttk.Label(self.create_frame, text="Department:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.department_combobox = ttk.Combobox(self.create_frame, width=28, state="readonly")
        self.department_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.department_combobox.bind("<<ComboboxSelected>>", self.update_doctor_dropdown)

        # Doctor Dropdown
        ttk.Label(self.create_frame, text="Doctor:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.doctor_combobox = ttk.Combobox(self.create_frame, width=28, state="readonly")
        self.doctor_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.doctor_combobox.bind("<<ComboboxSelected>>", self.update_time_slots)

        # Patient ID Entry
        ttk.Label(self.create_frame, text="Patient ID:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.patient_entry = ttk.Entry(self.create_frame)
        self.patient_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Appointment Date Entry
        ttk.Label(self.create_frame, text="Appointment Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = ttk.Entry(self.create_frame)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.date_entry.bind("<FocusOut>", self.update_time_slots)

        # Available Time Slots Dropdown
        ttk.Label(self.create_frame, text="Available Time Slots:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.time_combobox = ttk.Combobox(self.create_frame, width=28, state="readonly")
        self.time_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Create Appointment Button
        self.create_button = ttk.Button(self.create_tab, text="Create Appointment", command=self.create_appointment)
        self.create_button.pack(pady=10)

        self.load_departments()

    def setup_delete_appointment_tab(self):
        self.delete_frame = ttk.LabelFrame(self.delete_tab, text="Delete Appointment")
        self.delete_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Configure grid layout
        self.delete_frame.rowconfigure(0, weight=1)
        self.delete_frame.columnconfigure(0, weight=1)
        self.delete_frame.columnconfigure(1, weight=2)

        # Appointment ID Entry
        ttk.Label(self.delete_frame, text="Appointment ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.appointment_id_entry = ttk.Entry(self.delete_frame)
        self.appointment_id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Delete Appointment Button
        self.delete_button = ttk.Button(self.delete_tab, text="Delete Appointment", command=self.delete_appointment)
        self.delete_button.pack(pady=10)

    def setup_view_appointments_tab(self):
        # Treeview widget to display appointments
        columns = ("ID", "Patient ID", "Doctor ID", "Doctor Name", "Department", "Date", "Time")
        self.appointment_tree = ttk.Treeview(self.view_tab, columns=columns, show="headings")

        for col in columns:
            self.appointment_tree.heading(col, text=col)
            self.appointment_tree.column(col, width=100, anchor="center")

        # Place the Treeview widget on the tab with scrollbar
        self.appointment_tree.pack(fill="both", expand=True, padx=10, pady=10)
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
