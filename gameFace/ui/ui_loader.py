from maya import cmds
from UTILS.ui.getMayaMainWindow import getMayaMainWindow


def build_ui_2022(path):
    from PySide2.QtUiTools import loadUiType
    ui, base = loadUiType(path)

    class MainWindow(base, ui):
        def __init__(self):
            super().__init__(getMayaMainWindow())
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


