from pathlib import Path
from PySide2 import QtWidgets, QtCore, QtGui  # noqa: F401

from maya import cmds  # noqa: F401
from maya.api import OpenMaya as om  # noqa: F401

from z_bs.ui.uiLoader import uiFileLoader


current_dir = Path(__file__).parent
ui_path = current_dir / "src" / "uiMain.ui"
ui_path = str(ui_path.resolve())

uiBase = uiFileLoader(ui_path, [])


class Speed_UI(uiBase):
    def __init__(self):
        self.callback_ids = []

        super().__init__()

        self.setupUi()

    def setupUi(self):
        pass


#
if __name__ == "__main__":
    bsUI = Speed_UI()
    bsUI.show()
