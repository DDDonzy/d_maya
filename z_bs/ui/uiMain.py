from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui


from z_bs.utils.undoCallback import UndoCallback
from z_bs.utils.getMayaWidget import getMayaWidget

from z_bs.ui.resource import qrc
from z_bs.ui.uiLoader import uiFileLoader
from z_bs.ui.widgets import DragLineEdit, MirrorTableView
from z_bs.ui.logic.event import EventHandler
from z_bs.ui.logic.actions import ActionHandler

from maya import cmds
from maya.api import OpenMaya as om

current_dir = Path(__file__).parent
ui_path = current_dir / "resource" / "uiMain.ui"
ui_path = str(ui_path.resolve())

uiBase = uiFileLoader(ui_path, [DragLineEdit, MirrorTableView])


def getMayaPanelName(panelType):
    panels = cmds.getPanel(type=panelType)
    return [f"{panel}Window" for panel in panels]


def getShapeEditorWidgets():
    panelNames = getMayaPanelName("shapePanel")
    return [getMayaWidget(panelName) for panelName in panelNames]


class ShapeToolsWidget(uiBase):
    def __init__(self):
        self.callback_ids = []

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
        self.transferButton: QtWidgets.QPushButton
        self.previewButton: QtWidgets.QPushButton
        self.resetDeltaBtn: QtWidgets.QPushButton

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

        self.proximityWrapPag: QtWidgets.QScrollArea
        self.wrapPag: QtWidgets.QScrollArea
        self.treeView: QtWidgets.QTreeWidget

        self.transferLoadBtn: QtWidgets.QPushButton
        self.transferComboBox: QtWidgets.QComboBox
        self.transferMeshLineEdit: QtWidgets.QLineEdit

        self.wrapRadioButton: QtWidgets.QRadioButton
        self.proximityWrapRadioButton: QtWidgets.QRadioButton

        self.proximityModeComboBox: QtWidgets.QComboBox
        self.smoothInfluencesLineEdit: DragLineEdit
        self.smoothNormalLineEdit: DragLineEdit
        self.falloffScaleLineEdit: DragLineEdit
        self.dropoffScaleLineEdit: DragLineEdit

        self.wrapModeComboBox: QtWidgets.QComboBox
        self.wrapExclusiveBindLineEdit: DragLineEdit
        self.warpAutoWeightThresholdLineEdit: DragLineEdit
        self.wrapWeightThresholdLineEdit: DragLineEdit
        self.wrapMaxDistanceLineEdit: DragLineEdit
        self.mirrorTableView: MirrorTableView
        self.flipButton: QtWidgets.QPushButton
        self.mirrorButton: QtWidgets.QPushButton
        self.mirrorDirectionComboBox: QtWidgets.QComboBox
        self.mirrorAxisComboBox: QtWidgets.QComboBox
        self.mirrorAutoButton: QtWidgets.QPushButton

        # 初始化事件处理器
        self.event_handler = EventHandler(self)

        # 初始化动作处理器
        self.action_handler = ActionHandler(self)

        self.openShapeEditor()

        self.setupUi()

        self.action_handler.load_blendshape()

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
        self.transferButton.clicked.connect(UndoCallback(self.action_handler.transfer))
        self.previewButton.clicked.connect(UndoCallback(self.action_handler.preview))
        self.mirrorButton.clicked.connect(UndoCallback(self.action_handler.mirror_bsTarget))
        self.flipButton.clicked.connect(UndoCallback(self.action_handler.flip_bsTarget))
        self.mirrorAutoButton.clicked.connect(UndoCallback(self.action_handler.flip_bsTarget, autoMirror=True))
        self.resetDeltaBtn.clicked.connect(UndoCallback(self.action_handler.resetDelta))

        self.treeView.selectionModel().selectionChanged.connect(self.action_handler.update_object_label)

        self.modifyExpandButton()
        self.setsButtonTemplate.hide()
        self.action_handler.wrap_attrs_pag_vis()
        self.action_handler.tree_view_expand_or_collapse()

        self.treeView.viewport().installEventFilter(self)
        self.meshLabel.installEventFilter(self)
        self.bsLabel.installEventFilter(self)

        # attr line edit
        # proximity wrap
        self.smoothInfluencesLineEdit.set_range(0, 20)
        self.smoothInfluencesLineEdit.set_value_type(int)
        self.smoothInfluencesLineEdit.value = 0
        self.smoothNormalLineEdit.set_range(0, 20)
        self.smoothNormalLineEdit.set_value_type(int)
        self.smoothNormalLineEdit.value = 0
        self.falloffScaleLineEdit.set_range(0, None)
        self.falloffScaleLineEdit.value = 10
        self.dropoffScaleLineEdit.set_range(0, None)
        # wrap
        self.wrapExclusiveBindLineEdit.set_range(0, 1)
        self.wrapExclusiveBindLineEdit.set_value_type(int)
        self.wrapExclusiveBindLineEdit.value = 0
        self.warpAutoWeightThresholdLineEdit.set_range(0, 1)
        self.warpAutoWeightThresholdLineEdit.set_value_type(int)
        self.warpAutoWeightThresholdLineEdit.value = 1
        self.wrapWeightThresholdLineEdit.value = 0
        self.wrapWeightThresholdLineEdit.set_range(0, 1)
        self.wrapMaxDistanceLineEdit.value = 1
        self.wrapMaxDistanceLineEdit.set_range(0, None)

    def eventFilter(self, obj, event):
        # 使用事件处理器处理所有事件
        if self.event_handler.event_filter(obj, event):
            return True
        return super().eventFilter(obj, event)

    def closeShapeEditor(self):
        """close shape editor if it is open"""
        shapeEditorNames = getMayaPanelName("shapePanel")
        for shapeEditor in shapeEditorNames:
            if cmds.window(shapeEditor, ex=1):
                cmds.deleteUI(shapeEditor)

    def openShapeEditor(self):
        self.closeShapeEditor()
        self.action_handler.setBlendShapeManagerFilter("")
        cmds.ShapeEditor()

        shapeEditorWidgets = getShapeEditorWidgets()  # get all Shape Editor widgets
        if not shapeEditorWidgets:
            raise RuntimeError("Shape Editor widget not found.")

        """
        get maya shapeEdit widget and reparent it to this shapeEdit window
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
        mayaTreeView: QtWidgets.QTreeView = shapeEditorWidget.findChild(QtWidgets.QTreeView)
        mayaTreeView.hide()
        coreWidget: QtWidgets.QWidget = mayaTreeView.parent().parent().parent()

        """
        replace the maya tree view with our custom tree view
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
        """ add callbacks for scene events """
        shapeEditorPanel.destroyed.connect(self._parentDestroyed)
        self._register_scene_callbacks()

    def modifyExpandButton(self):
        header = self.treeView.header()
        self.expandButton.setParent(header)
        self.expandButton.setFixedHeight(header.height() - 2)
        self.expandButton.setFixedWidth(header.height() - 2)
        self.event_handler.updateExpandButtonPos()
        header.sectionResized.connect(self.event_handler.updateExpandButtonPos)
        header.sectionMoved.connect(self.event_handler.updateExpandButtonPos)
        header.geometriesChanged.connect(self.event_handler.updateExpandButtonPos)

    def _newScene(self, *args, **kwargs):
        """New scene reopen this widget"""
        ShapeToolsWidget().show()

    def _register_scene_callbacks(self):
        """Register callbacks for new and open scene events."""
        after_new_id = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, self._newScene)
        after_open_id = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterOpen, self._newScene)
        self.callback_ids.extend([after_new_id, after_open_id])

    def _remove_scene_callbacks(self):
        """Remove all registered scene callbacks."""
        if not self.callback_ids:
            return
        for callback_id in self.callback_ids:
            try:
                om.MMessage.removeCallback(callback_id)
            except RuntimeError:
                pass
        self.callback_ids = []

    @QtCore.Slot()
    def _parentDestroyed(self):
        """Get parent destroyed signal and remove callbacks."""
        self._remove_scene_callbacks()

    def closeEvent(self, event):
        """Remove callbacks and close the widget."""
        self._remove_scene_callbacks()
        super(ShapeToolsWidget, self).closeEvent(event)


#
if __name__ == "__main__":
    bsUI = ShapeToolsWidget()
    bsUI.show()
