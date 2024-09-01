import logging

import sys

from . import config

CONSOLE_MSG_FORMAT = "COMET: %(message)s"

FILE_MSG_FORMAT = "%(asctime)s COMET %(levelname)s: %(message)s"


def setup() -> None:
    comet_root_logger = logging.getLogger("opik")
    config_ = config.CometConfig()

    console_handler = logging.StreamHandler(sys.stdout)
    console_level = config_.console_logging_level
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter(CONSOLE_MSG_FORMAT))

    comet_root_logger.addHandler(console_handler)

    root_level = console_handler.level

    if config_.file_logging_level is not None:
        file_handler = logging.FileHandler(config_.logging_file)
        file_level = config_.file_logging_level
        file_handler.setLevel(file_level)
        file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        comet_root_logger.addHandler(file_handler)

        root_level = min(root_level, file_handler.level)

    comet_root_logger.setLevel(level=root_level)
