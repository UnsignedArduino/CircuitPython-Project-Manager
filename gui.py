"""
The main GUI code.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

# TODO: Add tooltips

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import filedialog as fd
from gui_tools.right_click.entry import EntryWithRightClick
from gui_tools.right_click.spinbox import SpinboxWithRightClick
from gui_tools.right_click.combobox import ComboboxWithRightClick
from gui_tools.right_click.listbox import ListboxWithRightClick
from gui_tools.right_click.text import TextWithRightClick
from gui_tools.idlelib_clone import tooltip
from gui_tools.scrollable_frame import VerticalScrolledFrame
from gui_tools.clickable_label import ClickableLabel
from threading import Thread
from pathlib import Path
import traceback
import json
from webbrowser import open as open_application
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

    def show_traceback(self) -> bool:
        """
        Whether to show the traceback or not depending on the config file.

        :return: None.
        """
        try:
            return bool(self.load_key("show_traceback_in_error_messages"))
        except AttributeError:
            return False

    def create_config(self) -> None:
        """
        Re-create the config keys if they do not exist.

        :return: None.
        """
        if not self.load_key("show_traceback_in_error_messages"):
            self.save_key("show_traceback_in_error_messages", False)
        if not self.load_key("unix_drive_mount_point"):
            self.save_key("unix_drive_mount_point", "/media")

    def open_project(self) -> None:
        """
        Open a project.

        :return: None.
        """
        logger.debug("Opening project...")
        path = fd.askopenfilename(initialdir=str(Path.cwd()),
                                  title="CircuitPython Project Manager: Select a .cpypmconfig file",
                                  filetypes=((".cpypmconfig files", "*.cpypmconfig"), ("All files", "*.*")))
        if path:
            path = Path(path)
            logger.debug(f"Returned valid path! Path is {repr(path)}")
            self.cpypmconfig_path = path
            self.update_main_gui()
        else:
            logger.debug("User canceled opening project!")

    def close_project(self) -> None:
        """
        Close a project.

        :return: None.
        """
        logger.debug("Closing project...")
        self.cpypmconfig_path = None
        self.update_main_gui()

    def dismiss_dialog(self, dlg: tk.Toplevel) -> None:
        """
        Intercept a dialog's close button to make sure we release the window grab.

        :param dlg: The dialog to destroy.
        :return: None.
        """
        if self.disable_closing:
            logger.warning("Currently in the middle of doing something!")
            if mbox.askokcancel("CircuitPython Project Manager: Confirmation",
                                "Something is happening right now!\n"
                                "If you close out now, this will immediately stop what we are doing and may cause a "
                                "corrupt directory hierarchy, broken files and/or broken directories. "
                                "Are you sure you want to exit?",
                                icon="warning", default="cancel"):
                logger.debug("User continued to close window!")
                logger.debug("Destroying dialog")
                try:
                    dlg.grab_release()
                    dlg.destroy()
                except tk.TclError:
                    pass
        else:
            logger.debug("Destroying dialog")
            dlg.grab_release()
            dlg.destroy()

    def create_dialog(self, title: str) -> tk.Toplevel:
        """
        Create a dialog and return it.

        :param title: The title of the dialog.
        :return:
        """
        dlg = tk.Toplevel(master=self)
        dlg.protocol("WM_DELETE_WINDOW", lambda: self.dismiss_dialog(dlg))
        dlg.transient(self)
        dlg.resizable(False, False)
        dlg.title(title)
        dlg.wait_visibility()
        dlg.grab_set()
        return dlg

    def open_new_project_directory(self) -> None:
        """
        Open a directory and return None or a pathlib.Path.

        :return: None.
        """
        logger.debug("Opening directory...")
        path = fd.askdirectory(initialdir=str(Path.cwd()),
                               title="CircuitPython Project Manager: Select a directory")
        if path:
            path = Path(path)
            logger.debug(f"Returned valid path! Path is {repr(path)}")
            self.project_location_var.set(str(path))
        else:
            logger.debug("User canceled opening project!")

    def create_new_project_location(self) -> None:
        """
        Create the new project location widgets.

        :return: None.
        """
        self.project_location_frame = ttk.Frame(master=self.new_project_frame)
        self.project_location_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.project_location_label = ttk.Label(master=self.project_location_frame, text="Project location: ")
        self.project_location_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.project_location_var = tk.StringVar()
        self.project_location_entry = EntryWithRightClick(master=self.project_location_frame,
                                                          textvariable=self.project_location_var, width=51)
        self.project_location_entry.initiate_right_click_menu()
        self.project_location_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)
        self.project_location_button = ttk.Button(master=self.project_location_frame, text="Browse...",
                                                  command=self.open_new_project_directory)
        self.project_location_button.grid(row=0, column=2, padx=1, pady=0, sticky=tk.NW)

    def create_new_project_details(self) -> None:
        """
        Create the new project detail widgets, like title and description.

        :return: None.
        """
        self.project_details_frame = ttk.Frame(master=self.new_project_frame)
        self.project_details_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)
        self.project_title_label = ttk.Label(master=self.project_details_frame, text="Project title: ")
        self.project_title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.project_title_var = tk.StringVar(value="Untitled")
        self.project_title_entry = EntryWithRightClick(master=self.project_details_frame, width=40, textvariable=self.project_title_var)
        self.project_title_entry.initiate_right_click_menu()
        self.project_title_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)
        self.project_autogen_var = tk.BooleanVar(value=True)
        self.project_autogen_checkbox = ttk.Checkbutton(master=self.project_details_frame, text="Auto-generate a .gitignore",
                                                        variable=self.project_autogen_var)
        self.project_autogen_checkbox.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NW)
        self.project_description_label = ttk.Label(master=self.project_details_frame, text="Project description: ")
        self.project_description_label.grid(row=1, column=0, columnspan=3, padx=1, pady=1, sticky=tk.NW)
        self.project_description_text = TextWithRightClick(master=self.project_details_frame, width=60, height=10)
        self.project_description_text.initiate_right_click_menu()
        self.project_description_text.grid(row=2, column=0, columnspan=3, padx=1, pady=1, sticky=tk.NW)
        self.project_status = ttk.Label(master=self.project_details_frame)
        self.project_status.stop = False
        self.project_status.grid(row=3, column=0, columnspan=3, padx=1, pady=1, sticky=tk.NW)

    def update_new_project_buttons(self) -> None:
        """
        Update the new project buttons. Will reschedule itself automatically.

        :return: None.
        """
        if self.project_status.stop:
            return
        try:
            if not self.project_title_var.get():
                enable = False
                self.project_status.config(text="No title found!")
            elif not self.project_location_var.get() or not Path(self.project_location_var.get()).exists():
                enable = False
                self.project_status.config(text="The parent directory of the project does not exist!")
            elif (Path(self.project_location_var.get()) / project.replace_sus_chars(self.project_title_var.get())).exists():
                enable = False
                self.project_status.config(text="A project under the same name already exists in that parent directory!")
            else:
                enable = True
                self.project_status.config(text="All good!")
            self.make_new_project_button.config(state=tk.NORMAL if enable else tk.DISABLED)
        except tk.TclError:
            pass
        else:
            self.after(ms=100, func=self.update_new_project_buttons)

    def create_new_project_buttons(self) -> None:
        """
        Create the new project buttons, like Ok and Cancel.

        :return: None.
        """
        self.project_buttons_frame = ttk.Frame(master=self.new_project_frame)
        self.project_buttons_frame.grid(row=2, column=0, padx=1, pady=1, sticky=tk.N)
        self.make_new_project_button = ttk.Button(master=self.project_buttons_frame, text="Make new project",
                                                  command=self.start_create_new_project_thread)
        self.make_new_project_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.N)
        self.cancel_new_project_button = ttk.Button(master=self.project_buttons_frame, text="Cancel",
                                                    command=lambda: self.dismiss_dialog(self.new_project_window))
        self.cancel_new_project_button.grid(row=0, column=1, padx=1, pady=1, sticky=tk.N)
        self.update_new_project_buttons()

    def set_childrens_state(self, frame, enabled: bool = True) -> None:
        """
        Set the state of a frame's children.

        :param frame: A Tkinter widget to iterate over's it's children.
        :param enabled: Weather to enable/disable the children.
        :return: None.
        """
        logger.debug(f"{'Enabling' if enabled else 'Disabling'} {repr(frame)}")
        for child in frame.winfo_children():
            try:
                child.configure(state=tk.NORMAL if enabled else tk.DISABLED)
            except tk.TclError:
                try:
                    self.set_childrens_state(frame=child, enabled=enabled)
                except tk.TclError:
                    pass

    def start_create_new_project_thread(self) -> None:
        """
        Start the create new project thread.

        :return: None.
        """
        thread = Thread(target=self.create_new_project, args=(), daemon=True)
        logger.debug(f"Starting create new project thread {repr(thread)}")
        thread.start()

    def create_new_project(self) -> None:
        """
        Create a new project - this will block.

        :return: None.
        """
        self.project_status.stop = True
        self.project_status.config(text="Creating project...")
        self.disable_closing = True
        self.set_childrens_state(self.new_project_frame, False)
        try:
            self.cpypmconfig_path = project.make_new_project(parent_directory=Path(self.project_location_var.get()),
                                                             project_name=self.project_title_var.get(),
                                                             project_description=self.project_description_text.get("1.0", tk.END),
                                                             autogen_gitignore=self.project_autogen_var.get())
        except FileExistsError:
            mbox.showerror("CircuitPython Project Manager: Error!",
                           "A project already exists under the same name!\n"
                           "Please try creating a project with a different name or try creating it somewhere else!"
                           "\n\n" + (traceback.format_exc() if self.show_traceback() else ""))
            self.disable_closing = False
            return
        self.update_main_gui()
        self.disable_closing = False
        self.dismiss_dialog(self.new_project_window)

    def open_create_new_project(self) -> None:
        """
        Create a new project. This will open a new window.

        :return: None.
        """
        logger.debug("Creating new project...")
        self.new_project_window = self.create_dialog(title="CircuitPython Project Manager: Make a new project...")
        self.new_project_frame = ttk.Frame(master=self.new_project_window)
        self.new_project_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.create_new_project_location()
        self.create_new_project_details()
        self.create_new_project_buttons()
        self.new_project_frame.wait_window()

    def create_file_menu(self) -> None:
        """
        Create the file menu.

        :return: None.
        """
        self.file_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.file_menu.add_command(label="New...", command=self.open_create_new_project)
        self.file_menu.add_command(label="Open...", command=self.open_project)
        self.file_menu.add_command(label="Close project", command=self.close_project)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.try_to_close)

    def create_edit_menu(self) -> None:
        """
        Create the edit menu.

        :return: None.
        """
        self.edit_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.edit_menu, label="Edit")
        self.edit_menu.add_command(label="Open .cpypmconfig",
                                   command=lambda: open_application(self.cpypmconfig_path))
        self.edit_menu.add_command(label="Open .cpypmconfig file location",
                                   command=lambda: open_application(self.cpypmconfig_path.parent))

    def sync_files(self) -> None:
        """
        Sync the files - this will block.

        :return: None.
        """
        self.disable_closing = True
        self.sync_menu.entryconfigure("Sync files", state=tk.DISABLED)
        project.sync_project(cpypm_config_path=self.cpypmconfig_path)
        self.sync_menu.entryconfigure("Sync files", state=tk.NORMAL)
        self.disable_closing = False

    def start_sync_files_thread(self) -> None:
        """
        Start the sync files thread.

        :return: None.
        """
        thread = Thread(target=self.sync_files, args=(), daemon=True)
        logger.debug(f"Starting sync file thread {repr(thread)}")
        thread.start()

    def create_sync_menu(self) -> None:
        """
        Create the sync menu.

        :return: None.
        """
        self.sync_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.sync_menu, label="Sync")
        self.sync_menu.add_command(label="Sync files", command=self.start_sync_files_thread)

    def create_help_menu(self) -> None:
        """
        Create the help menu.

        :return: None.
        """
        self.help_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.help_menu, label="Help")
        self.help_menu.add_command(label="Open configuration", command=lambda: open_application(str(self.config_path)))
        self.help_menu.add_command(label="Open logs", command=lambda: open_application(str(Path.cwd() / "log.log")))
        self.help_menu.add_separator()
        # TODO: Implement opening the README.md
        self.help_menu.add_command(label="Open README.md", state=tk.DISABLED)
        # TODO: Implement opening the project on GitHub
        self.help_menu.add_command(label="Open project on GitHub", state=tk.DISABLED)

    def update_menu_state(self) -> None:
        """
        Update the menu's disable and enabled items.

        :return: None.
        """
        logger.debug(f"Updating menu state...")
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
        try:
            if self.cpypmconfig_path is None or json.loads(self.cpypmconfig_path.read_text())["sync_location"] is None:
                self.sync_menu.entryconfigure("Sync files", state=tk.DISABLED)
            else:
                self.sync_menu.entryconfigure("Sync files", state=tk.NORMAL)
        except FileNotFoundError:
            logger.exception("Uh oh, an exception has occurred!")
            self.close_project()
            mbox.showerror("CircuitPython Project Manager: Error!",
                           "Your project's .cpypmconfig file cannot be accessed, closing project!")

    def create_menu(self) -> None:
        """
        Create the menu.

        :return: None.
        """
        self.option_add("*tearOff", tk.FALSE)
        self.menu_bar = tk.Menu(self, postcommand=self.update_menu_state)
        self["menu"] = self.menu_bar
        self.create_file_menu()
        self.create_edit_menu()
        self.create_sync_menu()
        self.create_help_menu()
        self.cpypmconfig_path = None
        self.update_menu_state()

    def destroy_all_children(self, widget):
        """
        Destroy all the children of the widget.

        :param widget: The parent of the children you want to destroy.
        :return: None.
        """
        logger.debug(f"Destroying all children of {repr(widget)}")
        for child in widget.winfo_children():
            try:
                child.destroy()
            except tk.TclError:
                pass

    def make_title(self, title: str) -> None:
        """
        Make the title's label and entry box.

        :title: The title of the project.
        :return: None.
        """
        self.title_frame = ttk.Frame(master=self.main_frame)
        self.title_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.title_label = ttk.Label(master=self.title_frame, text="Project title: ")
        self.title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.title_var = tk.StringVar(value=title)
        self.title_entry = EntryWithRightClick(master=self.title_frame, width=32, textvariable=self.title_var)
        self.title_entry.initiate_right_click_menu()
        self.title_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)

    def make_description(self, description: str) -> None:
        """
        Make the description's labels and text box.

        :param description: The description of the project.
        :return: None.
        """
        self.description_frame = ttk.Frame(master=self.main_frame)
        self.description_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)
        self.description_label = ttk.Label(master=self.description_frame, text="Project description: ")
        self.description_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.description_text = TextWithRightClick(master=self.description_frame, width=33, height=7)
        self.description_text.initiate_right_click_menu()
        self.description_text.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)
        self.description_text.insert("1.0", description)

    def update_drives(self) -> None:
        """
        Update all the drives connected.

        :return: None.
        """
        try:
            connected_drives = drives.list_connected_drives(not self.drive_selector_show_all_var.get(),
                                                            Path(self.load_key("unix_drive_mount_point")))
        except OSError:
            logger.error(f"Could not get connected drives!\n\n{traceback.format_exc()}")
            mbox.showerror("CircuitPython Project Manager: ERROR!",
                           "Oh no! An error occurred while getting a list of connected drives!\n\n" + (traceback.format_exc() if self.show_traceback() else ""))
            return
        logger.debug(f"Connected drives: {repr(connected_drives)}")
        self.drive_selector_combobox["values"] = connected_drives

    def make_drive_selector(self, drive: Path) -> None:
        """
        Make the drive selector.

        :drive: A pathlib.Path to the drive.
        :return: None.
        """
        self.drive_selector_frame = ttk.Frame(master=self.main_frame)
        self.drive_selector_frame.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW)
        self.drive_selector_label = ttk.Label(master=self.drive_selector_frame, text="Drive: ")
        self.drive_selector_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.drive_selector_var = tk.StringVar()
        if drive is not None:
            self.drive_selector_var.set(str(drive))
        self.drive_selector_combobox = ComboboxWithRightClick(master=self.drive_selector_frame, width=13, textvariable=self.drive_selector_var)
        self.drive_selector_combobox.initiate_right_click_menu()
        self.drive_selector_combobox.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW)
        self.drive_selector_refresh_btn = ttk.Button(master=self.drive_selector_frame, text="↻", width=2, command=self.update_drives)
        self.drive_selector_refresh_btn.grid(row=0, column=2, padx=1, pady=0, sticky=tk.NW)
        self.drive_selector_show_all_var = tk.BooleanVar(value=False)
        self.drive_selector_show_all_checkbtn = ttk.Checkbutton(master=self.drive_selector_frame, text="Show all drives?",
                                                                variable=self.drive_selector_show_all_var, command=self.update_drives)
        self.drive_selector_show_all_checkbtn.grid(row=0, column=3, padx=1, pady=1, sticky=tk.NW)
        self.update_drives()

    def update_main_gui(self) -> None:
        """
        Update the main GUI.

        :return: None.
        """
        self.update_menu_state()
        logger.debug("Updating main GUI...")
        self.destroy_all_children(widget=self.main_frame)
        if self.cpypmconfig_path is None:
            ttk.Label(
                master=self.main_frame,
                text="No project is open! Use the file menu to create\na new project or open an existing project!"
            ).grid(row=0, column=0, sticky=tk.NW)
        else:
            logger.debug(f"Parsing {repr(self.cpypmconfig_path)}")
            self.cpypmconfig = json.loads(self.cpypmconfig_path.read_text())
            # TODO: Show:
            #  - [✔] Title
            #  - [✔] Description
            #  - [✔] A combo box to select a drive to sync to
            #  - [ ] A listbox of all file/directories to sync.
            #  - [ ] A button to add file when nothing selected in listbox and open dialog to select file
            #  - [ ] A button to add directory when nothing selected in listbox and open dialog to select directory
            #  - [ ] A button to remove when something is selected in listbox and confirm too
            #  - [ ] Button to save all changes to .cpypmconfig which pops up un-closable dialog saying saving..
            #  - [ ] Button to sync files which pops up un-closable dialog with status bar and label saying syncing...
            self.make_title(self.cpypmconfig["project_name"])
            self.make_description(self.cpypmconfig["description"])
            self.make_drive_selector(self.cpypmconfig["sync_location"])

    def make_main_gui(self) -> None:
        """
        Make the main GUI stuffs.

        :return: None.
        """
        self.main_frame = ttk.Frame(master=self)
        self.main_frame.grid(row=0, column=0, sticky=tk.NW)
        self.update_main_gui()

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
        self.make_main_gui()

    def run(self) -> None:
        """
        Run the GUI, this will block.

        :return: None.
        """
        self.create_gui()
        self.lift()
        self.minsize(width=200, height=100)
        self.mainloop()

    def __exit__(self, err_type=None, err_value=None, err_traceback=None):
        if err_type is not None:
            mbox.showerror("CircuitPython Project Manager: ERROR!",
                           "Oh no! A fatal error has occurred!\n"
                           f"Error type: {err_type}\n"
                           f"Error value: {err_value}\n"
                           f"Error traceback: {err_traceback}\n\n" + traceback.format_exc())
            logger.exception("Uh oh, a fatal error has occurred!", exc_info=True)

