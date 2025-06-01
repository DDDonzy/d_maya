from pathlib import Path

from PySide2 import QtWidgets
from PySide2.QtUiTools import loadUiType

from maya import cmds
from z_bs.getMayaWidget import getMayaMainWindow, getMayaWidget



current_dir = Path(__file__).parent
ui_path = current_dir / "_addUI.ui"
ui_path = str(ui_path.resolve())
print(ui_path)
ui, base = loadUiType(r"E:\d_maya\z_bs\_addUI.ui")