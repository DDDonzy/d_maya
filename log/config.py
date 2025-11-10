from loguru import logger

import sys
import os

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


logger.remove()

# Console
if CONSOLE:
    logger.add(
        sys.stdout,  # 输出到控制台
        level="TRACE",  # 最低日志级别
        format=DEFAULT_FORMAT,
    )


# file
if LOG_FILE_PATH:
    if os.path.exists(LOG_FILE_PATH):
        os.remove(LOG_FILE_PATH)
    logger.add(
        LOG_FILE_PATH,  # 输出到文件
        level="TRACE",  # 最低日志级别
        format=DEFAULT_FORMAT,
    )


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
    import time

    s = time.time()
    for x in range(1000):
        trace(f"This is a trace message. {x}")
    print(f"Done in {time.time() - s}")
