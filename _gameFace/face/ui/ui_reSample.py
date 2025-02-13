from face.fn.mPartial import partial

from face.ui.ui_loader import build_ui
from face.fit import mirrorDuplicateTransform_cmd
from face.fn.reSample import reSample
from face.control import get_brow, get_eyeLine, get_lid, get_lip, get_cheek

from maya import cmds

import os

uiFile = os.path.join(os.path.dirname(__file__), "designer", "reSample.ui")

global ui


def show_UI():
    global ui
    ui = build_ui(uiFile)

    workSpaceControlName = "{}_workSpaceControl".format(ui.objectName())
    if cmds.workspaceControl(workSpaceControlName, q=1, ex=1):
        cmds.deleteUI(workSpaceControlName)

    setup_ui_logic()

    dock_windows = cmds.workspaceControl(workSpaceControlName, retain=True, label=ui.windowTitle())
    dock_layout = cmds.paneLayout(configuration='single', p=dock_windows)
    cmds.control(ui.objectName(), e=True, p=dock_layout)


def setup_ui_logic():
    ui.pt_brow.clicked.connect(partial(reSample_brow_command))
    ui.pt_eyeline.clicked.connect(partial(reSample_eyeLine_command))
    ui.pt_lid.clicked.connect(partial(resample_lid_command))
    ui.pt_lip.clicked.connect(partial(resample_lip_command))
    ui.pt_cheek.clicked.connect(partial(resample_cheek_command))


def reSample_brow_command():
    num = ui.brow_spinBox.value() - 2
    reSample([x.fit for x in get_brow("L_")], num)
    reSample([x.fit for x in get_brow("R_")], num)


def reSample_eyeLine_command():
    num = ui.eyeLine_spinBox.value() - 2
    reSample([x.fit for x in get_eyeLine("L_")], num)
    reSample([x.fit for x in get_eyeLine("R_")], num)


def resample_lid_command():
    num = ui.lid_spinBox.value() - 2
    reSample([x.fit for x in get_lid("L_")], num)
    reSample([x.fit for x in get_lid("R_")], num)


def resample_lip_command():
    num = ui.lip_spinBox.value() - 2
    reSample([x.fit for x in get_lip("L_")], num)
    reSample([x.fit for x in get_lip("R_")], num)


def resample_cheek_command():
    num = ui.cheek_spinBox.value() - 2
    reSample([x.fit for x in get_cheek("L_")], num)
    reSample([x.fit for x in get_cheek("R_")], num)
