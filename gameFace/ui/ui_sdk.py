from functools import partial
from gameFace.planeControls import importSDK, exportSDK, PlaneControls

from gameFace.ui.ui_loader import build_ui
from gameFace.data.config import *
from maya import cmds

import os

import yaml

uiFile = f"{os.path.dirname(__file__) }\\designer\\sdk.ui"

global data
global ui

def deleteSDK_UI():
    global ui
    ui.deleteLater()
    print('delete sdk UI')

def showSDK_UI():
    global ui

    if cmds.workspaceControl('FacialSDK_UI', q=1, ex=1):
        cmds.deleteUI('FacialSDK_UI')

    ui = build_ui(uiFile)
    setup_ui_logic()

    dock_windows = cmds.workspaceControl('FacialSDK_UI', retain=True, label='Facial SDK')
    dock_layout = cmds.paneLayout(configuration='single', p=dock_windows)
    cmds.control(ui.objectName(), e=True, p=dock_layout)


def setup_ui_logic():
    ui.bt_importSDK.clicked.connect(partial(importSDK))
    ui.bt_exportSDK.clicked.connect(partial(exportSDK))
    ui.bt_set.clicked.connect(partial(PlaneControls, "set"))
    ui.bt_mirror.clicked.connect(partial(print, "mir"))
    ui.bt_flip.clicked.connect(partial(print, "flip"))
    ui.bt_mirrorFlip.clicked.connect(partial(print, "MF"))

    # listWidget
    update_listWidget()
    ui.listWidget.currentItemChanged.connect(listViveClickCommand)


def listViveClickCommand(currentIndex, lastIndex):
    i = ui.listWidget.row(currentIndex)
    last_i = ui.listWidget.row(lastIndex)
    
    if last_i >= 0:
        if not data[last_i].driverAttr:
            return
        if cmds.objExists(data[last_i].driverAttr):
            cmds.setAttr(data[last_i].driverAttr, data[last_i].min)
            print(f"setAttr '{data[last_i].driverAttr}', {data[last_i].min}")
            

    if not data[i].driverAttr:
        return
    if not cmds.objExists(data[i].driverAttr):
        return
    cmds.setAttr(data[i].driverAttr, data[i].max)
    print(f"setAttr '{data[i].driverAttr}', {data[i].max}")




def update_listWidget():
    global data
    ui.listWidget.clear()
    try:
        data = yaml.unsafe_load(cmds.getAttr(f"{BRIDGE}.notes"))
    except:
        return
    for i in data:
        ui.listWidget.addItem(i.name)
    return data
