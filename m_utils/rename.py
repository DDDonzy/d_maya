from email.mime import base
from functools import partial
import re

from maya.api import OpenMaya as om
from PySide2.QtCore import Qt, QSize, QStringListModel
from PySide2.QtWidgets import QLineEdit, QCompleter
from PySide2.QtGui import QCursor
from m_utils.apiundo import commit

from m_utils.ui.getMayaMainWindow import getMayaMainWindow
from m_utils.create.generateUniqueName import generateUniqueName, adjustName


class RenameUI(QLineEdit):
    _suffix = ["", "_CTL", "_GRP", "_SDK", "_OFFSET"]

    def __init__(self):
        # user data
        self.updated_suffix = RenameUI._suffix
        self.modelNeedUpdate = True
        # ui
        super().__init__(getMayaMainWindow())
        self.setFixedSize(QSize(300, 30))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.move(QCursor().pos())

        # QLineEdit
        self.setPlaceholderText("Input name.     '@'=self.     '#'=num.")
        self.setFocus()

        # textCompleter
        self.model = QStringListModel(self.updated_suffix)
        self.model.setStringList(RenameUI._suffix)
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

        # event
        self.installEventFilter(self)

    def change(self, text):
        self.modelNeedUpdate = False

    def textChange(self, text):
        text = self._adjustText(text)
        if self.modelNeedUpdate:
            self.updated_suffix = [self._adjustText(f"{text}{x}") for x in RenameUI._suffix]
            self.model.setStringList(self.updated_suffix)
        self.modelNeedUpdate = True
        cursorPosition = self.cursorPosition()
        self.setText(text)
        self.setCursorPosition(cursorPosition)

    def _adjustText(self, text):
        text = re.sub(r"[`·]", "", text)
        text = re.sub(r"[^a-zA-Z0-9_#@]", "_", string=text)
        if not text:
            return text
        if text[0].isdigit():
            text = "_" + text
        return text

    def run(self):
        rename(self.text())
        self.deleteLater()

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonPress:
            inQLineEdit = self.rect().contains(event.pos())
            if not inQLineEdit:
                self.deleteLater()
                return True
        elif event.type() == event.KeyPress and event.key() == Qt.Key_Escape:
            self.deleteLater()
            return True
        return False


def rename(text: str, obj: list = None):
    # if no obj input, use current selection and excluding shapes

    mSel = om.MGlobal.getActiveSelectionList()
    mIterSel = om.MItSelectionList(mSel)

    _doit = []
    _undo = []

    for x in mIterSel:
        mObj: om.MObject = x.getDependNode()
        if mObj.hasFn(om.MFn.kShape):
            continue

        mDep: om.MFnDependencyNode = om.MFnDependencyNode(mObj)
        baseName = mDep.uniqueName()
        if "|" in baseName:
            baseName = baseName.split("|")[-1]

        _undo.append(lambda baseName=baseName, dependencyNode=mDep: dependencyNode.setName(baseName))
        _doit.append(lambda name=text, baseName=baseName, dependencyNode=mDep: dependencyNode.setName(generateUniqueName(adjustName(name=name, baseName=baseName))))

    def doit():
        for f in _doit:
            f()

    def undo():
        for f in _undo:
            f()

    doit()
    commit(undo, doit)


def showUI():
    rename_ui = RenameUI()
    rename_ui.show()


if __name__ == "__main__":
    showUI()
