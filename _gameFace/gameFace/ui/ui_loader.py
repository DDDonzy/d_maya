from gameFace.fn.getMayaMainWindow import getMayaMainWindow

from maya import cmds


def build_ui_2022(path):
    from PySide2.QtUiTools import loadUiType
    ui, base = loadUiType(path)

    class MainWindow(base, ui):
        def __init__(self):
            super(MainWindow, self).__init__(getMayaMainWindow())
            self.setupUi(self)

    return MainWindow()


def build_ui_2019(path):
    from PySide2.QtUiTools import QUiLoader
    return QUiLoader().load(path, getMayaMainWindow())


def build_ui(path):
    maya_version = cmds.about(api=1)
    if maya_version >= 20220000:
        return build_ui_2022(path)
    else:
        return build_ui_2019(path)
