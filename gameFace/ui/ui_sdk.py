from functools import partial

from gameFace.ui.ui_loader import build_ui
from maya import cmds


def showSDK_UI():
    path = r"E:\d_maya\gameFace\ui\designer\sdk.ui"
    ui = build_ui(path)
    setup_ui_logic(ui)

    if cmds.workspaceControl('FacialSDK_UI', q=1, ex=1):
        cmds.deleteUI('FacialSDK_UI')

    dock_windows = cmds.workspaceControl('FacialSDK_UI', retain=True, label='Facial SDK')
    dock_layout = cmds.paneLayout(configuration='single', p=dock_windows)
    cmds.control(ui.objectName(), e=True, p=dock_layout)


def setup_ui_logic(ui):
    pass
