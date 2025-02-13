from __future__ import print_function
from face.fn.mPartial import partial
from face.fn.showMessage import showMessage
from face.fn.mirrorEnv import MIRROR_CONFIG

from face.data.config import *
from face.ui.ui_loader import build_ui
from face.pose import setPose, delPoseData, mirrorPose, flipPose, importPose, exportPose, pose_scale


import os
import yaml

from PySide2.QtGui import QFont, QBrush, QColor
from PySide2.QtCore import Qt

from maya import cmds


uiFile = os.path.join(os.path.dirname(__file__), "designer", "sdk.ui")


global data
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
    # command connect
    ui.bt_importPose.clicked.connect(partial(import_pose_command))
    ui.bt_exportPose.clicked.connect(partial(export_pose_command))
    ui.bt_set.clicked.connect(partial(set_pose_command))
    ui.bt_mirror.clicked.connect(partial(mirror_pose_command))
    ui.bt_flip.clicked.connect(partial(flip_pose_command))
    ui.bt_mirrorFlip.clicked.connect(partial(mirror_flip_all_command))
    ui.bt_defaultPose.clicked.connect(partial(default_pose_command))
    ui.bt_delPoseData.clicked.connect(partial(del_pose_command))
    ui.bt_add.clicked.connect(partial(scaleAdd_pose_command))
    ui.bt_sub.clicked.connect(partial(scaleSub_pose_command))

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
        data = yaml.load(cmds.getAttr("{}.notes".format(BRIDGE)))
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


def listWidget_currentIndex():
    current_item = ui.listWidget.currentIndex()
    if not current_item:
        return None
    return current_item.row()


def filter_items_command():
    filter_text = ui.text_filter.text().lower()
    for item in ui.listWidget_items:
        if filter_text in item.text().lower():
            item.setHidden(False)
        else:
            item.setHidden(True)


def set_pose_command():
    current_index = listWidget_currentIndex()
    if current_index >= 0:
        setPose(current_index)
        showMessage("Set Pose")


def mirror_pose_command():
    current_index = listWidget_currentIndex()
    if current_index >= 0:
        mirrorPose(data[current_index].name)
    showMessage("Mirror Pose")


def flip_pose_command():
    current_index = listWidget_currentIndex()
    if current_index >= 0:
        flipPose(data[current_index].name)
    showMessage("Flip Pose")


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
    showMessage("Auto Flip/Mirror All.")


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
    showMessage("Reset To Default Pose.")


def del_pose_command():
    current_index = listWidget_currentIndex()
    if current_index >= 0:
        delPoseData(current_index)
        showMessage("Delete Pose Data.")


def scaleAdd_pose_command():
    current_index = listWidget_currentIndex()
    pose_scale(current_index, 1.1)
    showMessage("*= 1.1")


def scaleSub_pose_command():
    current_index = listWidget_currentIndex()
    pose_scale(current_index, 0.9)
    showMessage("*= 0.9")
