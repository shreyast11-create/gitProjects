from tkinter import *


root = Tk()
root.title("To Do List")


class ToDo:
    def __init__(self, master):
        self.master = master

        # frame for listbox and scrollbar
        self.frame = LabelFrame(master, text="Work Items", padx=5)
        self.frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.title = Label(master, text="Add your pending work item below", padx=10, pady=10)
        self.title.grid(row=0, column=0, columnspan=2, padx=4)

        # entry box to enter work item
        self.entry = Entry(master, width=35)
        self.entry.grid(row=1, column=0, sticky="ns", padx=4)

        # button to add item
        self.add_button = Button(master, text="Add", command=lambda: self.add_item(self.entry.get()), padx=10, pady=5)
        self.add_button.grid(row=1, column=1, sticky="we", padx=4)

        # scrollbar for list box
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)

        # listbox for display
        self.listbox = Listbox(self.frame, width=40, yscrollcommand=self.scrollbar.set, selectmode=MULTIPLE)

        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.pack(pady=4)

        # delete highlighted entry from listbox
        self.delete_button = Button(master, text="Highlighted task(s) complete", command=lambda: self.delete_items(),
                                    padx=10, pady=4)
        self.delete_button.grid(row=3, column=0, pady=4)

        # button to select all items
        self.select_all_button = Button(master, text="Select All", command=lambda: self.select_all(),
                                        pady=4)
        self.select_all_button.grid(row=3, column=1, padx=8, pady=4)

    def add_item(self, item):
        self.listbox.insert(END, item)
        self.entry.delete(0, END)

    def delete_items(self):
        for index in reversed(self.listbox.curselection()):
            self.listbox.delete(index)

    def select_all(self):
        self.listbox.selection_set(0, END)


t = ToDo(root)
root.mainloop()
