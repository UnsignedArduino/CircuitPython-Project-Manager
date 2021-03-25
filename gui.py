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
from gui_tools import download_dialog
from gui_tools.scrollable_frame import VerticalScrolledFrame
from threading import Thread
from pathlib import Path
import traceback
from pathlib import Path
from project_tools import drives, os_detect, project
from typing import Union, Any
import logging
from project_tools.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)
