"""
This module handles making a new CircuitPython project.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

from pathlib import Path
from project_tools.create_logger import create_logger
import logging

logger = create_logger(name=__name__, level=logging.DEBUG)


def make_new_project(parent_directory: Path, project_name: str = "Untitled", autogen_gitignore: bool = True,
                     dfl_cpy_hierarchy: Path = (Path.cwd() / "default_circuitpython_hierarchy")) -> None:
    """
    Make a new CircuitPython project.

    :param parent_directory: A pathlib.Path - where to put the project.
    :param project_name: A str - what to call the project - defaults to "Untitled"
    :param autogen_gitignore: A bool - whether to auto-generate a .gitignore for the project - defaults to True.
    :param dfl_cpy_hierarchy: A pathlib.Path - where we copy the base project files from - defaults to
     Path.cwd() / "default_circuitpython_hierarchy"
    :return: None.
    """
