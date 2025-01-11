import re
import maya.OpenMayaUI as omui
from maya import cmds
from maya.api import OpenMaya as om
from shiboken2 import wrapInstance
from PySide2.QtCore import Qt, QSize, QStringListModel
from PySide2.QtWidgets import QLineEdit, QWidget, QCompleter
from PySide2.QtGui import QCursor
from utils.generateUniqueName import generateUniqueName


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)


class InputDialog(QLineEdit):
    _suffix = ["", "_CTL", "_GRP", "_SDK", "_OFFSET"]

    def __init__(self):
        # user data
        self.updated_suffix = InputDialog._suffix
        self.modelNeedUpdate = True
        # ui
        super().__init__(get_maya_main_window())
        self.setFixedSize(QSize(300, 30))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.move(QCursor().pos())

        # QLineEdit
        self.setPlaceholderText("Input name.     '@'=self.     '#'=num.")
        self.setFocus()

        # textCompleter
        self.model = QStringListModel(self.updated_suffix)
        self.model.setStringList(InputDialog._suffix)
        self.textCompleter = QCompleter(self)
        self.textCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        self.textCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.textCompleter.setMaxVisibleItems(7)
        self.textCompleter.setModel(self.model)
        self.setCompleter(self.textCompleter)

        # connect function
        self.textChanged.connect(self.textChange)
        self.textCompleter.highlighted.connect(self.change)
        self.returnPressed.connect(self.run)

    def change(self, text):
        self.modelNeedUpdate = False

    def textChange(self, text):
        text = self.adjust_variable_name(text)
        if self.modelNeedUpdate:
            self.updated_suffix = [self.adjust_variable_name(f"{text}{x}") for x in InputDialog._suffix]
            self.model.setStringList(self.updated_suffix)
        self.modelNeedUpdate = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.deleteLater()
        else:
            super().keyPressEvent(event)

    def run(self):
        text = self.text()
        print(text)
        cmds.undoInfo(openChunk=True)
        mSel = om.MGlobal.getActiveSelectionList()
        mIterSel = om.MItSelectionList(mSel)
        for x in mIterSel:
            baseName = x.getDagPath().partialPathName()
            text = re.sub(r"\@", baseName, text)
            text = re.sub(r"\#", "1_", text)
            text = self.adjust_variable_name(text)
            if text[-1] == "_":
                text = text[0:-1]
            name = generateUniqueName(text)
            cmds.rename(baseName, name)
        cmds.undoInfo(closeChunk=True)
        self.deleteLater()

    def adjust_variable_name(self, name):
        if not name:
            return name
        name = re.sub(r'[^a-zA-Z0-9_#@]', '_', name)
        name = re.sub(r'_{2,}', '_', name)
        if name[0].isdigit():
            name = "_" + name
        return name


window = InputDialog()
window.show()
