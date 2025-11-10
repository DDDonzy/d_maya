from maya import cmds as cmds
import log


def removeUnknownPlugin():
    log.debug("REMOVE_UNKNOWN_PLUGIN:")
    unknown_plugin = cmds.unknownPlugin(q=1, l=1)
    if not unknown_plugin:
        log.warning("None unknown plugin found.")
        return
    for x in unknown_plugin:
        try:
            cmds.unknownPlugin(x, r=1)
            log.debug("    REMOVE: {}", x)
        except Exception:
            log.warning("    ERROR:{}", x)
    log.success("REMOVE_UNKNOWN_PLUGIN_DONE")
