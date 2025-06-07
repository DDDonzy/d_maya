# z_bs/_tools/reloader.py
import sys
import importlib
from loguru import logger
import maya.cmds as cmds

# (maya_sink function and logger configuration section remain unchanged)


def maya_sink(message):
    record = message.record
    level_name = record["level"].name
    formatted_message = message.strip()
    if level_name == "ERROR" or level_name == "CRITICAL":
        cmds.error(formatted_message)
    elif level_name == "WARNING":
        cmds.warning(formatted_message)
    else:
        print(formatted_message)


logger.remove()
logger.add(
    maya_sink,
    level="INFO",
    format="{level: <8} | {name}:{function}:{line} - {message}",
    colorize=False
)
# (Above section requires no changes)


def reload_project(project_prefix: str):
    """
    Use loguru and custom maya_sink to find and reload modules, while skipping .qrc files.
    """
    if not isinstance(project_prefix, str) or not project_prefix:
        logger.error("A valid string must be provided for project_prefix.")
        return

    logger.info(f"--- Starting to reload all '{project_prefix}' related modules ---")

    # ----- Core changes are here -----
    # In the filtering conditions, add one more item: exclude modules ending with '.qrc'
    modules_to_reload = [
        name for name in sys.modules
        if name.startswith(project_prefix) and not name.endswith('.qrc')
    ]
    # --------------------------

    # (Optional) Explicitly tell users which files we skipped to improve user experience
    qrc_modules_skipped = [
        name for name in sys.modules
        if name.startswith(project_prefix) and name.endswith('.qrc')
    ]
    for name in qrc_modules_skipped:
        logger.info(f"Skipped reloading resource file: {name}")

    if not modules_to_reload:
        logger.warning(f"No reloadable modules found starting with '{project_prefix}'.")
        return

    # (The rest of the function code remains unchanged)
    modules_to_reload.sort(key=lambda name: name.count('.'), reverse=True)
    reloaded_count = 0
    failed_count = 0
    for module_name in modules_to_reload:
        try:
            module_obj = sys.modules[module_name]
            importlib.reload(module_obj)
            logger.success(f"Successfully reloaded: {module_name}")
            reloaded_count += 1
        except Exception:
            logger.exception(f"Failed to reload module: {module_name}")
            failed_count += 1
    logger.info("--- Reload completed ---")
    logger.info(f"Summary: {reloaded_count} successful, {failed_count} failed.")


reload_project("z_bs")
