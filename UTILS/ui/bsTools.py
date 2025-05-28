import maya.OpenMayaUI as omui
import shiboken2
from PySide2 import QtWidgets,QtGui
from maya import cmds
from PySide2.QtUiTools import loadUiType

ui, base = loadUiType(r"T:\d_maya\UTILS\ui\untitled.ui")


class bsAddonWidget(base, ui):
    def __init__(self):
        super(bsAddonWidget, self).__init__(getMayaMainWindow())
        self.setupUi(self)


def getMayaMainWindow():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QtWidgets.QWidget) if main_window_ptr else None


def getMayaControl(name):
    maya_control = omui.MQtUtil.findControl(name)
    return shiboken2.wrapInstance(int(maya_control), QtWidgets.QWidget) if maya_control else None


class bsAddonWidget(base, ui):
    def __init__(self):
        super(bsAddonWidget, self).__init__(getMayaMainWindow())
        self.setupUi(self)


if __name__ == "__main__":
    cmds.ShapeEditor()
    cmds.refresh(f=1)
    bsPanelName = cmds.getPanel(type="shapePanel")

    bsWinWidgetList = []
    for panel in bsPanelName:
        result = getMayaControl(f"{panel}Window")
        if result:
            bsWinWidgetList.append(result)

    bs_win: QtWidgets.QWidget = bsWinWidgetList[0]
    h_splitter: QtWidgets.QSplitter = bs_win.findChild(QtWidgets.QSplitter)
    v_splitter = h_splitter.findChild(QtWidgets.QSplitter)
    addWidget = bsAddonWidget()
    v_splitter.addWidget(addWidget)
    treeView:QtWidgets.QTreeView = v_splitter.findChild(QtWidgets.QTreeView)
    header:QtWidgets.QHeaderView = treeView.header()
    # header.setSectionHidden(3,True)
    header.setSectionHidden(4,True)
    
    model = treeView.model()
    
    if model:
        for row in range(model.rowCount()):
            item = model.item(row).setHidden(True)
    
    treeView.children()
    treeView.findChild()
    
    for x in dir(treeView):
        print(x)