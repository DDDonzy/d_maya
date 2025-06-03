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




    return shapeEditorWidgets[0]


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
