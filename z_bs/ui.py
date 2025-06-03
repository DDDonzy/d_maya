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

    treeView = shapeEditorWidget.findChild(QtWidgets.QTreeView)
    treeView_parent = treeView.parent()
    coreWidget: QtWidgets.QWidget = treeView.parent().parent().parent()

    # header = treeView.header()
    # # header.setSectionHidden(4, True)
    # model = treeView.model()

    """
    创建 ui 文件的控件
    """
    toolWidget = toolUI.ShapeToolsWidget(treeView)

    # """重写组合maya ui 和 qt新ui"""
    toolWidget.addonWidget.layout().addWidget(treeView)
    toolWidget.addonWidget.setParent(treeView_parent)
    v_splitter = treeView_parent.parent().parent().parent()
    toolWidget.addonWidget.setParent(v_splitter)
    toolWidget.setParent(v_splitter)
    


    treeView = shapeEditorWidget.findChild(QtWidgets.QTreeView)
    reParentList = coreWidget.children()
    reParentDone = []
    for item in reParentList:
        if not item.findChild(QtWidgets.QTreeView):
            if isinstance(item, QtWidgets.QPushButton):
                item.setParent(toolWidget.bsAddWidget)
                toolWidget.bsAddWidget.layout().addWidget(item)
                reParentDone.append(item)
    for x in reParentDone[3:]:
        x.hide()
    coreWidget.hide()
    v_splitter.setSizes([1000, 1000,1])
    

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
