import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget


def getMayaMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget) if main_window_ptr else None


def getMayaControl(name):
    maya_control = omui.MQtUtil.findControl(name)
    return wrapInstance(int(maya_control), QWidget) if maya_control else None


if __name__ == "__main__":
    from maya import cmds
    bsPanelName = cmds.getPanel(type="shapePanel")[0]
    getMayaControl()
