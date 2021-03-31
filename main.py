"""
The main program.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

# TODO: Make public on GitHub
# TODO: Make binaries like in CPY Bundle Manager

import gui
from pathlib import Path
from sys import argv
from project_tools.create_logger import create_logger
import logging

LEVEL = logging.DEBUG

log_path = Path.cwd() / "log.log"
log_path.write_text("")

logger = create_logger(name=__name__, level=LEVEL)

logger.debug(f"Found {len(argv)} argument(s)")
logger.debug(f"({repr(argv)})")

path = None
if len(argv) > 1:
    logger.debug("Path to .cpypmconfig was passed in!")
    logger.debug(f"Path is {repr(argv[1])}")
    path = Path(argv[1])
    if path.is_dir():
        path = None

logger.debug(f"Starting application...")
logger.info(f"Log level is {repr(LEVEL)}")
with gui.GUI() as gui:
    gui.run(cpypmconfig_path=path)
logger.warning(f"Application stopped!")
