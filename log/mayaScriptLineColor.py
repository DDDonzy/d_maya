from maya import cmds
import maya.OpenMayaUI as omui

from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget, QLineEdit


error_style_sheet = """
    QLineEdit {
        font-weight: bold;
        background-color: #ff5a5a;
        color: #373737;
        border-radius: 3px;
    }
    QLineEdit:focus {
        border-color: #5C9DED; 
    }
"""

warning_style_sheet = """
    QLineEdit {
        font-weight: bold;
        background-color: #dcce87;
        color: #373737;
        border-radius: 3px;
    }
    QLineEdit:focus {
        border-color: #5C9DED; 

    }
"""

success_style_sheet = """
    QLineEdit {
        font-weight: bold;
        background-color: #39AB6F;
        color: #373737;
        border-radius: 3px;
    }
    QLineEdit:focus {
        border-color: #5C9DED; 

    }
"""

notice_style_sheet = """"""


style_sheet_dict = {
    "NOTICE": notice_style_sheet,
    "ERROR": error_style_sheet,
    "WARNING": warning_style_sheet,
    "SUCCESS": success_style_sheet,
}


def getMayaControl(name):
    maya_control = omui.MQtUtil.findControl(name)
    return wrapInstance(int(maya_control), QWidget) if maya_control else None


commandLine_list = []
lineEdit_list = []

for x in cmds.lsUI(type="commandLine"):
    qt_commandLine = getMayaControl(x)
    commandLine_list.append(qt_commandLine)
    qt_lineEdit: list[QLineEdit] = qt_commandLine.findChildren(QLineEdit)
    for lineEdit in qt_lineEdit:
        if lineEdit.isEnabled():
            lineEdit_list.append(lineEdit)
            break


def resetLineEditStyleSheet(lineEdit):
    lineEdit.setStyleSheet("")
    lineEdit.textChanged.disconnect()


def updateLineEditStyleSheet(level):
    for x in lineEdit_list:
        x.setStyleSheet(style_sheet_dict[level])
        x.textChanged.connect(lambda: resetLineEditStyleSheet(x))


class ScriptEditorStyler:
    def __init__(self):
        self._current_level = None
        self._job_scheduled = False

        self._commandLine_list = []
        self._lineEdit_list = []

        self._getLineEditControls()

    def _getMayaControl(self, name):
        maya_control = omui.MQtUtil.findControl(name)
        return wrapInstance(int(maya_control), QWidget) if maya_control else None

    def _getLineEditControls(self):
        for x in cmds.lsUI(type="commandLine"):
            qt_commandLine = self._getMayaControl(x)
            self._commandLine_list.append(qt_commandLine)
            qt_lineEdit: list[QLineEdit] = qt_commandLine.findChildren(QLineEdit)
            for lineEdit in qt_lineEdit:
                if lineEdit.isEnabled():
                    self._lineEdit_list.append(lineEdit)
                    break

    def _resetLineEditStyleSheet(self, lineEdit):
        lineEdit.setStyleSheet("")
        lineEdit.textChanged.disconnect()
    
    def updateLineEditStyleSheet(self, level):
        if level not in ("SUCCESS", "WARNING", "ERROR"):
            return
        self._current_level = level
        for x in self._lineEdit_list:
            x.setStyleSheet(style_sheet_dict[level])
            x.textChanged.connect(lambda: self._resetLineEditStyleSheet(x))

    def _updateLineEditStyleSheet(self):
        if not self._current_level:
            self._job_scheduled = False
            return

        self._job_scheduled = False
        self.updateLineEditStyleSheet(self._current_level)
        self._current_level = None
