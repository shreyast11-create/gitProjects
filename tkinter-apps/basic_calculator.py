from tkinter import *
from math import sqrt


root = Tk()
root.title("Basic Calculator")


class Calculator:
    def __init__(self, master):
        self.entry = Entry(master, width=40, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.operator = ""
        self.expression = [0.0, 0.0]
        self.error_check = ""
        self.valid_input = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        self.button1 = Button(master, padx=35, pady=10, text="1", command=lambda: self.input_operand(1))
        self.button2 = Button(master, padx=35, pady=10, text="2", command=lambda: self.input_operand(2))
        self.button3 = Button(master, padx=35, pady=10, text="3", command=lambda: self.input_operand(3))
        self.button4 = Button(master, padx=35, pady=10, text="4", command=lambda: self.input_operand(4))
        self.button5 = Button(master, padx=35, pady=10, text="5", command=lambda: self.input_operand(5))
        self.button6 = Button(master, padx=35, pady=10, text="6", command=lambda: self.input_operand(6))
        self.button7 = Button(master, padx=35, pady=10, text="7", command=lambda: self.input_operand(7))
        self.button8 = Button(master, padx=35, pady=10, text="8", command=lambda: self.input_operand(8))
        self.button9 = Button(master, padx=35, pady=10, text="9", command=lambda: self.input_operand(9))
        self.button0 = Button(master, padx=35, pady=10, text="0", command=lambda: self.input_operand(0))

        self.button_add = Button(master, padx=35, pady=10, text="+", command=lambda: self.get_operator("+"))
        self.button_subtract = Button(master, padx=35, pady=10, text="-", command=lambda: self.get_operator("-"))
        self.button_multiply = Button(master, padx=35, pady=10, text="*", command=lambda: self.get_operator("*"))
        self.button_divide = Button(master, padx=35, pady=10, text="/", command=lambda: self.get_operator("/"))
        self.button_clear = Button(master, padx=35, pady=10, text="C", command=self.clear_entry)
        self.button_equal = Button(master, padx=35, pady=10, text="=", command=self.equal)
        self.button_decimal = Button(master, padx=35, pady=10, text=".", command=lambda: self.input_operand("."))
        self.button_square = Button(master, padx=28, pady=10, text="x^2", command=self.square)
        self.button_sqrt = Button(master, padx=23, pady=10, text="x^1/2", command=self.sqroot)

        self.button1.grid(row=4, column=0)
        self.button2.grid(row=4, column=1)
        self.button3.grid(row=4, column=2)

        self.button4.grid(row=3, column=0)
        self.button5.grid(row=3, column=1)
        self.button6.grid(row=3, column=2)

        self.button7.grid(row=2, column=0)
        self.button8.grid(row=2, column=1)
        self.button9.grid(row=2, column=2)

        self.button0.grid(row=5, column=1)

        self.button_add.grid(row=4, column=3)
        self.button_subtract.grid(row=3, column=3)
        self.button_multiply.grid(row=2, column=3)
        self.button_divide.grid(row=1, column=3)
        self.button_square.grid(row=1, column=0)
        self.button_sqrt.grid(row=1, column=1)

        self.button_clear.grid(row=1, column=2)
        self.button_decimal.grid(row=5, column=2)
        self.button_equal.grid(row=5, column=3)

    def input_operand(self, number):
        current = self.entry.get()
        self.entry.delete(0, END)
        self.entry.insert(0, str(current)+str(number))

    def get_operator(self, operator):
        try:
            self.expression[0] = float(self.entry.get())
        except ValueError as err:
            self.error_check = err
            self.entry.delete(0, END)
            self.entry.insert(0, str(self.error_check))
            self.error_check = ""
            return
        self.operator = operator
        self.entry.delete(0, END)

    def clear_entry(self):
        self.entry.delete(0, END)
        self.expression[0] = 0.0
        self.expression[1] = 0.0
        self.operator = ""
        self.error_check = ""

    def evaluate(self):
        if self.operator == "+":
            self.expression[0] += self.expression[1]
            self.expression[1] = 0
        elif self.operator == "-":
            self.expression[0] -= self.expression[1]
            self.expression[1] = 0
        elif self.operator == "*":
            self.expression[0] *= self.expression[1]
            self.expression[1] = 0
        elif self.operator == "/":
            try:
                self.expression[0] /= self.expression[1]
                self.expression[1] = 0
            except ZeroDivisionError as err:
                self.error_check = err

    def square(self):
        try:
            self.expression[0] = float(self.entry.get())
        except ValueError as err:
            self.error_check = err
            self.entry.delete(0, END)
            self.entry.insert(0, str(self.error_check))
            self.error_check = ""
            return
        self.expression[1] = self.expression[0]
        self.expression[0] *= self.expression[1]
        self.expression[1] = 0.0
        self.entry.delete(0, END)
        self.entry.insert(0, str(self.expression[0]))

    def sqroot(self):
        try:
            self.expression[0] = float(self.entry.get())
        except ValueError as err:
            self.error_check = err
            self.entry.delete(0, END)
            self.entry.insert(0, str(self.error_check))
            self.error_check = ""
            return
        self.expression[1] = sqrt(self.expression[0])
        self.expression[0] = self.expression[1]
        self.expression[1] = 0.0
        self.entry.delete(0, END)
        self.entry.insert(0, str(self.expression[0]))

    def equal(self):
        if self.entry.get():
            try:
                self.expression[1] = float(self.entry.get())
            except ValueError as err:
                self.error_check = err
            self.evaluate()
            if self.error_check:
                self.entry.delete(0, END)
                self.entry.insert(0, str(self.error_check))
            else:
                if self.operator != "":
                    self.entry.delete(0, END)
                    self.entry.insert(0, str(self.expression[0]))


calc = Calculator(root)
root.mainloop()
