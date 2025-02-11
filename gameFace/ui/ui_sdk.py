from UTILS.other.mPartial import partial
from UTILS.ui.showMessage import showMessage
from UTILS.mirrorEnv import MIRROR_CONFIG

from gameFace.data.config import *
from gameFace.ui.ui_loader import build_ui
from gameFace.pose import setPose, delPoseData, mirrorPose, flipPose, importPose, exportPose


import os
import yaml

from PySide2.QtGui import QFont, QBrush, QColor
from PySide2.QtCore import Qt

from maya import cmds


uiFile = f"{os.path.dirname(__file__) }\\designer\\sdk.ui"

global data
global ui


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
    # command connect
    ui.bt_importPose.clicked.connect(partial(import_pose_command))
    ui.bt_exportPose.clicked.connect(partial(export_pose_command))
    ui.bt_set.clicked.connect(partial(set_pose_command))
    ui.bt_mirror.clicked.connect(partial(mirror_pose_command))
    ui.bt_flip.clicked.connect(partial(flip_pose_command))
    ui.bt_mirrorFlip.clicked.connect(partial(mirror_flip_all_command))
    ui.bt_defaultPose.clicked.connect(partial(default_pose_command))
    ui.bt_delPoseData.clicked.connect(partial(del_pose_command))

    # listWidget
    update_listWidget()
    ui.listWidget.currentItemChanged.connect(listWidget_change_command)
    # text filter
    ui.text_filter.textChanged.connect(filter_items_command)


def listWidget_change_command(currentIndex, lastIndex):
    i = ui.listWidget.row(currentIndex)
    last_i = ui.listWidget.row(lastIndex)

    if last_i >= 0:
        if data[last_i].driverAttr:
            if cmds.objExists(data[last_i].driverAttr):
                cmds.setAttr(data[last_i].driverAttr, data[last_i].min)

    if data[i].driverAttr:
        if cmds.objExists(data[i].driverAttr):
            cmds.setAttr(data[i].driverAttr, data[i].max)


def update_listWidget():
    global data

    ui.listWidget_items = []
    ui.listWidget.clear()
    try:
        data = yaml.unsafe_load(cmds.getAttr(f"{BRIDGE}.notes"))
    except:
        return

    font = QFont()
    font.setBold(True)
    font.setPointSize(10)
    for i, x in enumerate(data):
        ui.listWidget.addItem(x.name)
        item = ui.listWidget.item(i)

        if "__" in x.name and x.driverAttr is None:
            item.setText(x.name.replace("__", ""))
            item.setFont(font)
            color = QColor(255, 255, 255)
            color.setAlpha(50)
            item.setBackground(QBrush(color))
            item.setTextAlignment(Qt.AlignCenter)
        else:
            ui.listWidget_items.append(item)

    return data


def filter_items_command():
    filter_text = ui.text_filter.text().lower()
    for item in ui.listWidget_items:
        if filter_text in item.text().lower():
            item.setHidden(False)
        else:
            item.setHidden(True)


def set_pose_command():
    current_item = ui.listWidget.currentIndex()
    if not current_item:
        return
    current_index = current_item.row()
    if current_index >= 0:
        setPose(current_index)
        showMessage("Set Pose")


def mirror_pose_command():
    current_item = ui.listWidget.currentIndex()
    if not current_item:
        return
    current_index = current_item.row()
    if current_index >= 0:
        mirrorPose(data[current_index].name)


def flip_pose_command():
    current_item = ui.listWidget.currentIndex()
    if not current_item:
        return
    current_index = current_item.row()
    if current_index >= 0:
        flipPose(data[current_index].name)


def mirror_flip_all_command():
    for i, x in enumerate(data):
        if not x.driverAttr:
            continue
        source = x.name
        target = MIRROR_CONFIG.exchange(x.name)[0]
        if source == target:
            mirrorPose(source)
            continue
        if MIRROR_CONFIG.l.lower() in x.name.lower().split("_"):
            flipPose(source)
            continue


def import_pose_command():
    importPose()
    showMessage("Import PoseData")


def export_pose_command():
    exportPose()
    showMessage("Export PoseData")


def default_pose_command():
    for x in data:
        if x.driverAttr:
            if cmds.objExists(x.driverAttr):
                cmds.setAttr(x.driverAttr, x.min)
    showMessage("Reset to default pose.")


def del_pose_command():
    current_item = ui.listWidget.currentIndex()
    if not current_item:
        return
    current_index = current_item.row()
    if current_index >= 0:
        delPoseData(current_index)
        showMessage("Set Pose")
