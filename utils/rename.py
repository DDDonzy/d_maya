import re
from maya import cmds
from maya.api import OpenMaya as om
from PySide2.QtCore import Qt, QSize, QStringListModel
from PySide2.QtWidgets import QLineEdit, QCompleter
from PySide2.QtGui import QCursor

from UTILS.ui.getMayaMainWindow import getMayaMainWindow
from UTILS.create.generateUniqueName import generateUniqueName, adjustName


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
        self.setText(text)

    def _adjustText(self, text):
        if not text:
            return text
        text = re.sub(r'[^a-zA-Z0-9_#@]', '_', string=text)
        text = re.sub(r'_{2,}', '_', text)
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
    if not obj:
        obj = cmds.ls(sl=1)
    mSel = om.MSelectionList()
    [mSel.add(x) for x in obj]

    oldName = []
    mIterSel = om.MItSelectionList(mSel)
    for x in mIterSel:
        baseName = x.getDagPath().partialPathName()
        oldName.append(baseName)

    cmds.undoInfo(openChunk=True)
    mIterSel = om.MItSelectionList(mSel)
    for x in mIterSel:
        baseName = x.getDagPath().partialPathName()
        if baseName in oldName:
            name = adjustName(name=text, baseName=baseName, num=1)
            name = generateUniqueName(name)
            cmds.rename(baseName, name)
    cmds.undoInfo(closeChunk=True)


def showUI():
    rename_ui = RenameUI()
    rename_ui.show()
