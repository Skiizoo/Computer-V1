#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

from model import Model
from view import View

class Controller:

    def __init__(self):
        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self.model)

    def run(self):
        self.root.title("ComputerV1 @tbroggi")
        self.root.deiconify()
        self.root.mainloop()
