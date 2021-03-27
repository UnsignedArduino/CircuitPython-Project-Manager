"""
A module that extends the tk.Label class to make a clickable link.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

import tkinter as tk
from tkinter import ttk


class ClickableLabel(tk.Label):
    def __init__(self, master, callback, *args, **kwargs):
        super().__init__(master=master, fg="blue", cursor="hand2", *args, **kwargs)
        self.bind("<Button-1>", lambda e: callback)
