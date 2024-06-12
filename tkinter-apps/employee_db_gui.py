import tkinter.messagebox
from tkinter import *
from sqlite3 import *
import os


root = Tk()
root.title("Employee Database Editor")
database = "employee_db.db"

if not os.path.isfile(os.path.join(r"C:\Users\shrey\PycharmProjects\pythonProject", database)):
    db_init = connect(database)
    c_init = db_init.cursor()
    c_init.execute("""CREATE TABLE employee (
              empid text,
              fname text,
              lname text,
              age text,
              exp text,
              address text
              )""")
    db_init.commit()
    db_init.close()


class BaseWindow:
    def __init__(self, master):
        self.master = master
        self.records = []
        self.display_record = ""
        # separate window for edit information
        self.editor_window = None
        self.edit_fname_label = None
        self.edit_lname_label = None
        self.edit_age_label = None
        self.edit_exp_label = None
        self.edit_address_label = None

        self.edit_fname_entry = None
        self.edit_lname_entry = None
        self.edit_age_entry = None
        self.edit_exp_entry = None
        self.edit_address_entry = None

        self.update_button = None

        # 4 frames - add, delete, edit, show
        # add information frame
        # input field labels
        self.add_frame = LabelFrame(master, text="Add employee details", padx=20, pady=20)
        self.add_frame.grid(row=0, column=0, padx=20, pady=20, columnspan=2, rowspan=50)

        self.empid_label = Label(self.add_frame, text="Employee ID :")
        self.fname_label = Label(self.add_frame, text="First name :")
        self.lname_label = Label(self.add_frame, text="Last name :")
        self.age_label = Label(self.add_frame, text="Age :")
        self.exp_label = Label(self.add_frame, text="Work experience :")
        self.address_label = Label(self.add_frame, text="Address :")

        self.empid_label.grid(row=0, column=0, sticky="e", padx=10)
        self.fname_label.grid(row=1, column=0, sticky="e", padx=10)
        self.lname_label.grid(row=2, column=0, sticky="e", padx=10)
        self.age_label.grid(row=3, column=0, sticky="e", padx=10)
        self.exp_label.grid(row=4, column=0, sticky="e", padx=10)
        self.address_label.grid(row=5, column=0, sticky="e", padx=10)

        # input field entries
        self.empid_entry = Entry(self.add_frame, width=35)
        self.fname_entry = Entry(self.add_frame, width=35)
        self.lname_entry = Entry(self.add_frame, width=35)
        self.age_entry = Entry(self.add_frame, width=35)
        self.exp_entry = Entry(self.add_frame, width=35)
        self.address_entry = Entry(self.add_frame, width=35)

        self.empid_entry.grid(row=0, column=1, padx=10)
        self.fname_entry.grid(row=1, column=1, padx=10)
        self.lname_entry.grid(row=2, column=1, padx=10)
        self.age_entry.grid(row=3, column=1, padx=10)
        self.exp_entry.grid(row=4, column=1, padx=10)
        self.address_entry.grid(row=5, column=1, padx=10)

        # submit entries into database
        self.submit_button = Button(self.add_frame, text="Submit", command=self.submit_fields, padx=5, pady=5)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=5)
        
        # delete information frame
        self.delete_frame = LabelFrame(master, text="Delete employee details", padx=20, pady=10)
        self.delete_frame.grid(row=30, column=2, padx=20, pady=10, columnspan=2)

        # taking employee id of record to be deleted
        self.delete_id_label = Label(self.delete_frame, text="Enter employee ID :")
        self.delete_id_label.grid(row=0, column=0, sticky="e", padx=10)

        self.delete_id_entry = Entry(self.delete_frame, width=35)
        self.delete_id_entry.grid(row=0, column=1, padx=10)

        self.delete_button = Button(self.delete_frame, text="Delete", command=lambda:
                                    self.delete_field(self.delete_id_entry.get()), padx=5, pady=5)
        self.delete_button.grid(row=1, column=0, columnspan=2, pady=5)

        # edit information frame
        self.edit_frame = LabelFrame(master, text="Edit employee details", padx=20, pady=10)
        self.edit_frame.grid(row=25, column=2, padx=20, pady=10, columnspan=2)

        self.edit_id_label = Label(self.edit_frame, text="Enter employee ID :")
        self.edit_id_label.grid(row=0, column=0, sticky="e", padx=10)

        self.edit_id_entry = Entry(self.edit_frame, width=35)
        self.edit_id_entry.grid(row=0, column=1, padx=10)

        self.edit_button = Button(self.edit_frame, text="Edit", command=lambda:
                                  self.edit_field(self.edit_id_entry.get()), padx=5, pady=5)
        self.edit_button.grid(row=1, column=0, columnspan=2, pady=5)

        # show information frame

        self.show_frame = LabelFrame(master, text="Show employee details", padx=20, pady=20)
        self.show_frame.grid(row=50, column=0, padx=20, pady=10, columnspan=2)

        self.show_id_label = Label(self.show_frame, text="Enter employee ID :")
        self.show_id_label.grid(row=0, column=0, sticky="e", padx=10)

        self.show_id_entry = Entry(self.show_frame, width=35)
        self.show_id_entry.grid(row=0, column=1, padx=10)

        self.show_button = Button(self.show_frame, text="Display employee details", command=lambda:
                                  self.show_field(self.show_id_entry.get()), padx=5, pady=5)

        self.show_button.grid(row=1, column=0, columnspan=2, pady=10)

        # show full table

        self.show_button2 = Button(master, text="Display employee table", command=lambda:
                                   self.show_field("ALL"), padx=20, pady=20)

        self.show_button2.grid(row=50, column=2, columnspan=2, pady=20, padx=20)

    def submit_fields(self):
        db = connect(database)
        c = db.cursor()

        c.execute("SELECT * FROM employee WHERE empid = ?", (self.empid_entry.get(),))
        self.records = c.fetchone()

        if not self.records:
            c.execute("INSERT INTO employee VALUES (?,?,?,?,?,?)",
                      (self.empid_entry.get(),
                       self.fname_entry.get(),
                       self.lname_entry.get(),
                       self.age_entry.get(),
                       self.exp_entry.get(),
                       self.address_entry.get(),
                       ))
        else:
            tkinter.messagebox.showerror("Error", "Employee ID already exists")

        db.commit()
        db.close()

        self.empid_entry.delete(0, END)
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.exp_entry.delete(0, END)
        self.address_entry.delete(0, END)

    def delete_field(self, delete_id):
        db = connect(database)
        c = db.cursor()

        c.execute("DELETE FROM employee WHERE empid = ?", (delete_id,))

        db.commit()
        db.close()

        self.delete_id_entry.delete(0, END)

    def edit_field(self, edit_id):
        db = connect(database)
        c = db.cursor()

        c.execute("SELECT * FROM employee WHERE empid = ?", (edit_id,))
        self.records = c.fetchone()

        db.commit()
        db.close()
        if self.records:
            self.editor_window = Toplevel()
            self.editor_window.title("Edit employee information")

            self.edit_fname_label = Label(self.editor_window, text="First name :")
            self.edit_lname_label = Label(self.editor_window, text="Last name :")
            self.edit_age_label = Label(self.editor_window, text="Age :")
            self.edit_exp_label = Label(self.editor_window, text="Work experience :")
            self.edit_address_label = Label(self.editor_window, text="Address :")

            self.edit_fname_label.grid(row=1, column=0, sticky="e", padx=10)
            self.edit_lname_label.grid(row=2, column=0, sticky="e", padx=10)
            self.edit_age_label.grid(row=3, column=0, sticky="e", padx=10)
            self.edit_exp_label.grid(row=4, column=0, sticky="e", padx=10)
            self.edit_address_label.grid(row=5, column=0, sticky="e", padx=10)

            self.edit_fname_entry = Entry(self.editor_window, width=35)
            self.edit_lname_entry = Entry(self.editor_window, width=35)
            self.edit_age_entry = Entry(self.editor_window, width=35)
            self.edit_exp_entry = Entry(self.editor_window, width=35)
            self.edit_address_entry = Entry(self.editor_window, width=35)

            self.edit_fname_entry.grid(row=1, column=1, padx=10)
            self.edit_lname_entry.grid(row=2, column=1, padx=10)
            self.edit_age_entry.grid(row=3, column=1, padx=10)
            self.edit_exp_entry.grid(row=4, column=1, padx=10)
            self.edit_address_entry.grid(row=5, column=1, padx=10)

            # submit entries into database
            self.update_button = Button(self.editor_window, text="Confirm edit",
                                        command=lambda: self.update(edit_id), padx=5, pady=5)
            self.update_button.grid(row=6, column=0, columnspan=2, pady=5)

        else:
            tkinter.messagebox.showerror("Error", "Employee ID does not exist")

        self.edit_id_entry.delete(0, END)

    def update(self, upd_id):
        db = connect(database)
        c = db.cursor()
        c.execute("""UPDATE employee SET
                     fname = ?,
                     lname = ?,
                     age = ?,
                     exp = ?,
                     address = ?
                     WHERE empid = ?""",
                  (self.edit_fname_entry.get(),
                   self.edit_lname_entry.get(),
                   self.edit_age_entry.get(),
                   self.edit_exp_entry.get(),
                   self.edit_address_entry.get(),
                   upd_id))
        db.commit()
        db.close()
        self.editor_window.destroy()
        tkinter.messagebox.showinfo("Edit complete", "Information for Employee ID " + upd_id +
                                    " updated.")

    def show_field(self, show_id):
        self.display_record = ""
        db = connect(database)
        c = db.cursor()

        if show_id == "ALL":
            c.execute("SELECT * FROM employee")
            self.records = c.fetchall()

            for record in self.records:
                self.display_record += str(record) + "\n"
            tkinter.messagebox.showinfo("Employee table dataset", self.display_record)

        elif show_id and show_id != "ALL":
            c.execute("SELECT * FROM employee WHERE empid = ?", (show_id,))
            self.records = c.fetchone()

            if self.records:
                self.display_record += ("Employee ID : " + self.records[0] + "\nName : " + self.records[1]
                                        + " " + self.records[2] + "\nAge : " + self.records[3] + "\nWork Experience : "
                                        + self.records[4] + "\nAddress : " + self.records[5])
                tkinter.messagebox.showinfo("Employee ID " + show_id, self.display_record)
            else:
                self.display_record = ""
                tkinter.messagebox.showerror("Error", "Employee ID does not exist")

        db.commit()
        db.close()

        self.show_id_entry.delete(0, END)


emp = BaseWindow(root)
root.mainloop()
