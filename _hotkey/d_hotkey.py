import os
from maya import cmds, mel
from functools import partial
from UTILS.transform import reset_transformObjectValue_cmd

STATUS = False


sys_hotBox = "modelPanel4ObjectPop"
melFileName = "menu_d_hotbox_ui.mel"
hotkeyFileName = "hotkey.mhk"

menuMelPath = os.path.join(os.path.dirname(__file__), melFileName).replace('\\', '/')
hotkeyPath = os.path.join(os.path.dirname(__file__), hotkeyFileName).replace('\\', '/')


d_hotBox_LMB = "d_hotbox_LMB"
d_hotBox_RMB = "d_hotbox_LMB"


def d_hotbox_press():
    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)

    cmds.popupMenu(sys_hotBox, e=1, button=2)
    cmds.popupMenu(d_hotBox_LMB, button=3, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=partial(setStatus, True))
    mel.eval(f'source "{menuMelPath}"')
    cmds.popupMenu(d_hotBox_RMB, button=1, parent=mel.eval("findPanelPopupParent"), aob=0, mm=1, pmc=partial(setStatus, True))
    mel.eval(f'source "{menuMelPath}"')


def d_hotbox_release():
    if cmds.popupMenu(d_hotBox_LMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_LMB)
    if cmds.popupMenu(d_hotBox_RMB, q=1, ex=1):
        cmds.deleteUI(d_hotBox_RMB)
    cmds.popupMenu(sys_hotBox, e=1, button=3)
    if not STATUS:
        reset_transformObjectValue_cmd(transform=True, userDefined=False)
    setStatus(status=False)


def setStatus(status, *args, **kwargs):
    global STATUS
    STATUS = status


def install_hotkey():
    cmds.hotkeySet(e=1, ip=hotkeyPath)
    print(menuMelPath)


def onMayaDroppedPythonFile(*args, **kwargs):
    install_hotkey()
