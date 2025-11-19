from maya import cmds, utils
import maya.OpenMayaUI as omui

from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget, QLineEdit


error_style_sheet = """
    QLineEdit {
        font-weight: bold;
        background-color: #ff5a5a;
        color: #373737;

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

    }
    QLineEdit:focus {
        border-color: #5C9DED; 

    }
"""


style_sheet_dict = {
    "ERROR": error_style_sheet,
    "WARNING": warning_style_sheet,
    "SUCCESS": success_style_sheet,
}


class ScriptEditorStyler:
    def __init__(self):
        self._job_scheduled = False

        self._commandLine_list = []
        self._lineEdit_list = []

        self._jobs = []
        self._level = "INFO"

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

    def _reset(self, lineEdit):
        lineEdit.setStyleSheet("")
        lineEdit.textChanged.disconnect()

    def update(self, level):
        self._level = level

        if not self._job_scheduled:
            self._job_scheduled = True
            utils.executeDeferred(self._update)

    def _update(self):
        for x in self._lineEdit_list:
            x.setStyleSheet(style_sheet_dict.get(self._level, ""))
            x.textChanged.connect(lambda: self._reset(x))
        self._job_scheduled = False
        self._level = "INFO"
