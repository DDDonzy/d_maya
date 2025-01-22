
from loguru import logger as log

from maya.api.OpenMaya import MGlobal


def maya_log_handler(message):
    level = message.record["level"].name  # 获取日志级别
    if level == "ERROR":
        MGlobal.displayError(message)
    elif level == "WARNING":
        MGlobal.displayWarning(message)
    elif level == "INFO":
        MGlobal.displayInfo(f"Info: {message}")
    else:
        MGlobal.displayInfo(message)


def configure_logger():

    log.remove()
    log.add(maya_log_handler, format="{message}", level="INFO")


configure_logger()
