from maya import cmds as cmds
from UTILS.ui.showMessage import showMessage


def removeUnknownPlugin():
    print("REMOVE_UNKNOWN_PLUGIN:")
    unknown_plugin = cmds.unknownPlugin(q=1, l=1)
    if not unknown_plugin:
        showMessage("REMOVE_UNKNOWN_PLUGIN_DONE")
        return
    for x in unknown_plugin:
        try:
            cmds.unknownPlugin(x, r=1)
            print(f"    REMOVE: {x}")
        except Exception:
            print(f"  ERROR:{x}")
    showMessage("REMOVE_UNKNOWN_PLUGIN_DONE")


# removeUnknownPlugin()
