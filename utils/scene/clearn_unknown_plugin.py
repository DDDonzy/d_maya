from maya import cmds as cmds


def remove_unknown_plugin():
    print("REMOVE_UNKNOWN_PLUGIN:")
    unknown_plugin = cmds.unknownPlugin(q=1, l=1)
    if not unknown_plugin:
        return
    for x in unknown_plugin:
        try:
            cmds.unknownPlugin(x, r=1)
            print(f"    REMOVE: {x}")
        except Exception:
            print(f"  ERROR:{x}")


remove_unknown_plugin()
