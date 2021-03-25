"""
This module handles making a new CircuitPython project.

-----------

Classes list:

No classes!

-----------

Functions list:

- replace_sus_chars(file_name: str) -> str
- make_new_project(parent_directory: Path, project_name: str = "Untitled", autogen_gitignore: bool = True,
                   fl_cpy_hierarchy: Path = (Path.cwd() / "default_circuitpython_hierarchy")) -> None

"""

from pathlib import Path
import shutil
import re
from project_tools.create_logger import create_logger
import logging

logger = create_logger(name=__name__, level=logging.DEBUG)


def replace_sus_chars(file_name: str) -> str:
    """
    Replace suspicious characters in file name - found at https://stackoverflow.com/a/13593932/10291933

    :param file_name: A str - the file name to check.
    :return: A str - the file name cleaned.
    """
    return re.sub("[^\w\-_. ]", "_", file_name)


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
    project_path = parent_directory / dfl_cpy_hierarchy.name
    logger.debug(f"Copying from {repr(dfl_cpy_hierarchy)} to {repr(project_path)}")
    shutil.copytree(dfl_cpy_hierarchy, project_path)
    new_path = parent_directory / replace_sus_chars(project_name)
    logger.debug(f"Renaming {repr(project_path)} to {repr(new_path)}")
    project_path.rename(new_path)
