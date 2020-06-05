#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3


class View:

    def __init__(self, root, model):
        self.frame = Tk.Frame(root, bg="#141414", padx="50", pady="100")
        self.model = model
        self.success = False

        Tk.Label(self.frame, text="Solver for second degree polynomial", bg="#141414", fg="white",
                 font="Verdana 32 bold italic").pack()

        self.frame2 = Tk.Frame(self.frame, bg="#141414")
        self.left = Tk.StringVar()
        self.right = Tk.StringVar()
        Tk.Entry(self.frame2, width="40", relief="groove", highlightbackground="#141414", bg="#141414",
                 fg="#bebebe", textvariable=self.left, justify="center").grid(row=0, column=0)
        Tk.Label(self.frame2, text="=", fg="#bebebe", bg="#141414", bd=0, pady="50").grid(row=0, column=1)
        Tk.Entry(self.frame2, width="40", relief="groove", highlightbackground="#141414", bg="#141414",
                 fg="#bebebe", textvariable=self.right, justify="center").grid(row=0, column=2)
        self.frame2.pack()

        Tk.Button(self.frame, bg="#bebebe", text="Solve", command=self.resolve).pack()
        self.left.set('0')
        self.right.set('0')
        
        self.result_frame = Tk.Frame(self.frame, bg="#141414", pady="75")

        self.frame.pack(fill=Tk.BOTH, expand=1)

    def resolve(self):
        res = self.model.resolve(self.left.get(), self.right.get())
        self.reset_frame()
        if not res[0]:
            Tk.Label(self.result_frame, text=res[1], fg="red", bg="#141414", bd=0, pady="25").grid(row=4, columnspan=4)
        else:
            self.print_result([res[1], res[2], res[3]])
        self.result_frame.pack()

    def reset_frame(self):
        for widget1 in self.result_frame.winfo_children():
            widget1.grid_forget()

    def print_reduce(self, array1, array2, row):
        Tk.Label(self.result_frame, text=array1, bg="#141414", fg="#bebebe").grid(row=row, column=1)
        Tk.Label(self.result_frame, text=" ---> ", bg="#141414", fg="#bebebe").grid(row=row, column=2)
        Tk.Label(self.result_frame, text=array2, bg="#141414", fg="green").grid(row=row, column=3)
    
    def print_result(self, params):
        Tk.Label(self.result_frame, text="Reduced form: ", bg="#141414", fg="white").grid(row=1, column=0)
        self.print_reduce(" a*X^2 + b*X + c = 0 ", params[2], 1)
        Tk.Label(self.result_frame, text="Polynomial degree: ", bg="#141414", fg="white").grid(row=2, column=0)
        Tk.Label(self.result_frame, text=params[1], bg="#141414", fg="green").grid(row=2, column=3)
        if params[1] <= 2:
            a, b, c = float(params[0][2]), float(params[0][1]), float(params[0][0])
            if params[1] == 0 and c == 0:
                Tk.Label(self.result_frame, text="All real number are solution", bg="#141414", fg="green")\
                    .grid(row=3, columnspan=4)
            elif params[1] == 0 and c != 0:
                Tk.Label(self.result_frame, text="There is no solution", bg="#141414", fg="red")\
                    .grid(row=3, columnspan=4)
            elif params[1] == 1:
                Tk.Label(self.result_frame, text="The solution is", bg="#141414", fg="white").grid(row=3, column=0)
                if c == 0:
                    Tk.Label(self.result_frame, text="0", bg="#141414", fg="green").grid(row=4, column=3)
                else:
                    self.print_reduce(" -c/b ", self.model.to_fract(-1 * c / b), 4)
            else:
                delta = (b ** 2) - (4 * a * c)
                Tk.Label(self.result_frame, text="Discriminant Δ: ", bg="#141414", fg="white").grid(row=3, column=0)
                self.print_reduce(" b^2 - 4ac ", self.model.clean_float(delta), 3)
                if delta > 0:
                    first_solution, second_solution = (-b + (delta ** (.5))) / (2 * a), (-b - (delta ** .5)) / (2 * a)
                    Tk.Label(self.result_frame, text="The two solutions are: ", bg="#141414", fg="white")\
                        .grid(row=4, column=0)
                    self.print_reduce(" x1 = (-b + √Δ)/2a ", self.model.to_fract(round(first_solution, 6)), 5)
                    self.print_reduce(" x1 = (-b - √Δ)/2a ", self.model.to_fract(round(second_solution, 6)), 6)
                elif delta == 0:
                    Tk.Label(self.result_frame, text="The solution is: ", bg="#141414", fg="white")\
                        .grid(row=4, column=0)
                    self.print_reduce(" x1 = -b/a ", self.model.to_fract(-1 * b / a), 5)
                else:
                    Tk.Label(self.result_frame, text="The two solutions are: ", bg="#141414", fg="white")\
                        .grid(row=4, column=0)
                    delta = -delta if delta < 0 else delta
                    self.print_reduce(" x1 = (-b + i√Δ)/2a ", '(-' + self.model.clean_float(b) + '+ i√' +
                                      self.model.clean_float(delta) + ')/' + self.model.clean_float(2 * a), 5)
                    self.print_reduce(" x1 = (-b - i√Δ)/2a ", '(-' + self.model.clean_float(b) + '- i√' +
                                      self.model.clean_float(delta) + ')/' + self.model.clean_float(2 * a), 6)
        else:
            Tk.Label(self.result_frame, text="The polynomial degree is stricly greater than 2, I can\'t solve.",
                     bg="#141414", fg="red").grid(row=4, columnspan=4)
        self.result_frame.pack()
