"""
The main GUI code.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from gui_tools.right_click.entry import EntryWithRightClick
from gui_tools.right_click.spinbox import SpinboxWithRightClick
from gui_tools.right_click.combobox import ComboboxWithRightClick
from gui_tools.right_click.listbox import ListboxWithRightClick
from gui_tools.idlelib_clone import tooltip
from gui_tools.scrollable_frame import VerticalScrolledFrame
from threading import Thread
from pathlib import Path
import traceback
import json
from pathlib import Path
from project_tools import drives, os_detect, project
from typing import Union, Any
import logging
from project_tools.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class GUI(tk.Tk):
    """
    The GUI for the CircuitPython Project Manager.
    """
    def __init__(self):
        super().__init__()
        self.title("CircuitPython Project Manager")
        self.resizable(False, False)
        self.config_path = Path.cwd() / "config.json"
        self.disable_closing = False
        self.protocol("WM_DELETE_WINDOW", self.try_to_close)

    def __enter__(self):
        return self

    def try_to_close(self) -> None:
        """
        Try to close the application - checks if we are not busy and displays dialogs appropriately.

        :return: None.
        """
        logger.debug("User requested closing window...")
        if self.disable_closing:
            logger.warning("Currently in the middle of doing something!")
            if mbox.askokcancel("CircuitPython Project Manager: Confirmation",
                                "Something is happening right now!\n"
                                "If you close out now, this will immediately stop what we are doing and may cause a "
                                "corrupt directory hierarchy, broken files and/or broken directories. "
                                "Are you sure you want to exit?",
                                icon="warning", default="cancel"):
                logger.debug("User continued to close window!")
                self.destroy()
        else:
            logger.debug("Destroying main window!")
            self.destroy()

    def save_key(self, key: str = None, value: Any = None) -> None:
        """
        Save a key to the config file.

        :param key: A string.
        :param value: Something.
        :return: None.
        """
        if not self.config_path.exists():
            self.config_path.write_text("{}")
        try:
            old_json = json.loads(self.config_path.read_text())
        except json.decoder.JSONDecodeError:
            old_json = {}
        logger.debug(f"Setting {repr(key)} to {repr(value)}!")
        old_json[key] = value
        self.config_path.write_text(json.dumps(old_json, sort_keys=True, indent=4))

    def load_key(self, key: str) -> Any:
        """
        Retrieves a key from the config file.

        :param key: A string.
        :return: Something, or None if it was not found.
        """
        if not self.config_path.exists():
            self.config_path.write_text("{}")
        try:
            value = json.loads(self.config_path.read_text())[key]
            return value
        except (json.decoder.JSONDecodeError, KeyError):
            logger.warning(f"Could not find {repr(key)} in config!")
            return None

    def validate_for_number(self, new: str = "") -> bool:
        """
        Checks a string to see whether it's a number and within 3 digits.

        :param new: The string to validate.
        :return: A bool telling whether it passed validation.
        """
        logger.debug(f"{repr(new)} did " + ("" if new.isdigit() and len(new) <= 3 else "not ") + "pass validation!")
        return new.isdigit() and len(new) <= 3

    def create_config(self) -> None:
        """
        Re-create the config keys if they do not exist.

        :return: None.
        """

    def create_file_menu(self) -> None:
        """
        Create the file menu.

        :return: None.
        """
        self.file_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.file_menu.add_command(label="New...")
        self.file_menu.add_command(label="Open...")
        self.file_menu.add_command(label="Close project", state=tk.DISABLED)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.try_to_close)

    def create_edit_menu(self) -> None:
        """
        Create the edit menu.

        :return: None.
        """
        self.edit_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.edit_menu, label="Edit")
        self.edit_menu.add_command(label="Open .cpypmconfig", state=tk.DISABLED)
        self.edit_menu.add_command(label="Open .cpypmconfig file location", state=tk.DISABLED)

    def create_sync_menu(self) -> None:
        """
        Create the sync menu.

        :return: None.
        """
        self.sync_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.sync_menu, label="Sync")
        self.sync_menu.add_command(label="Sync files", state=tk.DISABLED)

    def create_help_menu(self) -> None:
        """
        Create the help menu.

        :return: None.
        """
        self.help_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.help_menu, label="Help")
        self.help_menu.add_command(label="Open README.md", state=tk.DISABLED)
        self.help_menu.add_command(label="Open project on GitHub", state=tk.DISABLED)

    def update_menu_state(self) -> None:
        """
        Update the menu's disable and enabled items.

        :return: None.
        """
        self.file_menu.entryconfigure("New...",
                                      state=tk.NORMAL if self.cpypmconfig_path is None else tk.DISABLED)
        self.file_menu.entryconfigure("Open...",
                                      state=tk.NORMAL if self.cpypmconfig_path is None else tk.DISABLED)
        self.file_menu.entryconfigure("Close project",
                                      state=tk.DISABLED if self.cpypmconfig_path is None else tk.NORMAL)
        self.edit_menu.entryconfigure("Open .cpypmconfig",
                                      state=tk.DISABLED if self.cpypmconfig_path is None else tk.NORMAL)
        self.edit_menu.entryconfigure("Open .cpypmconfig file location",
                                      state=tk.DISABLED if self.cpypmconfig_path is None else tk.NORMAL)
        self.sync_menu.entryconfigure("Sync files",
                                      state=tk.DISABLED if self.cpypmconfig_path is None else tk.NORMAL)

    def create_menu(self) -> None:
        """
        Create the menu.

        :return: None.
        """
        self.option_add("*tearOff", tk.FALSE)
        self.menu_bar = tk.Menu(self)
        self["menu"] = self.menu_bar
        self.create_file_menu()
        self.create_edit_menu()
        self.create_sync_menu()
        self.create_help_menu()
        self.cpypmconfig_path = None
        self.update_menu_state()

    def create_gui(self) -> None:
        """
        Create the GUI.

        :return: None.
        """
        logger.debug("Creating GUI...")
        if os_detect.on_linux():
            self.global_style = ttk.Style()
            self.global_style.theme_use("clam")
        self.create_config()
        self.create_menu()

    def run(self) -> None:
        """
        Run the GUI, this will block.

        :return: None.
        """
        self.create_gui()
        self.lift()
        self.mainloop()

    def __exit__(self, err_type=None, err_value=None, err_traceback=None):
        if err_type is not None:
            mbox.showerror("CircuitPython Project Manager: ERROR!",
                           "Oh no! A fatal error has occurred!\n"
                           f"Error type: {err_type}\n"
                           f"Error value: {err_value}\n"
                           f"Error traceback: {err_traceback}\n\n" + traceback.format_exc())
            logger.exception("Uh oh, a fatal error has occurred!", exc_info=True)

