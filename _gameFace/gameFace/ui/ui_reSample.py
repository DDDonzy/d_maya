from UTILS.other.mPartial import partial

from gameFace.reSample import *
from gameFace.ui.ui_loader import build_ui
from gameFace.fit import mirrorDuplicateTransform_cmd

from maya import cmds

import os

uiFile = os.path.join(os.path.dirname(__file__), "designer", "reSample.ui")

global ui


def show_UI():
    global ui
    ui = build_ui(uiFile)
    
    workSpaceControlName = f"{ui.objectName()}_workSpaceControl"
    if cmds.workspaceControl(workSpaceControlName, q=1, ex=1):
        cmds.deleteUI(workSpaceControlName)

    setup_ui_logic()

    dock_windows = cmds.workspaceControl(workSpaceControlName, retain=True, label=ui.windowTitle())
    dock_layout = cmds.paneLayout(configuration='single', p=dock_windows)
    cmds.control(ui.objectName(), e=True, p=dock_layout)


def setup_ui_logic():
    ui.pt_brow.clicked.connect(partial(reSample_brow_command))
    # ui.bt_importFit.clicked.connect(partial(importFit))
    # ui.bt_exportFit.clicked.connect(partial(exportFit))
    # ui.bt_visClass.clicked.connect(partial(hideClass))
    # ui.bt_visPart.clicked.connect(partial(hidePart))
    # ui.bt_mirror.clicked.connect(partial(mirrorDuplicateTransform_cmd))
    # ui.bt_importShape.clicked.connect(partial(import_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    # ui.bt_exportShape.clicked.connect(partial(export_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    # ui.bt_exportMax.clicked.connect(partial(print, "Export Max"))
    # ui.bt_exportPoseAsset.clicked.connect(partial(print, "Export PoseAsset"))
    # ui.bt_build.clicked.connect(partial(build, "Face"))


def reSample_brow_command():
    value = ui.brow_spinBox.value()
    base = get_brow("L_")
    reSample(base,value)
    base = get_brow("R_")
    reSample(base,value)