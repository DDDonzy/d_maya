# filepath: e:\d_maya\z_bs\reloader.py
# z_bs/_tools/reloader.py
import sys
import importlib

from loguru import logger as log

log.remove()
log.add(sys.stdout, format="| <level>{level: <8}</level> | <green>{time:HH:mm:ss}</green> | <cyan>{name}: {function}  line {line}</cyan> - <level>{message}</level>")

def reload_project(project_prefix: str):

    if not isinstance(project_prefix, str) or not project_prefix:
        log.error("A valid string must be provided for project_prefix.")
        return

    log.info(f"--- Starting reload of all '{project_prefix}' related modules ---")

    modules_to_reload = [
        name for name in sys.modules
        if name.startswith(project_prefix)
    ]

    if not modules_to_reload:
        log.warning(f"No loaded modules found starting with '{project_prefix}', no reload needed.")
        return

    modules_to_reload.sort(key=lambda name: name.count('.'), reverse=True)

    reloaded_count = 0
    failed_count = 0
    for module_name in modules_to_reload:
        try:
            module_obj = sys.modules[module_name]
            importlib.reload(module_obj)
            # Using loguru's specific success level for clearer output
            log.success(f"Successfully reloaded: {module_name}")
            reloaded_count += 1
        except Exception:
            # loguru's exception method automatically logs complete error stack
            log.exception(f"Failed to reload module: {module_name}")
            failed_count += 1

    log.info("--- Reload completed ---")
    log.info(f"Summary: {reloaded_count} successful, {failed_count} failed.")
    

if __name__ == "__main__":
    reload_project("z_bs")
