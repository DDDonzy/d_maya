import os
from maya import cmds, mel
from functools import partial

from m_utils.transform import reset_transform_cmd
from _hotkey.d_hotbox_ui import addUI

PRESS_COUNT = 0
DISPLAY_COUNT = 0


sys_hotBox = "modelPanel4ObjectPop"
hotkeyFileName = "hotkey.mhk"

hotkeyPath = os.path.join(os.path.dirname(__file__), hotkeyFileName).replace("\\", "/")


d_hotBox_LMB = "d_hotbox_LMB"
d_hotBox_RMB = "d_hotbox_RMB"


# Custom menu hotkeys are set to allow both left and right mouse buttons to activate the menu, so two menus are added.
# However, in Maya, the right mouse button setting doesn't work because the system's default hotkey is assigned to it, and system defaults have the highest priority.
# To work around this, the system's default hotkey is temporarily changed to the middle mouse button, and it is switched back to the right mouse button after the menu is called.


def createUI():

    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)
    # set sys_hotBox button = 2
    cmds.popupMenu(sys_hotBox, e=1, button=2)
    # add ui as mouser button 3
    addUI(d_hotBox_LMB, button=3, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=lambda *args, **kwargs: changeDisplayCount())
    # add ui as mouser button 1
    addUI(d_hotBox_RMB, button=1, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=lambda *args, **kwargs: changeDisplayCount())


def deleteUI():
    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)
    # set sys_hotBox button = 3
    cmds.popupMenu(sys_hotBox, e=1, button=3)


def d_hotbox_press():
    global PRESS_COUNT
    PRESS_COUNT += 1
    createUI()


def d_hotbox_release():
    global PRESS_COUNT, DISPLAY_COUNT

    if PRESS_COUNT != DISPLAY_COUNT:
        reset_transform_cmd(transform=True, userDefined=False)
    PRESS_COUNT = 0
    DISPLAY_COUNT = 0

    deleteUI()


def changeDisplayCount():
    global DISPLAY_COUNT
    DISPLAY_COUNT += 1
    cmds.evalDeferred(partial(deleteUI))


def install_hotkey():
    cmds.hotkeySet(e=1, ip=hotkeyPath)
    print("Hotkey installed.")


def onMayaDroppedPythonFile(*args, **kwargs):
    install_hotkey()
