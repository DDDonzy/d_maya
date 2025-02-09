from functools import partial

from gameFace.ui.ui_loader import build_ui
from gameFace.ui.ui_sdk import showSDK_UI
from gameFace.fit import importFit, exportFit, mirrorDuplicateTransform_cmd, hideClass, hidePart
from gameFace.build import build
from gameFace.data.config import *
from UTILS.control.cvShape import export_cvData, import_cvData
from maya import cmds


def showUI():
    path = r"E:\d_maya\gameFace\ui\designer\main.ui"
    ui = build_ui(path)
    setup_ui_logic(ui)

    if cmds.workspaceControl('FacialMain_UI', q=1, ex=1):
        cmds.deleteUI('FacialMain_UI')

    dock_windows = cmds.workspaceControl('FacialMain_UI', retain=True, label='Facial')
    dock_layout = cmds.paneLayout(configuration='single', p=dock_windows)
    cmds.control(ui.objectName(), e=True, p=dock_layout)


def setup_ui_logic(ui):
    ui.bt_sdk.clicked.connect(partial(showSDK_UI))
    ui.bt_importFit.clicked.connect(partial(importFit))
    ui.bt_exportFit.clicked.connect(partial(exportFit))
    ui.bt_visClass.clicked.connect(partial(hideClass))
    ui.bt_visPart.clicked.connect(partial(hidePart))
    ui.bt_mirror.clicked.connect(partial(mirrorDuplicateTransform_cmd))
    ui.bt_importShape.clicked.connect(partial(import_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    ui.bt_exportShape.clicked.connect(partial(export_cvData, startingDirectory=DEFAULT_SHAPES_DIR))
    ui.bt_exportMax.clicked.connect(partial(print, "Export Max"))
    ui.bt_exportPoseAsset.clicked.connect(partial(print, "Export PoseAsset"))
    ui.bt_build.clicked.connect(partial(build, "Face"))
