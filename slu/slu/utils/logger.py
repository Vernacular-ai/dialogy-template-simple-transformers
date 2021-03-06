import logging
import os

import coloredlogs  # type: ignore

from slu import constants as const

project = "slu"


log = logging.getLogger(project)
fmt = "%(asctime)s:%(msecs)03d %(name)s [%(filename)s:%(lineno)s] %(levelname)s %(message)s"
level = (
    "ERROR"
    if os.environ.get(const.ENVIRONMENT, "").upper() == const.PRODUCTION.upper()
    else "DEBUG"
)
coloredlogs.install(level=level, logger=log, fmt=fmt)
