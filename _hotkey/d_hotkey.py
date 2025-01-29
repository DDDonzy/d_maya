import os
from maya import cmds, mel
from functools import partial
from UTILS.transform import reset_transformObjectValue_cmd
from .d_hotbox_ui import addUI

PRESS_COUNT = 0
DISPLAY_COUNT = 0


sys_hotBox = "modelPanel4ObjectPop"
melFileName = "menu_d_hotbox_ui.mel"
hotkeyFileName = "hotkey.mhk"

menuMelPath = os.path.join(os.path.dirname(__file__), melFileName).replace('\\', '/')
hotkeyPath = os.path.join(os.path.dirname(__file__), hotkeyFileName).replace('\\', '/')


d_hotBox_LMB = "d_hotbox_LMB"
d_hotBox_RMB = "d_hotbox_LMB"


def createUI():
    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)
    cmds.popupMenu(sys_hotBox, e=1, button=2)
    addUI(d_hotBox_LMB, button=3, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=partial(changeDisplayCount))
    addUI(d_hotBox_RMB, button=1, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=partial(changeDisplayCount))


def deleteUI():
    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)
    cmds.popupMenu(sys_hotBox, e=1, button=3)


def d_hotbox_press():
    global PRESS_COUNT

    PRESS_COUNT += 1
    createUI()


def d_hotbox_release():
    global PRESS_COUNT, DISPLAY_COUNT

    if PRESS_COUNT != DISPLAY_COUNT:
        reset_transformObjectValue_cmd(transform=True, userDefined=False)
    PRESS_COUNT = 0
    DISPLAY_COUNT = 0

    deleteUI()


def changeDisplayCount(*args, **kwargs):
    global DISPLAY_COUNT
    DISPLAY_COUNT += 1
    cmds.evalDeferred(partial(deleteUI))


def install_hotkey():
    cmds.hotkeySet(e=1, ip=hotkeyPath)
    print(menuMelPath)


def onMayaDroppedPythonFile(*args, **kwargs):
    install_hotkey()


