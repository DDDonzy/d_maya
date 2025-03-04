from __future__ import print_function
from face.fn.mPartial import partial
from face.fn.cvFn import export_cvData, import_cvData

from face.build import build, importUVPinWeights, exportUVPinWeights
from face.data.config import *
from face.ui import ui_sdk
from face.ui.ui_loader import build_ui
from face.fit import importFit, exportFit, mirrorDuplicateTransform_cmd, hideClass, hidePart, alignFromSec
from face.fn.maxCommand import toMaxCommand
from face.fn.showMessage import showMessage

from maya import cmds

import os


global ui

uiFile = os.path.join(os.path.dirname(__file__), "designer", "main.ui")


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
    ui.bt_sdk.clicked.connect(partial(ui_sdk.show_UI))
    ui.bt_importFit.clicked.connect(partial(importFit))
    ui.bt_exportFit.clicked.connect(partial(exportFit))
    ui.bt_visClass.clicked.connect(partial(hideClass))
    ui.bt_visPart.clicked.connect(partial(hidePart))
    ui.bt_mirror.clicked.connect(partial(mirrorDuplicateTransform_cmd))
    ui.bt_importShape.clicked.connect(partial(import_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    ui.bt_exportShape.clicked.connect(partial(export_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    ui.bt_exportMax.clicked.connect(partial(exportMax))
    ui.bt_exportPoseAsset.clicked.connect(partial(print, "Export PoseAsset"))
    ui.bt_importSDK.clicked.connect(partial(importUVPinWeights))
    ui.bt_exportSDK.clicked.connect(partial(exportUVPinWeights))
    ui.bt_build.clicked.connect(partial(build, "Face"))
    ui.bt_align.clicked.connect(partial(alignFromSec))


def exportMax():
    command = toMaxCommand()
    command.exportToMax()
    showMessage("Export Max Done")
    print("Export Max")
