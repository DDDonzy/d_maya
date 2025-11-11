from loguru import logger

import sys
import os
from enum import Enum

# Public API
__all__ = [
    "logger",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "exception",
    "catch",
    "success",
    "trace",
]


CONSOLE = True
LOG_FILE_PATH = None  # r"t:/d_maya/log.log"

# fmt: off
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
# fmt: on


# filter
log_filter = {"level": "INFO"}


def level_filter(record):
    filter_level = log_filter["level"]
    current_level_no = logger.level(filter_level).no
    return record["level"].no >= current_level_no


# Clear existing handlers
logger.remove()

# Console
LOG_CONSOLE_ID = None
if CONSOLE:
    CONSOLE_ID = logger.add(
        sys.stdout,  # 输出到控制台
        level="TRACE",  # 最低日志级别
        filter=level_filter,
        format=DEFAULT_FORMAT,
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
        format=DEFAULT_FORMAT,
    )


# Modify handler levels
class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


def set_level(level: int):
    if isinstance(level, int):
        level = LogLevel(level).name
    else:
        logger.error("Invalid level type. Must be str or int.")
        return
    log_filter["level"] = level
    logger.success(f"Log level set to '{level}'")


debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
success = logger.success
exception = logger.exception
catch = logger.catch
trace = logger.trace

if __name__ == "__main__":
    info("Test")
