"""
The main program.

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

LEVEL = logging.DEBUG

log_path = Path.cwd() / "log.log"
log_path.write_text("")

logger = create_logger(name=__name__, level=LEVEL)
