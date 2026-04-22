import tkinter as tk  # Importing the tkinter module
from tkinter import ttk, messagebox, simpledialog # Importing the ttk, messagebox, and simpledialog modules from tkinter
import datetime as dt # Importing the datetime module
from datetime import datetime # Importing the datetime class from the datetime module
import threading # Importing the threading module
import time # Importing the time module
import os  # Importing the os module
import mysql.connector # Importing the mysql.connector module

def connect_to_db(): # This function connects to the database
    return mysql.connector.connect( # This connects to the database
        host='64.31.22.34', # This is the host of the database
        user='alwhizco_scott', # This is the username of the database
        password='lci)+E4^%1lW', # This is the password of the database
        database='alwhizco_scott' # This is the name of the database
    )

def add_student(parent): # This function adds a student to the database
    import mysql.connector
    from tkinter import messagebox, simpledialog

    add_student_first_name = simpledialog.askstring("Input", "Enter first name:", parent=parent)
    add_student_last_name = simpledialog.askstring("Input", "Enter last name:", parent=parent)
    add_student_roll_number = simpledialog.askstring("Input", "Enter roll number:", parent=parent)
    add_student_contact_number = simpledialog.askstring("Input", "Enter contact number:", parent=parent)
    add_student_date_of_birth = simpledialog.askstring("Input", "Enter date of birth (YYYY-MM-DD):", parent=parent)
    add_student_course_ID = simpledialog.askstring("Input", "Enter the course ID:", parent=parent)

    if all([add_student_first_name, add_student_last_name, add_student_roll_number, add_student_contact_number, add_student_date_of_birth, add_student_course_ID]):
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Tbl_Students (FirstName, LastName, RollNumber, ContactNumber, DateOfBirth, CourseID) VALUES (%s, %s, %s, %s, %s, %s)",
                (add_student_first_name, add_student_last_name, add_student_roll_number, add_student_contact_number, add_student_date_of_birth, add_student_course_ID)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Student added successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showwarning("Input Error", "All fields are required to be filled out", parent=parent)

        
        
def update_student(parent): # This function updates a student in the database
    import mysql.connector
    from tkinter import messagebox, simpledialog

    update_student_ID = simpledialog.askstring("Input", "Enter student ID:", parent=parent)
    update_student_first_name = simpledialog.askstring("Input", "Enter first name:", parent=parent)
    update_student_last_name = simpledialog.askstring("Input", "Enter last name:", parent=parent)
    update_student_roll_number = simpledialog.askstring("Input", "Enter roll number:", parent=parent)
    update_student_contact_number = simpledialog.askstring("Input", "Enter contact number:", parent=parent)
    update_student_date_of_birth = simpledialog.askstring("Input", "Enter date of birth (YYYY-MM-DD):", parent=parent)
    update_student_course_ID = simpledialog.askstring("Input", "Enter the course ID:", parent=parent)

    if all([update_student_ID, update_student_first_name, update_student_last_name, update_student_roll_number, update_student_contact_number, update_student_date_of_birth, update_student_course_ID]):
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE Tbl_Students SET FirstName=%s, LastName=%s, RollNumber=%s, ContactNumber=%s, DateOfBirth=%s, CourseID=%s WHERE StudentID=%s",
                (update_student_first_name, update_student_last_name, update_student_roll_number, update_student_contact_number, update_student_date_of_birth, update_student_course_ID, update_student_ID)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Student updated successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "All fields are required.", parent=parent)


def remove_student(parent): # This function removes a student from the database
    import mysql.connector
    from tkinter import messagebox, simpledialog

    remove_student_id = simpledialog.askstring("Input", "Enter student ID to delete:", parent=parent)

    if remove_student_id:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM Tbl_Students WHERE StudentID = %s", (remove_student_id,))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Student deleted successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "Student ID is required.", parent=parent)


def view_students(parent): # This function views all students in the database
    import mysql.connector
    from tkinter import messagebox

    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT StudentID, FirstName, LastName, RollNumber, ContactNumber, DateOfBirth, CourseID FROM Tbl_Students")
        students = cursor.fetchall()
        db.close()
        student_list = "\n".join([f"ID: {s[0]}, Name: {s[1]} {s[2]}, Roll: {s[3]}, Contact: {s[4]}, DOB: {s[5]}, CourseID: {s[6]}" for s in students])
        messagebox.showinfo("Students", student_list if student_list else "No students found.", parent=parent)
    except Exception as e:
        messagebox.showerror("Database Error", str(e), parent=parent)


def search_student(parent): # This function searches for a student in the database
    win = tk.Toplevel(parent)
    win.title("Search Student")
    win.geometry("900x350")

    tk.Label(win, text="Search by First Name, Last Name, or Roll Number:").pack(pady=5)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(win, textvariable=search_var)
    search_entry.pack(pady=5)

    columns = ("StudentID", "FirstName", "LastName", "RollNumber", "ContactNumber", "DateOfBirth", "CourseID")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, pady=10)

    def do_search():
        for item in tree.get_children():
            tree.delete(item)
        search_term = search_var.get()
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT StudentID, FirstName, LastName, RollNumber, ContactNumber, DateOfBirth, CourseID "
                "FROM Tbl_Students WHERE FirstName LIKE %s OR LastName LIKE %s OR RollNumber LIKE %s",
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
            results = cursor.fetchall()
            db.close()
            for row in results:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=win)

    ttk.Button(win, text="Search", command=do_search).pack(pady=5)



def add_course(parent): # This function adds a course to the database
    from tkinter import messagebox, simpledialog

    add_course_name = simpledialog.askstring("Input", "Enter course name:", parent=parent)
    add_course_teacher_ID = simpledialog.askstring("Input", "Enter teacher ID:", parent=parent)

    if add_course_name and add_course_teacher_ID:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Tbl_Courses (CourseName, TeacherID) VALUES (%s, %s)",
                (add_course_name, add_course_teacher_ID)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Course added successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showwarning("Input Error", "All fields are required to be filled out", parent=parent)


def update_course(parent): # This function updates a course in the database
    from tkinter import messagebox, simpledialog

    update_course_ID = simpledialog.askstring("Input", "Enter course ID:", parent=parent)
    update_course_name = simpledialog.askstring("Input", "Enter course name:", parent=parent)
    update_course_teacher_ID = simpledialog.askstring("Input", "Enter teacher ID:", parent=parent)

    if update_course_ID and update_course_name and update_course_teacher_ID:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE Tbl_Courses SET CourseName=%s, TeacherID=%s WHERE CourseID=%s",
                (update_course_name, update_course_teacher_ID, update_course_ID)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Course updated successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "All fields are required.", parent=parent)



def remove_course(parent): # This function removes a course from the database
    from tkinter import messagebox, simpledialog

    remove_course_ID = simpledialog.askstring("Input", "Enter Course ID to delete:", parent=parent)

    if remove_course_ID:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM Tbl_Courses WHERE CourseID = %s", (remove_course_ID,))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Course deleted successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "Course ID is required.", parent=parent)




def view_courses(parent): # This function views all courses in the database
    from tkinter import messagebox

    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT CourseID, CourseName, TeacherID FROM Tbl_Courses")
        courses = cursor.fetchall()
        db.close()
        course_list = "\n".join([f"ID: {c[0]}, Name: {c[1]}, TeacherID: {c[2]}" for c in courses])
        messagebox.showinfo("Courses", course_list if course_list else "No courses found.", parent=parent)
    except Exception as e:
        messagebox.showerror("Database Error", str(e), parent=parent)


def search_course(parent): # This function searches for a course in the database
    win = tk.Toplevel(parent)
    win.title("Search Course")
    win.geometry("700x500")

    tk.Label(win, text="Search by Course Name or Course ID:").pack(pady=5)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(win, textvariable=search_var)
    search_entry.pack(pady=5)

    columns = ("CourseID", "CourseName", "TeacherID")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    tree.pack(fill="both", expand=True, pady=10)

    def do_search():
        for item in tree.get_children():
            tree.delete(item)
        search_term = search_var.get()
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT CourseID, CourseName, TeacherID FROM Tbl_Courses "
                "WHERE CourseName LIKE %s OR CourseID LIKE %s",
                (f'%{search_term}%', f'%{search_term}%')
            )
            results = cursor.fetchall()
            db.close()
            for row in results:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=win)

    ttk.Button(win, text="Search", command=do_search).pack(pady=5)



def add_teacher(parent): # This function adds a teacher to the database
    from tkinter import messagebox, simpledialog

    add_teacher_first_name = simpledialog.askstring("Input", "Enter first name:", parent=parent)
    add_teacher_last_name = simpledialog.askstring("Input", "Enter last name:", parent=parent)
    add_teacher_contact_number = simpledialog.askstring("Input", "Enter contact number:", parent=parent)
    add_teacher_hire_date = simpledialog.askstring("Input", "Enter hire date (YYYY-MM-DD):", parent=parent)

    if add_teacher_first_name and add_teacher_last_name and add_teacher_contact_number and add_teacher_hire_date:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO Tbl_Teachers (FirstName, LastName, ContactNumber, HireDate) VALUES (%s, %s, %s, %s)",
                (add_teacher_first_name, add_teacher_last_name, add_teacher_contact_number, add_teacher_hire_date)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Teacher added successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showwarning("Input Error", "All fields are required to be filled out", parent=parent)

        
        
def update_teacher(parent): # This function updates a teacher in the database
    from tkinter import messagebox, simpledialog

    update_teacher_ID = simpledialog.askstring("Input", "Enter teacher ID:", parent=parent)
    update_teacher_first_name = simpledialog.askstring("Input", "Enter first name:", parent=parent)
    update_teacher_last_name = simpledialog.askstring("Input", "Enter last name:", parent=parent)
    update_teacher_contact_number = simpledialog.askstring("Input", "Enter contact number:", parent=parent)
    update_teacher_hire_date = simpledialog.askstring("Input", "Enter hire date (YYYY-MM-DD):", parent=parent)

    if update_teacher_ID and update_teacher_first_name and update_teacher_last_name and update_teacher_contact_number and update_teacher_hire_date:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE Tbl_Teachers SET FirstName=%s, LastName=%s, ContactNumber=%s, HireDate=%s WHERE TeacherID=%s",
                (update_teacher_first_name, update_teacher_last_name, update_teacher_contact_number, update_teacher_hire_date, update_teacher_ID)
            )
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Teacher updated successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "All fields are required.", parent=parent)



def remove_teacher(parent): # This function removes a teacher from the database
    from tkinter import messagebox, simpledialog

    remove_teacher_id = simpledialog.askstring("Input", "Enter teacher ID to delete:", parent=parent)

    if remove_teacher_id:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM Tbl_Teachers WHERE TeacherID = %s", (remove_teacher_id,))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Teacher deleted successfully!", parent=parent)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=parent)
    else:
        messagebox.showerror("Error", "Teacher ID is required.", parent=parent)



def view_teachers(parent): # This function views all teachers in the database
    from tkinter import messagebox

    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("SELECT TeacherID, FirstName, LastName, ContactNumber, HireDate FROM Tbl_Teachers")
        teachers = cursor.fetchall()
        db.close()
        teacher_list = "\n".join([f"ID: {t[0]}, Name: {t[1]} {t[2]}, Contact: {t[3]}, Hire Date: {t[4]}" for t in teachers])
        messagebox.showinfo("Teachers", teacher_list if teacher_list else "No teachers found.", parent=parent)
    except Exception as e:
        messagebox.showerror("Database Error", str(e), parent=parent)


def search_teacher(parent): # This function searches for a teacher in the database
    win = tk.Toplevel(parent)
    win.title("Search Teacher")
    win.geometry("800x500")

    tk.Label(win, text="Search by First Name, Last Name, or Teacher ID:").pack(pady=5)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(win, textvariable=search_var)
    search_entry.pack(pady=5)

    columns = ("TeacherID", "FirstName", "LastName", "ContactNumber", "HireDate")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    def do_search():
        for item in tree.get_children():
            tree.delete(item)
        search_term = search_var.get()
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT TeacherID, FirstName, LastName, ContactNumber, HireDate FROM Tbl_Teachers "
                "WHERE FirstName LIKE %s OR LastName LIKE %s OR TeacherID LIKE %s",
                (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%')
            )
            results = cursor.fetchall()
            db.close()
            for row in results:
                tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Database Error", str(e), parent=win)

    ttk.Button(win, text="Search", command=do_search).pack(pady=5)


def menu_window():
    menu = tk.Toplevel(root)
    menu.geometry("1500x1000")
    menu.title("Menu window")
    tk.Label(menu,text="Menu window", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=3, pady=20)

    for col in range(3):
        menu.grid_columnconfigure(col, weight=1)

    add_student_01=tk.StringVar()
    add_student_02=tk.StringVar()
    add_student_03=tk.StringVar()
    add_student_04=tk.StringVar()
    add_student_05=tk.StringVar()
    add_student_06=tk.StringVar()
    add_student_07=tk.StringVar()

    update_student_01=tk.StringVar()
    update_student_02=tk.StringVar()
    update_student_03=tk.StringVar()
    update_student_04=tk.StringVar()
    update_student_05=tk.StringVar()
    update_student_06=tk.StringVar()
    update_student_07=tk.StringVar()

    remove_student_01=tk.StringVar()
    remove_student_02=tk.StringVar()
    remove_student_03=tk.StringVar()
    remove_student_04=tk.StringVar()
    remove_student_05=tk.StringVar()
    remove_student_06=tk.StringVar()
    remove_student_07=tk.StringVar()
    
    btn_addstudent =ttk.Button(menu,text="Add_student", command=lambda: add_student(menu)).grid(row=1,column=0)

    btn_update_student =ttk.Button(menu,text="Update student", command=lambda: update_student(menu)).grid(row=2,column=0)   

    btn_remove_student =ttk.Button(menu, text="Remove student", command=lambda: remove_student(menu)).grid(row=3,column=0) 
   
    btn_view_students =ttk.Button(menu,text="View_students", command=lambda: view_students(menu)).grid(row=4,column=0)

    btn_search_students =ttk.Button(menu,text="Search_students", command=lambda: search_student(menu)).grid(row=5,column=0)

    
    btn_addcourse =ttk.Button(menu,text="Add_course", command=lambda: add_course(menu)).grid(row=1,column=1)
    
    btn_update_course =ttk.Button(menu,text="Update course", command=lambda: update_course(menu)).grid(row=2,column=1)   

    btn_remove_course =ttk.Button(menu, text="Remove course", command=lambda: remove_course(menu)).grid(row=3,column=1) 
   
    btn_view_courses =ttk.Button(menu,text="View_courses", command=lambda: view_courses(menu)).grid(row=4,column=1)

    btn_search_courses =ttk.Button(menu,text="Search_courses", command=lambda: search_course(menu)).grid(row=5,column=1)

    
    btn_addteacher =ttk.Button(menu,text="Add_teacher", command=lambda: add_teacher(menu)).grid(row=1,column=2)

    btn_update_teacher =ttk.Button(menu,text="Update teacher", command=lambda: update_teacher(menu)).grid(row=2,column=2)   

    btn_remove_teacher =ttk.Button(menu, text="Remove teacher", command=lambda: remove_teacher(menu)).grid(row=3,column=2) 
   
    btn_view_teachers =ttk.Button(menu,text="View_teachers", command=lambda: view_teachers(menu)).grid(row=4,column=2)

    btn_search_teachers =ttk.Button(menu,text="Search_teachers", command=lambda: search_teacher(menu)).grid(row=5,column=2)

def login(): # Thisis the login function which checks if the username and password are correct

    if username.get() == "admin" and password.get() == "password": # This checks if the username and password are correct
        menu_window()
    else:
        messagebox.showinfo("Wrong password", f"Access denied")


root = tk.Tk() # This creates the main window
root.title("Login window")
root.geometry("350x150") # This sets the size of the window

username=tk.StringVar()
password=tk.StringVar()
 
lbl_username = ttk.Label(root, text = "Username: ").grid(row=0,column=0,padx=10,pady=20,sticky="W")
txt_for_username= ttk.Entry(root, width = 25, textvariable = username ).grid(row=0,column=1,padx=10,pady=20)
 
lbl_password= ttk.Label(root, text = "Password: ").grid(row=1,column=0,padx=10,sticky="W")
txt_for_password = ttk.Entry(root, width = 25, textvariable = password).grid(row=1,column=1)
 
btn_login = ttk.Button(root, text = "Login", command = login).grid(row=4,column=0,pady=20, columnspan=2)

root.mainloop() # This runs the main window