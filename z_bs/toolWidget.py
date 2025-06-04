from z_bs.getMayaWidget import getMayaMainWindow, getMayaWidget
import z_bs.treeViewFunction as tf
from z_bs.showMessage import showMessage
from z_bs.getHistory import *
import z_bs.bsFunctions as bs
import z_bs.uiLoader as uiLoader
from z_bs import _debugUI

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
uiBase = uiLoader.uiFileLoader(ui_path)

# TODO maya treeview 选中后，不太好清空选择项，尤其是页面满了的时候，考虑一下点击已经选择的item，清空选择项。


def getMayaPanelName(panelType):
    panels = cmds.getPanel(type=panelType)
    return [f"{panel}Window" for panel in panels]


def getShapeEditorWidgets():
    panelNames = getMayaPanelName("shapePanel")
    return [getMayaWidget(panelName) for panelName in panelNames]


class ShapeToolsWidget(uiBase):
    def __init__(self):
        super().__init__()

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
        self.expandButton: QtWidgets.QPushButton
        self.proximityWrapRadioButton: QtWidgets.QRadioButton
        self.wrapRadioButton: QtWidgets.QRadioButton
        self.proximityWrapPag: QtWidgets.QScrollArea
        self.wrapPag: QtWidgets.QScrollArea

        self.openShapeEditor()
        self.setupUi()

    def closeShapeEditor(self):
        shapeEditorNames = getMayaPanelName("shapePanel")
        for shapeEditor in shapeEditorNames:
            if cmds.window(shapeEditor, ex=1):
                cmds.deleteUI(shapeEditor)

    def openShapeEditor(self):
        self.closeShapeEditor()
        cmds.ShapeEditor()
        # cmds.refresh(f=1)

        shapeEditorWidgets = getShapeEditorWidgets()  # get all Shape Editor widgets
        if not shapeEditorWidgets:
            raise RuntimeError("Shape Editor widget not found.")

        """
        获取 maya 自带 ui 控件
        """
        shapeEditorWidget = shapeEditorWidgets[0]  # get the first Shape Editor widget
        # shapeEditorWidget.hide()
        shapeEditorMenuBar = shapeEditorWidget.findChild(QtWidgets.QMenuBar)
        shapeEditorPanel = shapeEditorMenuBar.parent()
        # hide all other widgets in the shape editor panel except the menu bar
        for x in shapeEditorPanel.children():
            if isinstance(x, QtWidgets.QWidget) and x != shapeEditorMenuBar:
                x.hide()
        # parent the shape editor widget to the main window
        self.setParent(shapeEditorPanel)
        # get maya tree view
        mayaTreeView = shapeEditorWidget.findChild(QtWidgets.QTreeView)

        coreWidget: QtWidgets.QWidget = mayaTreeView.parent().parent().parent()

        """
        替换控件
        """
        parentLayout = self.baseTreeViewWidget.layout()
        parentLayout.addWidget(mayaTreeView)
        self.treeView = self.baseTreeViewWidget.findChild(QtWidgets.QTreeView)
        self.treeView.setParent(self.baseTreeViewWidget)

        reParentList = coreWidget.children()
        reParentDone = []
        for item in reParentList:
            if not item.findChild(QtWidgets.QTreeView):
                if isinstance(item, QtWidgets.QPushButton):
                    item.setParent(self.bsAddWidget)
                    self.bsAddWidget.layout().addWidget(item)
                    reParentDone.append(item)
        for x in reParentDone[3:]:
            x.hide()
        coreWidget.hide()
        #
        # debug_tool = _debugUI.WidgetDebugTool(shapeEditorWidget)
        # debug_tool.show()

    def setupUi(self):
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

        self.meshLabel.installEventFilter(self)
        self.proximityWrapRadioButton.toggled.connect(self.wrapAttrsPagVis)
        
        self.wrapAttrsPagVis()

        if self.treeView:
            self.treeView.viewport().installEventFilter(self)
            self.addHeaderButton()
            self.autoExpandOrCollapse()
            self.treeView.selectionModel().selectionChanged.connect(self.updateBaseMeshLabel)

    def updateBaseMeshLabel(self):

        text = "None"
        target = bs.targetData()
        target.getDataFromShapeEditor()

        if target.baseMesh:
            if cmds.objExists(target.baseMesh):
                text = cmds.listRelatives(target.baseMesh, parent=1)[0]

        self.meshLabel.setText(text)

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
        # TODO  考虑添加 bsTargetGroup 支持
        # TODO  自动加载有权重的target，不太好使，必须选择 bs节点才行。考虑优化一下，
        baseText = self.filterLineEdit.text()
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
                targetName = cmds.aliasAttr(f"{split[0]}.w[{split[-1]}]", q=1)
                targetNamelist.append(targetName)

        text = text.join(targetNamelist)
        if baseText == text:
            text = ""
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

        targetNames = []
        tolerance = 1e-5
        for name in cmds.listAttr(f"{target.node}.w", multi=True):
            w = cmds.getAttr(f"{target.node}.{name}")
            if abs(w) > tolerance:
                targetNames.append(name)
        return targetNames

    def addSculpt(self):
        # TODO  有bug！不添加inbetween的时候，假设当前bs权重为0.5，添加sculpt结果和maya自带的editSculpt不一致。
        #       问题可能在于 这里使用的是cmds.sculptTarget，toolModify文件中使用的方法可这里不一样，找一找啥原因？
        #       也有可能是 bs.inputTarget.sculptWeights 的问题，可能maya自带的editSculpt会自动设置这个值。
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
        """鼠标哦中键点击事件过滤器，用于自动设置权重"""
        # TODO 需要考虑清空选择项目，是否用这种方式比较好？
        # 再考虑下一下，goToPose 用什么快捷键，以及实现方式。
        if self.treeView:
            if obj == self.treeView.viewport() and event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.MiddleButton:
                    index = self.treeView.indexAt(event.pos())
                    if index.isValid():
                        self.autoSetWeight()
                    return True

        if obj == self.meshLabel and event.type() == QtCore.QEvent.MouseButtonPress:
            self.selectBaseMesh()

            return True
        return super().eventFilter(obj, event)

    def addHeaderButton(self):
        header = self.treeView.header()
        self.expandButton.setParent(header)
        self.expandButton.setFixedHeight(header.height() - 2)
        self.expandButton.setFixedWidth(header.height() - 2)
        self.expandButton.clicked.connect(self.autoExpandOrCollapse)
        self.updateHeaderButtonPos()
        header.sectionResized.connect(self.updateHeaderButtonPos)
        header.sectionMoved.connect(self.updateHeaderButtonPos)
        header.geometriesChanged.connect(self.updateHeaderButtonPos)

    def updateHeaderButtonPos(self):
        header = self.treeView.header()
        section = 0  # 你想放按钮的列号
        x = header.sectionPosition(section)
        y = 0
        h = header.height()
        # 按钮放在该列header的左侧
        self.expandButton.move(x + 2, y + (h - self.expandButton.height()) // 2)

    def selectBaseMesh(self):
        mesh = self.meshLabel.text()
        if mesh == "None":
            return
        else:
            if cmds.objExists(mesh):
                cmds.select(mesh)
            else:
                showMessage(f"{mesh} does not exist in the scene.")

    def autoExpandOrCollapse(self):
        # self.treeView.expandAll()
        # self.treeView.collapseAll()

        bsNodeItems = []
        isExpand = []
        model = self.treeView.model()
        for _, index in tf.TreeViewIterator(self.treeView):
            item = model.itemFromIndex(index)
            if not item:
                continue
            item_data = item.data()
            if not item_data:
                continue
            # 默认展开 blendShape_group
            if tf.SelectedItemType(item_data) == tf.SelectedItemType.blendShape_group:
                self.treeView.expand(item.index())
            # blendShape_node 添加到列表中，进行后续判断是否展开
            if tf.SelectedItemType(item_data) == tf.SelectedItemType.blendShape_node:
                bsNodeItems.append((item, item.index()))
                isExpand.append(self.treeView.isExpanded(item.index()))
            # 默认不展开 inbetween
            if tf.SelectedItemType(item_data) == tf.SelectedItemType.blendShape_target:
                self.treeView.collapse(item.index())
            # 默认展开 target group
            if tf.SelectedItemType(item_data) == tf.SelectedItemType.blendShape_targetGroup:
                self.treeView.expand(item.index())

        if any(isExpand):
            for item, index in bsNodeItems:
                self.treeView.collapse(index)

        else:
            # 如果没有展开任何blendShape_node，则展开所有选择的以及父层级
            # 获取当前选择的所有index
            selected_indexes = self.treeView.selectedIndexes()
            for index in selected_indexes:
                self.treeView.expand(index)
                # 向上递归展开所有父节点
                parent = index.parent()
                while parent.isValid():
                    self.treeView.expand(parent)
                    parent = parent.parent()
                # 展开当前选中项
                self.treeView.expand(index)

    def wrapAttrsPagVis(self):
        """
        切换 proximityWrap 的页面可见性
        """
        
        self.proximityWrapPag.setVisible(self.proximityWrapRadioButton.isChecked())
        self.wrapPag.setVisible(self.wrapRadioButton.isChecked())



#
if __name__ == "__main__":
    bsUI = ShapeToolsWidget()
    bsUI.show()
