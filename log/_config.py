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


# fmt: off
LOG_FILE_PATH =  r"/log.log"
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
# fmt: on

if os.path.exists(LOG_FILE_PATH):
    os.remove(LOG_FILE_PATH)


logger.remove()
# 控制台处理器
logger.add(
    sys.stdout,  # 输出到控制台
    level="TRACE",  # 最低日志级别
    format=DEFAULT_FORMAT,
)

# # 文件处理器
# logger.add(
#     LOG_FILE_PATH,  # 输出到文件
#     level="DEBUG",  # 最低日志级别
#     format=DEFAULT_FORMAT,
# )


debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
success = logger.success
exception = logger.exception
catch = logger.catch
trace = logger.trace
