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
# TODO: Add README.md
# TODO: Make binaries like in CPY Bundle Manager

import gui
from pathlib import Path
from project_tools.create_logger import create_logger
import logging

LEVEL = logging.DEBUG

log_path = Path.cwd() / "log.log"
log_path.write_text("")

logger = create_logger(name=__name__, level=LEVEL)

logger.debug(f"Starting application...")
logger.info(f"Log level is {repr(LEVEL)}")
with gui.GUI() as gui:
    gui.run()
logger.warning(f"Application stopped!")
