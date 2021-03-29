"""
A listbox with a right click!

-----------

Classes list:

- ListboxWithRightClick(ttk.Combobox).__init__(self, master, *args, **kwargs):

-----------

Functions list:

No functions!

"""

import tkinter as tk
from tkinter import ttk
from typing import Callable
from project_tools.create_logger import create_logger
import logging

logger = create_logger(name=__name__, level=logging.DEBUG)


class ListboxWithRightClick(tk.Listbox):
    """
    A tk.Listbox, but with a right click!
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.bind("<Button-3>", self.popup)

    def popup(self, event):
        """
        Try to pop up the menu.

        :param event: An object that Tk calls with a bunch of info about the event.
        :return: None.
        """
        logger.debug(f"Right click! Attempting to pop up context menu...")
        try:
            self.callback()
        except TypeError:
            pass
        finally:
            if str(self["state"]) == "normal":
                try:
                    self.right_click_menu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self.right_click_menu.grab_release()
            else:
                logger.info(f"Not showing context menu, widget is currently disabled!")

    def initiate_right_click_menu(self, disable: list = [], callback: Callable = None):
        """
        Initiate the right click menu.

        :param disable: A list of what commands to disable. You can disable: Copy, Cut, Paste, Delete, and Select all.
        :param callback: A function that gets called before the right click menu is shown.
        :return: None.
        """
        self.right_click_menu = tk.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label="Copy", command=self.copy, state="disabled" if "Copy" in disable else "normal")
        self.right_click_menu.add_command(label="Cut", command=self.cut, state="disabled" if "Cut" in disable else "normal")
        self.right_click_menu.add_command(label="Paste", command=self.paste, state="disabled" if "Paste" in disable else "normal")
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Delete", command=self.delete_menu, state="disabled" if "Delete" in disable else "normal")
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label="Select all", command=self.select_all, state="disabled" if "Select all" in disable else "normal")
        self.callback = callback

    def select_all(self):
        """
        Select everything.

        :return: None.
        """
        logger.debug(f"Select all!")
        self.select_range(0, tk.END)

    def delete_menu(self):
        """
        Delete.

        :return: None.
        """
        if self.selection_present():
            logger.debug(f"Deleting from {repr(tk.SEL_FIRST)} to {repr(tk.SEL_LAST)}!")
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            logger.debug(f"Deleting everything!")
            self.delete(0, tk.END)

    def paste(self):
        """
        Paste.

        :return: None.
        """
        if self.selection_present():
            logger.debug(f"Deleting from {repr(tk.SEL_FIRST)} to {repr(tk.SEL_LAST)}!")
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)
        logger.debug(f"Inserting {repr(self.clipboard_get())} at {repr(self.index(tk.INSERT))}!")
        self.insert(self.index(tk.INSERT), self.clipboard_get())

    def cut(self):
        """
        Cut.

        :return: None.
        """
        if self.selection_present():
            logger.debug(f"Copying {repr(self.selection_get())} to clipboard!")
            self.copy_to_clipboard(self.selection_get())
            self.delete(tk.SEL_FIRST, tk.SEL_LAST)
            logger.debug(f"Deleting from {repr(tk.SEL_FIRST)} to {repr(tk.SEL_LAST)}!")
            self.select_clear()
        else:
            logger.debug(f"Copying everything to clipboard!")
            self.copy_to_clipboard(self.get())
            logger.debug(f"Deleting everything!")
            self.delete(0, tk.END)

    def copy(self):
        """
        Copy.

        :return: None.
        """
        if self.selection_present():
            logger.debug(f"Copying {repr(self.selection_get())} to clipboard!")
            self.copy_to_clipboard(self.selection_get())
            self.select_clear()
        else:
            logger.debug(f"Copying everything to clipboard!")
            self.copy_to_clipboard(self.get())

    def copy_to_clipboard(self, string: str = ""):
        """
        Copy something to the clipboard.

        :param string: What to copy to the clipboard.
        :return: None.
        """
        logger.debug(f"Copying {repr(string)} to clipboard!")
        self.clipboard_clear()
        self.clipboard_append(string)
        self.update()
