"""
This module handles CircuitPython projects.

-----------

Classes list:

No classes!

-----------

Functions list:

- replace_sus_chars(file_name: str) -> str
- make_new_project(parent_directory: Path, project_name: str = "Untitled", project_description: str = "",
                   autogen_gitignore: bool = True,
                   dfl_cpy_hierarchy: Path = (Path.cwd() / "default_circuitpython_hierarchy")) -> None
- sync_project(cpypm_config_path: Path) -> None

"""

from pathlib import Path
import shutil
import re
from json import loads as load_json_string, dumps as dump_json_string
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


def make_new_project(parent_directory: Path, project_name: str = "Untitled", project_description: str = "",
                     autogen_gitignore: bool = True,
                     dfl_cpy_hierarchy: Path = (Path.cwd() / "default_circuitpython_hierarchy")) -> None:
    """
    Make a new CircuitPython project.

    :param parent_directory: A pathlib.Path - where to put the project.
    :param project_name: A str - what to call the project - defaults to "Untitled"
    :param project_description: A str - a description of the project - defaults to ""
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
    cpypm_path = new_path / ".cpypmconfig"
    logger.debug(f"Path to .cpypmconfig is {repr(cpypm_path)}")
    cpypm_config = load_json_string(cpypm_path.read_text())
    cpypm_config["project_name"] = project_name
    cpypm_config["description"] = project_description
    cpypm_config["project_root"] = str(new_path)
    cpypm_path.write_text(dump_json_string(cpypm_config, indent=4))
    logger.debug(f"Filled .cpypmconfig")
    if autogen_gitignore:
        logger.debug("Auto-generating .gitignore")
        gitignore_path = new_path / ".gitignore"
        logger.debug(f"Path to .gitignore is {repr(gitignore_path)}")
        gitignore = ""
        gitignore += ".fseventsd/*\n"
        gitignore += ".metadata_never_index\n"
        gitignore += ".Trashes\n"
        gitignore += "boot_out.txt\n"
        gitignore_path.write_text(gitignore)
        logger.debug(f"Wrote .gitignore")
    logger.info(f"Made new project at {repr(new_path)}")


def sync_project(cpypm_config_path: Path) -> None:
    """
    Sync a project to the CircuitPython device.

    :param cpypm_config_path: A pathlib.Path - the path to the .cpypmconfig file.
    :raise ValueError: Raises ValueError if the sync location of the file hasn't been set.
    :return: None.
    """
    cpypm_config = load_json_string(cpypm_config_path.read_text())
    to_sync = [Path(p) for p in cpypm_config["files_to_sync"]]
    project_root_path = Path(cpypm_config["project_root"])
    sync_location_path = cpypm_config["sync_location"]
    if sync_location_path is None:
        raise ValueError("sync_location has not been filled out!")
    else:
        sync_location_path = Path(sync_location_path).absolute().resolve()
    logger.info(f"Found {len(to_sync)} items to sync!")
    logger.debug(f"Sync location is {repr(sync_location_path)}")
    logger.debug(f"Project root path is {repr(project_root_path)}")
    for path in to_sync:
        new_path = sync_location_path / path
        path = (project_root_path / path)
        logger.debug(f"Syncing {repr(path)} to {repr(new_path)}")
        if path.is_file():
            new_path.write_bytes(path.read_bytes())
        else:
            if new_path.exists():
                shutil.rmtree(new_path, ignore_errors=True)
            new_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(path, new_path)
