from z_bs.getMayaWidget import getMayaMainWindow, getMayaWidget
import z_bs.toolWidget as toolUI


from maya import cmds
from PySide2 import QtWidgets, QtCore


from importlib import reload
reload(toolUI)


def getMayaPanelName(panelType):
    panels = cmds.getPanel(type=panelType)
    return [f"{panel}Window" for panel in panels]


def getShapeEditorWidgets():
    panelNames = getMayaPanelName("shapePanel")
    return [getMayaWidget(panelName) for panelName in panelNames]


class MoveWatcher(QtCore.QObject):
    def __init__(self, sourceWidget=None, targetWidget=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sourceWidget = sourceWidget
        self.sync_widget = targetWidget
        self.syncWidget()

    def syncWidget(self):
        if self.sync_widget is not None:
            self.sync_widget.move(self.sourceWidget.pos().x(),
                                  self.sourceWidget.pos().y()+11)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Move:
            self.syncWidget()
        return super().eventFilter(obj, event)


def openShapeEditor():

    closeShapeEditor()
    cmds.ShapeEditor()
    # cmds.refresh(f=1)

    shapeEditorWidgets = getShapeEditorWidgets()  # get all Shape Editor widgets
    if not shapeEditorWidgets:
        raise RuntimeError("Shape Editor widget not found.")

    """
    获取 maya 自带 ui 控件
    """
    shapeEditorWidget = shapeEditorWidgets[0]  # get the first Shape Editor widget
    shapeEditorWidget.hide()
    h_splitter = shapeEditorWidget.findChild(QtWidgets.QSplitter)
    v_splitter = h_splitter.findChild(QtWidgets.QSplitter)
    treeView = v_splitter.findChild(QtWidgets.QTreeView)
    shapePanelCoreWidget = v_splitter.findChild(QtWidgets.QWidget)
    header = treeView.header()
    # header.setSectionHidden(4, True)
    model = treeView.model()

    """
    创建 ui 文件的控件
    """
    toolWidget = toolUI.ShapeToolsWidget(treeView)

    """
    隐藏maya自带的FilterLineEdit, 使用ui文件的FilterLineEdit
    使用窗口变化事件，把新的LineEdit约束到旧的LineEdit上
    """
    baseLineEditWidget = shapeEditorWidget.findChild(QtWidgets.QLineEdit)
    baseLineEditWidget_parent = baseLineEditWidget.parent()
    baseLineEditWidget_parent_parent = baseLineEditWidget_parent.parent()

    lineEdit = toolWidget.filterLineEditWidget
    lineEdit.setParent(baseLineEditWidget_parent_parent)

    lineEdit.moveWatcher = MoveWatcher(sourceWidget=baseLineEditWidget_parent, targetWidget=lineEdit)
    baseLineEditWidget_parent.installEventFilter(lineEdit.moveWatcher)

    """ 隐藏旧的LineEdit"""
    sameHierarchyWidgets = baseLineEditWidget_parent_parent.children()
    _idx = sameHierarchyWidgets.index(baseLineEditWidget_parent)
    clearButtonWidget = sameHierarchyWidgets[_idx+1]

    stack = [baseLineEditWidget, clearButtonWidget]
    while stack:
        w = stack.pop()
        w.setMaximumSize(20, 0)
        stack.extend(w.findChildren(QtWidgets.QWidget))

    """重写组合maya ui 和 qt新ui"""
    filterWidget = toolWidget.filterWidget
    filterWidget.layout().addWidget(shapePanelCoreWidget)
    filterWidget.setParent(v_splitter)
    v_splitter.addWidget(filterWidget)
    v_splitter.addWidget(toolWidget)
    v_splitter.setSizes([10000, 1])

    treeViewParent = treeView.parent().parent()
    treeViewParent.layout().setContentsMargins(0, 5, 0, 0)
    
    toolWidget.treeView = v_splitter.findChild(QtWidgets.QTreeView)

    cmds.evalDeferred(lambda: shapeEditorWidget.show())
    return shapeEditorWidget, toolWidget


def closeShapeEditor():
    shapeEditorNames = getMayaPanelName("shapePanel")
    for shapeEditor in shapeEditorNames:
        if cmds.window(shapeEditor, ex=1):
            cmds.deleteUI(shapeEditor)


if __name__ == "__main__":
    widget, toolWidget = openShapeEditor()
    # from z_bs._debugUI import WidgetDebugTool
    # debug_tool = WidgetDebugTool(widget)
    # debug_tool.show()
