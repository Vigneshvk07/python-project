import math
import random
import tkinter as tk
from tkinter import ttk
import numpy as np

class Calculator:
    def __init__(self):
        self.result = ""

    def evaluate(self, expression):
        try:
            allowed_names = {'math': math, 'np': np, 'random': random}
            self.result = str(eval(expression, {"__builtins__": None}, allowed_names))
        except Exception as e:
            self.result = "Error"
        return self.result

    def clear(self):
        self.result = ""
        return self.result

    def get_result(self):
        return self.result

def animate_button(button):
    original_color = button.cget("background")
    button.config(background="lightblue")
    button.after(100, lambda: button.config(background=original_color))

class CalculatorApp:
    def __init__(self, root):
        self.calc = Calculator()
        self.expression = ""
        self.root = root
        self.inverse = False
        root.title("Scientific Calculator")
        root.geometry("700x800")

        self.display = ttk.Entry(root, font=('Arial', 24), justify='right')
        self.display.grid(row=0, column=0, columnspan=6, ipady=10, sticky='nsew')

        self.buttons = [
            'C', '(', ')', 'sin', 'cos', 'tan',
            '7', '8', '9', 'inv', 'π', 'sqrt',
            '4', '5', '6', '*', 'e^x', 'log',
            '1', '2', '3', '/', '10^x', 'ln',
            '0', '.', '=', '+', '-', 'fact',
            'rnd', 'rad', 'exp', 'Mat'
        ]

        self.button_objs = {}
        row = 1
        col = 0
        for button in self.buttons:
            action = lambda x=button: self.click(x)
            btn = ttk.Button(root, text=button, command=action)
            btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
            self.button_objs[button] = btn
            col += 1
            if col > 5:
                col = 0
                row += 1

        for i in range(6):
            root.grid_columnconfigure(i, weight=1)
        for i in range(8):  
            root.grid_rowconfigure(i, weight=1)

    def click(self, key):
        if key == "=":
            self.expression = self.calc.evaluate(self.expression)
        elif key == "C":
            self.expression = self.calc.clear()
        elif key == "inv":
            self.toggle_inverse()
        elif key in ("sin", "cos", "tan", "asin", "acos", "atan"):
            if self.inverse:
                self.expression += f"math.a{key}("
            else:
                self.expression += f"math.{key}("
        elif key == "sqrt":
            self.expression += "math.sqrt("
        elif key == "log":
            self.expression += "math.log10("
        elif key == "ln":
            self.expression += "math.log("
        elif key == "π":
            self.expression += "math.pi"
        elif key == "rnd":
            self.expression += "random.random()"
        elif key == "rad":
            self.expression += "math.radians("
        elif key == "fact":
            self.expression += "math.factorial("
        elif key == "exp":
            self.expression += "math.exp("
        elif key == "e^x":
            self.expression += "math.exp("
        elif key == "10^x":
            self.expression += "10**"
        elif key == "Mat":
            self.show_mat_options()
        else:
            self.expression += key

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

        button = self.root.focus_get()
        if button:
            animate_button(button)

    def toggle_inverse(self):
        self.inverse = not self.inverse
        if self.inverse:
            self.button_objs['sin'].config(text='asin')
            self.button_objs['cos'].config(text='acos')
            self.button_objs['tan'].config(text='atan')
        else:
            self.button_objs['sin'].config(text='sin')
            self.button_objs['cos'].config(text='cos')
            self.button_objs['tan'].config(text='tan')

    def show_mat_options(self):
        mat_options = [
            "Matrix Addition",
            "Matrix Subtraction",
            "Matrix Multiplication",
            "Matrix Power",
            "Matrix Dot Product",
            "Matrix Determinant",
            "Matrix Transpose",
            "Matrix Inverse"
        ]

        def add_mat_option(option):
            self.expression += option.lower().replace(" ", "_") + "("
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
            mat_window.destroy()

        mat_window = tk.Toplevel(self.root)
        mat_window.title("Matrix Options")

        for option in mat_options:
            btn = ttk.Button(mat_window, text=option, command=lambda o=option: add_mat_option(o))
            btn.pack(fill=tk.BOTH, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
