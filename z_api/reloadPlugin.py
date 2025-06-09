import os
from pathlib import Path
import maya.cmds as cmds
import PySide2.QtWidgets as QtWidgets

PLUGIN_PATH = r"E:\d_maya\z_api\brushPlugin.py"
PLUGIN_NAME = Path(PLUGIN_PATH).stem


def reload_plugin():
    """重载Maya插件"""

    if not os.path.exists(PLUGIN_PATH):
        raise RuntimeError(f"Path not found: {PLUGIN_PATH}")

    # uninstall
    if cmds.pluginInfo(PLUGIN_NAME, query=True, loaded=True):
        print(f"UNINSTALL: plugin: {PLUGIN_NAME}")
        cmds.unloadPlugin(PLUGIN_NAME)
        cmds.refresh(f=1)

    # install
    print(f"INSTALL: plugin: {PLUGIN_PATH}")
    cmds.loadPlugin(PLUGIN_PATH)
    cmds.refresh(f=1)

    # check
    if cmds.pluginInfo(PLUGIN_NAME, query=True, loaded=True):
        print(f"'{PLUGIN_NAME}' install successfully!")


def initScene():
    cmds.file(new=True, force=True)



if __name__ == "__main__":
    initScene()
    reload_plugin()
    
    cmds.setToolTo(cmds.customBlendShapeBrush())
