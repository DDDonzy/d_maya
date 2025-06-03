
import z_bs.uiLoader as uiLoader

from PySide2 import QtWidgets, QtCore

from z_bs.test import AttrSliderWidget

ui_path = r"E:\d_maya\z_bs\_addUI.ui"

print(ui_path)
uiBase = uiLoader.uiFileLoader(ui_path)


class ShapeToolsWidget(uiBase):
    def __init__(self):
        super().__init__()


a = ShapeToolsWidget()
a.show()
