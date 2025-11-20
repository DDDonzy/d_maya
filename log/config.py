from loguru import logger

import sys
import os
from enum import Enum
from functools import partial

# Public API
__all__ = [
    "logger",
    "debug",
    "info",
    "warning",
    "error",
    "exception",
    "catch",
    "success",
    "trace",
]


CONSOLE = True
LOG_FILE_PATH = None  # r"t:/d_maya/log.log"


# format
# fmt: off
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
# fmt: on
def formatter(record):
    """Custom formatter to handle multi-line messages."""
    record["message"] = record["message"].strip("\n") + "\n"
    return DEFAULT_FORMAT


logger.level("TRACE", color="<cyan><dim><bold>")
try:
    logger.level("NOTICE", no=22, color="<cyan><bold>")
except Exception:
    pass
logger.notice = partial(logger.log, "NOTICE")

# filter
_log_filter = {"level": "TRACE"}


def level_filter(record):
    filter_level = _log_filter["level"]
    current_level_no = logger.level(filter_level).no
    return record["level"].no >= current_level_no


# set level
def set_level(level: int):
    if isinstance(level, int):
        level = LogLevel(level).name
    else:
        logger.error("Invalid level type. Must be str or int.")
        return
    _log_filter["level"] = level
    logger.success(f"Log level set to '{level}'")


# Clear existing handlers
logger.remove()
#

# Console
LOG_CONSOLE_ID = None
if CONSOLE:
    CONSOLE_ID = logger.add(
        sys.stdout,  # 输出到控制台
        level="TRACE",  # 最低日志级别
        filter=level_filter,
        format=formatter,
    )


# File
LOG_FILE_ID = None
if LOG_FILE_PATH:
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
    LOG_FILE_ID = logger.add(
        LOG_FILE_PATH,  # 输出到文件
        level="TRACE",  # 最低日志级别
        filter=level_filter,
        format=formatter,
    )


# Modify handler levels
class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


# set_level(1)

trace = logger.trace
debug = logger.debug
info = logger.info
notice = logger.notice
success = logger.success
warning = logger.warning
error = logger.error
exception = logger.exception
catch = logger.catch


if __name__ == "__main__":
    info("Test")
