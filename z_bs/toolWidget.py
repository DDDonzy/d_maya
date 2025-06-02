from z_bs.getMayaWidget import getMayaMainWindow, getMayaWidget
import z_bs.toolFunctions as tools
import z_bs.treeViewFunction as tf
from z_bs.showMessage import showMessage
from z_bs.getHistory import *
import z_bs.bsFunctions as bs

from PySide2 import QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType

from pathlib import Path
from importlib import reload
from functools import partial

from maya import cmds, mel
from maya.api import OpenMaya as om
reload(tf)
reload(bs)


# ui_path = r"E:\d_maya\z_bs\_addUI.ui"

current_dir = Path(__file__).parent
ui_path = current_dir / "_addUI.ui"
ui_path = str(ui_path.resolve())


print(ui_path)
ui, base = loadUiType(ui_path)


class ShapeToolsWidget(base, ui):
    def __init__(self, treeView: QtWidgets.QTreeView = None):
        super().__init__(getMayaMainWindow())
        self.treeView = treeView

        """complete variables."""
        self.meshLabel: QtWidgets.QLabel
        self.loadBsButton: QtWidgets.QPushButton
        self.loadTargetButton: QtWidgets.QPushButton
        self.addSculptButton: QtWidgets.QPushButton

        self.deleteSculptCheckBox: QtWidgets.QCheckBox
        self.addInbetweenCheckBox: QtWidgets.QCheckBox

        self.filterLineEdit: QtWidgets.QLineEdit
        self.filterLineEditWidget: QtWidgets.QWidget
        self.filterComboBox: QtWidgets.QComboBox
        self.meshLabel: QtWidgets.QLabel

        self.addonWidget: QtWidgets.QWidget
        self.filterWidget: QtWidgets.QWidget

        self.setupUi()

        if self.treeView:
            self.treeView.viewport().installEventFilter(self)

        # self.treeView.setParent(self)

    def setupUi(self):
        super().setupUi(self)

        """先清除所有shapeEditorManager的过滤器，避免文件自带的过滤器影响"""
        for manager in cmds.ls(type="shapeEditorManager"):
            cmds.setAttr(f"{manager}.filterString", "", type="string")
        #
        self.loadTargetButton.clicked.connect(self.loadTarget)
        self.loadBsButton.clicked.connect(self.loadBlendShape)
        self.filterLineEdit.textChanged.connect(self.filterChanged)
        self.filterComboBox.currentTextChanged.connect(self.filterChanged)
        self.filterComboBox.currentTextChanged.connect(self.updateBaseMeshLabel)
        self.addSculptButton.clicked.connect(self.addSculpt)

        self.treeView.selectionModel().selectionChanged.connect(self.updateBaseMeshLabel)

    def updateBaseMeshLabel(self):

        text = "None"
        target = bs.targetData()
        target.getDataFromShapeEditor()

        if target.baseMesh:
            if cmds.objExists(target.baseMesh):
                text = cmds.listRelatives(target.baseMesh, parent=1)[0]

        self.meshLabel.setText(text)
        if text == "None":
            self.meshLabel.setStyleSheet("")  # 不设置颜色
        else:
            self.meshLabel.setStyleSheet("color: #7ab5bf;")  # 红色

    def filterChanged(self):
        nodeText = self.filterComboBox.currentText().strip()
        if nodeText == "None":
            nodeText = ""
        targetText = self.filterLineEdit.text().strip()
        tf.treeView_filter(self.treeView, targetText, tf.SelectedItemType(3))
        tf.treeView_filter(self.treeView, nodeText, tf.SelectedItemType(2))
        tf.treeView_filter(self.treeView, nodeText, tf.SelectedItemType(1))

    def loadBlendShape(self):
        self.filterComboBox.clear()
        self.filterComboBox.addItem("None")

        blendShapes = []

        sel = cmds.ls(sl=1)
        for obj in sel:
            blendShapes.extend(get_history(obj, type="blendShape"))

        treeviewSelectedBSD = mel.eval("getShapeEditorTreeviewSelection 1")
        if treeviewSelectedBSD:
            blendShapes.extend(treeviewSelectedBSD)

        blendShapes = set(blendShapes)  # 去重
        if not blendShapes:
            showMessage("No blendShape node found in the selected in scene or shapeEdit.")
            return

        self.filterComboBox.addItems(blendShapes)
        self.filterComboBox.setCurrentIndex(1)

    def loadTarget(self):
        text = "&"
        targetList = mel.eval("getShapeEditorTreeviewSelection 14")
        targetNamelist = []
        if not targetList:
            targetNamelist = self.getNoZeroWeightTargets()
            if not targetNamelist:
                self.filterLineEdit.setText("")
                return

        for target in targetList:
            if "." in target:
                split = target.split(".")
                print(f"{split[0]}.w[{split[-1]}]")
                targetName = cmds.aliasAttr(f"{split[0]}.w[{split[-1]}]", q=1)
                targetNamelist.append(targetName)

        text = text.join(targetNamelist)
        self.filterLineEdit.setText(text)

    def getNoZeroWeightTargets(self):
        """
        Get all targets with non-zero weight from the selected blendShape node.
        """
        target = bs.targetData()
        target.getDataFromShapeEditor()

        if target.node is None:
            return []
        if not cmds.objExists(target.node):
            return []

        targetNames = cmds.listAttr(f"{target.node}.w", multi=True)
        for name in targetNames:
            if cmds.getAttr(f"{target.node}.{name}") == 0:
                targetNames.remove(name)
        return targetNames

    def addSculpt(self):
        """
        Add a sculpt to the selected blendShape node.
        """
        target = bs.targetData()
        target.getDataFromShapeEditor()
        if target.targetIdx < 0:
            showMessage("No target selected in shape editor.")
            return

        sel = cmds.ls(sl=1)
        if not cmds.ls(sl=1):
            showMessage("No mesh selected.")
            return
        sculptGeo = sel[0]
        shapes = get_shape(sculptGeo)
        if not shapes:
            showMessage("Selected object is not a mesh.")
            return
        shape = shapes[0]
        if not cmds.objectType(shape, isa="mesh"):
            showMessage("Selected object is not a mesh.")

        bs.add_sculptGeo(sculptGeo=shape, targetData=target, addInbetween=self.addInbetweenCheckBox.isChecked())

        if not self.deleteSculptCheckBox.isChecked():
            cmds.delete(sculptGeo)
        showMessage("Add sculpt target successfully.")

    def autoSetWeight(self):
        """
        Automatically set the weight of the selected target.
        """
        target = bs.targetData()
        target.getDataFromShapeEditor()
        if target.targetIdx < 0:
            return

        weightAttr = f"{target.node}.w[{target.targetIdx}]"

        v = 0
        if target.inbetweenIdx == 6000:
            w = cmds.getAttr(weightAttr)
            if w >= 0.5:
                v = 0
            else:
                v = 1
        else:
            v = (target.inbetweenIdx - 5000) / 1000

        cmds.setAttr(weightAttr, v)
        showMessage(f"Set {target.node}.w[{target.targetIdx}] to {v} .")

    def eventFilter(self, obj, event):
        if obj == self.treeView.viewport() and event.type() == QtCore.QEvent.MouseButtonRelease:
            if event.button() == QtCore.Qt.MiddleButton:
                index = self.treeView.indexAt(event.pos())
                if index.isValid():
                    self.autoSetWeight()
                return True
        return super().eventFilter(obj, event)
