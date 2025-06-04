from z_bs.getMayaWidget import getMayaWidget
import z_bs.treeViewFunction as tf
from z_bs.showMessage import showMessage
from z_bs.getHistory import *
import z_bs.bsFunctions as bs
import z_bs._uiLoader as _uiLoader

from PySide2 import QtWidgets, QtCore

from pathlib import Path
from importlib import reload

from maya import cmds, mel
from maya.api import OpenMaya as om

from z_bs.icon import qrc as x

reload(tf)
reload(bs)


# ui_path = r"E:\d_maya\z_bs\_addUI.ui"

current_dir = Path(__file__).parent
ui_path = current_dir / "_addUI.ui"
ui_path = str(ui_path.resolve())
print(ui_path)
uiBase = _uiLoader.uiFileLoader(ui_path)

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
        self.addSetsButton: QtWidgets.QPushButton

        self.deleteSculptCheckBox: QtWidgets.QCheckBox
        self.addInbetweenCheckBox: QtWidgets.QCheckBox

        self.filterLineEdit: QtWidgets.QLineEdit
        self.filterLineEditWidget: QtWidgets.QWidget
        self.filterComboBox: QtWidgets.QComboBox
        self.meshLabel: QtWidgets.QLabel
        self.bsLabel: QtWidgets.QLabel

        self.addonWidget: QtWidgets.QWidget
        self.filterWidget: QtWidgets.QWidget
        self.expandButton: QtWidgets.QPushButton
        self.proximityWrapRadioButton: QtWidgets.QRadioButton
        self.wrapRadioButton: QtWidgets.QRadioButton
        self.proximityWrapPag: QtWidgets.QScrollArea
        self.wrapPag: QtWidgets.QScrollArea

        self.treeView: QtWidgets.QTreeWidget

        self.openShapeEditor()
        self.setupUi()
        self.splitter.setSizes([300, 1])

    def closeShapeEditor(self):
        """ close shape editor if it is open """
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

    def setupUi(self):
        """先清除所有shapeEditorManager的过滤器，避免文件自带的过滤器影响"""
        for manager in cmds.ls(type="shapeEditorManager"):
            cmds.setAttr(f"{manager}.filterString", "", type="string")
        #
        self.loadTargetButton.clicked.connect(self.loadTarget)
        self.loadBsButton.clicked.connect(self.loadBlendShape)
        self.filterLineEdit.textChanged.connect(self.filterChanged)
        self.filterComboBox.currentTextChanged.connect(self.filterChanged)
        self.addSculptButton.clicked.connect(self.addSculpt)
        self.proximityWrapRadioButton.toggled.connect(self.wrapAttrsPagVis)
        self.addSetsButton.clicked.connect(self.addDynamicButton)

        self.treeView.selectionModel().selectionChanged.connect(self.updateObjectLabel)
        self.treeView.viewport().installEventFilter(self)
        self.meshLabel.installEventFilter(self)
        self.bsLabel.installEventFilter(self)

        self.modifyExpandButton()
        self.treeViewExpandOrCollapse()

        self.wrapAttrsPagVis()

    def updateObjectLabel(self):

        meshText = "None"
        bsText = "None"
        target = bs.targetData()
        target.getDataFromShapeEditor()

        if target.baseMesh:
            if cmds.objExists(target.baseMesh):
                meshText = cmds.listRelatives(target.baseMesh, parent=1)[0]
        if target.node:
            if cmds.objExists(target.node):
                bsText = target.node

        self.meshLabel.setText(meshText)
        self.bsLabel.setText(bsText)

    def filterChanged(self):
        nodeText = self.filterComboBox.currentText().strip()
        if nodeText == "None":
            nodeText = ""
        targetText = self.filterLineEdit.text().strip()
        tf.treeView_filter(self.treeView, targetText, tf.SelectedItemType(3))
        tf.treeView_filter(self.treeView, nodeText, tf.SelectedItemType(2))
        tf.treeView_filter(self.treeView, nodeText, tf.SelectedItemType(1))
        print(f"filter changed: {nodeText}, {targetText}")
        # 过滤后清除选择项，避免选择项不在过滤后的列表中，导致误操作
        self.treeView.selectionModel().clearSelection()

    def loadBlendShape(self):

        blendShapeNames = []

        sel = cmds.ls(sl=1)
        for obj in sel:
            blendShapeNames.extend(get_history(obj, type="blendShape"))

        treeviewSelectedBSD = mel.eval("getShapeEditorTreeviewSelection 1")
        blendShapeNames.extend(treeviewSelectedBSD)

        if not treeviewSelectedBSD:
            lastSelectionData = bs.targetData()
            lastSelectionData.getDataFromShapeEditor()
            if lastSelectionData.node:
                blendShapeNames.append(lastSelectionData.node)

        blendShapeNames = list(dict.fromkeys(blendShapeNames))  # 保持顺序去重
        if not blendShapeNames:
            self.filterComboBox.clear()
            showMessage("No blendShape node found in the selected in scene or shapeEdit.")
            return

        self.filterComboBox.clear()
        allStr = "&".join(blendShapeNames)
        self.filterComboBox.addItem(allStr)
        self.filterComboBox.addItems(blendShapeNames)
        self.filterComboBox.setCurrentIndex(0)

    def loadTarget(self):
        # TODO  考虑添加 bsTargetGroup 支持
        # TODO  自动加载有 数值 的target，不太好使，必须选择 bs节点才行。考虑优化一下，
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
        Auto set the weight of the selected target.
        """
        target = bs.targetData()
        target.getDataFromShapeEditor()

        if target.targetIdx < 0:
            weightAttr = f"{target.node}.envelope"
        else:
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
        # auto set weight on middle mouse button click
        if self._eventAutoSetWeight(obj, event):
            return True
        # select by label
        if self._eventSelectByLabel(obj, event):
            return True
        # go to pose
        if self._eventGoToPose(obj, event):
            return True
        # delete dynamic button
        if self._deleteDynamicButton(obj, event):
            return True
        return super().eventFilter(obj, event)

    def _eventGoToPose(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                index = self.treeView.indexAt(event.pos())
                if not index.isValid():
                    return False
                try:
                    iconLabel = tf.get_treeViewItemIconLabel(self.treeView, index)
                    if not isinstance(iconLabel, QtWidgets.QLabel):
                        return False
                    label_top_left = iconLabel.mapToGlobal(QtCore.QPoint(0, 0))
                    label_rect = QtCore.QRect(label_top_left, iconLabel.size())
                    mouse_pos = event.globalPos()
                    if label_rect.contains(mouse_pos):
                        self.goToPose()
                        return True
                except Exception as e:
                    print(f"Error in _eventGoToPose: {e}")
        return False

    def _eventAutoSetWeight(self, obj, event):
        """鼠标哦中键点击事件过滤器，用于自动设置权重"""
        if obj == self.treeView.viewport():  # treeView event filter
            # auto set weight on middle mouse button click
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.MiddleButton:
                    index = self.treeView.indexAt(event.pos())
                    if index.isValid():
                        self.treeView.selectionModel().select(index, QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows)
                        self.autoSetWeight()
                    return True

    def _eventSelectByLabel(self, obj, event):
        # select base mesh or blendShape
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj == self.meshLabel:
                self.selectBaseMesh()
                return True
            if obj == self.bsLabel:
                self.selectBsNode()
                return True

    def modifyExpandButton(self):
        header = self.treeView.header()
        self.expandButton.setParent(header)
        self.expandButton.setFixedHeight(header.height() - 2)
        self.expandButton.setFixedWidth(header.height() - 2)
        self.expandButton.clicked.connect(self.treeViewExpandOrCollapse)
        self._evenUpdateExpandButtonPos()
        header.sectionResized.connect(self._evenUpdateExpandButtonPos)
        header.sectionMoved.connect(self._evenUpdateExpandButtonPos)
        header.geometriesChanged.connect(self._evenUpdateExpandButtonPos)

    def _evenUpdateExpandButtonPos(self):
        header = self.treeView.header()
        section = 0  # 你想放按钮的列号
        x = header.sectionPosition(section)
        y = 0
        h = header.height()
        # 按钮放在该列header的左侧
        self.expandButton.move(x + 2, y + (h - self.expandButton.height()) // 2)

    def goToPose(self):
        print("Go to pose clicked.")

    def selectBaseMesh(self):
        mesh = self.meshLabel.text()
        if mesh == "None":
            return
        else:
            if cmds.objExists(mesh):
                cmds.select(mesh)
            else:
                showMessage(f"{mesh} does not exist in the scene.")

    def selectBsNode(self):
        bsName = self.bsLabel.text()
        if bsName == "None":
            return
        else:
            if cmds.objExists(bsName):
                cmds.select(bsName)
            else:
                showMessage(f"{bsName} does not exist in the scene.")

    def treeViewExpandOrCollapse(self):
        # self.treeView.expandAll()
        # self.treeView.collapseAll()

        bsNodeItems = []
        isExpand = []
        model = self.treeView.model()
        for index in tf.TreeViewIterator(self.treeView):
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

    def copy_QPushbutton(self, src_btn):
        """
        Create a new QPushButton and copy common properties from src_btn.
        """
        new_btn = QtWidgets.QPushButton()
        new_btn.setText(src_btn.text())
        new_btn.setIcon(src_btn.icon())
        new_btn.setIconSize(src_btn.iconSize())
        new_btn.setEnabled(src_btn.isEnabled())
        new_btn.setCheckable(src_btn.isCheckable())
        new_btn.setChecked(src_btn.isChecked())
        new_btn.setFlat(src_btn.isFlat())
        new_btn.setFont(src_btn.font())
        new_btn.setStyleSheet(src_btn.styleSheet())
        new_btn.setMinimumSize(src_btn.minimumSize())
        new_btn.setMaximumSize(src_btn.maximumSize())
        new_btn.setSizePolicy(src_btn.sizePolicy())
        return new_btn

    def addDynamicButton(self):
        if not hasattr(self, "dynamicButtonCount"):
            self.dynamicButtonCount = 0
        if not hasattr(self, "dynamicButtonsDict"):
            self.dynamicButtonsDict = {}

        self.dynamicButtonCount += 1
        btn = self.copy_QPushbutton(self.addSetsButton)
        btn.installEventFilter(self)
        self.setsButtonWidget.layout().addWidget(btn)
        
        i = str(self.dynamicButtonCount)
        def onButtonClicked():
            showMessage(f"Dynamic Button {i} clicked.")
            
        self.dynamicButtonsDict[btn] = onButtonClicked
        btn.clicked.connect(self.dynamicButtonsDict[btn])
            
        

    def _deleteDynamicButton(self, obj, event):
        if (isinstance(obj, QtWidgets.QPushButton)) and (hasattr(self, "dynamicButtonsDict")) and (obj in self.dynamicButtonsDict):
            if (event.type() == QtCore.QEvent.MouseButtonPress) and (event.button() == QtCore.Qt.RightButton):
                self.setsButtonWidget.layout().removeWidget(obj)
                obj.deleteLater()
                del self.dynamicButtonsDict[obj]
                return True


#
if __name__ == "__main__":
    bsUI = ShapeToolsWidget()
    bsUI.show()
