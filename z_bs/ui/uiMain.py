from z_bs.ui.resource import qrc
from maya import cmds
from z_bs.utils.getMayaWidget import getMayaWidget

import z_bs.ui.uiLoader as uiLoader
from z_bs.ui.logic.event import EventHandler
from z_bs.ui.logic.actions import ActionHandler

from PySide2 import QtWidgets, QtCore

from pathlib import Path
from z_bs.utils.undoCallback import UndoCallback
from z_bs.ui.widgets.dragLineEdit import DragLineEdit


current_dir = Path(__file__).parent
ui_path = current_dir / "resource" / "uiMain.ui"
ui_path = str(ui_path.resolve())

uiBase = uiLoader.uiFileLoader(ui_path,[DragLineEdit])


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
        self.setsButtonTemplate: QtWidgets.QPushButton
        self.copyDeltaBtn: QtWidgets.QPushButton
        self.pastedDeltaBtn: QtWidgets.QPushButton

        self.transferLoadBtn: QtWidgets.QPushButton
        self.transferComboBox: QtWidgets.QComboBox
        self.transferLineEdit: QtWidgets.QLineEdit

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

        # 初始化事件处理器
        self.event_handler = EventHandler(self)

        # 初始化动作处理器
        self.action_handler = ActionHandler(self)
        
        
        self.openShapeEditor()
        self.setupUi()
        

    def setupUi(self):

        #
        self.loadTargetButton.clicked.connect(self.action_handler.load_target)
        self.loadBsButton.clicked.connect(self.action_handler.load_blendshape)
        self.filterLineEdit.textChanged.connect(self.action_handler.filter_changed)
        self.filterComboBox.currentTextChanged.connect(self.action_handler.filter_changed)
        self.addSculptButton.clicked.connect(UndoCallback(self.action_handler.add_sculpt))
        self.proximityWrapRadioButton.toggled.connect(self.action_handler.wrap_attrs_pag_vis)
        self.addSetsButton.clicked.connect(self.action_handler.add_dynamic_button)
        self.copyDeltaBtn.clicked.connect(self.action_handler.copy_delta_cmd)
        self.pastedDeltaBtn.clicked.connect(UndoCallback(self.action_handler.pasted_delta_cmd))
        self.expandButton.clicked.connect(self.action_handler.tree_view_expand_or_collapse)
        self.transferLoadBtn.clicked.connect(self.action_handler.transfer_load)

        self.treeView.selectionModel().selectionChanged.connect(self.action_handler.update_object_label)

        self.modifyExpandButton()
        self.setsButtonTemplate.hide()
        self.action_handler.wrap_attrs_pag_vis()
        self.action_handler.tree_view_expand_or_collapse()
        

        self.treeView.viewport().installEventFilter(self)
        self.meshLabel.installEventFilter(self)
        self.bsLabel.installEventFilter(self)

    def closeShapeEditor(self):
        """ close shape editor if it is open """
        shapeEditorNames = getMayaPanelName("shapePanel")
        for shapeEditor in shapeEditorNames:
            if cmds.window(shapeEditor, ex=1):
                cmds.deleteUI(shapeEditor)

    def openShapeEditor(self):
        self.closeShapeEditor()
        self.action_handler.setBlendShapeManagerFilter("") 
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
        mayaTreeView:QtWidgets.QTreeView = shapeEditorWidget.findChild(QtWidgets.QTreeView)
        mayaTreeView.hide()
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
        self.treeView.show()

    def eventFilter(self, obj, event):
        # 使用事件处理器处理所有事件
        if self.event_handler.event_filter(obj, event):
            return True
        return super().eventFilter(obj, event)

    def modifyExpandButton(self):
        header = self.treeView.header()
        self.expandButton.setParent(header)
        self.expandButton.setFixedHeight(header.height() - 2)
        self.expandButton.setFixedWidth(header.height() - 2)
        self.event_handler.updateExpandButtonPos()
        header.sectionResized.connect(self.event_handler.updateExpandButtonPos)
        header.sectionMoved.connect(self.event_handler.updateExpandButtonPos)
        header.geometriesChanged.connect(self.event_handler.updateExpandButtonPos)


#
if __name__ == "__main__":
    bsUI = ShapeToolsWidget()
    bsUI.show()
