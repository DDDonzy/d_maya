# =============================================================================
# 文件说明：
# 本文件用于将Qt Designer生成的.ui文件动态加载为可继承的Qt类，并支持自定义控件注册。
# 这样可以让我们在不手动转换.ui为.py的情况下，直接在Python中继承和扩展UI逻辑，
# 同时支持自定义控件（如自定义的QWidget、QPushButton等）在UI中提升使用。
#
#
# 1. 动态加载UI，方便UI设计和代码分离，UI修改后无需重新生成py文件。
# 2. 支持自定义控件注册，方便在Qt Designer中提升自定义控件并在Python中实现逻辑。
# 3. 通过递归绑定UI中的所有控件到self，便于在代码中直接访问UI控件。
# 4. 便于团队协作，UI设计与逻辑开发分离，提高开发效率。
# =============================================================================

from PySide2 import QtWidgets, QtCore
from PySide2.QtUiTools import QUiLoader

__all__ = ["uiFileLoader"]


def uiFileLoader(uiPath, customWidgets: list = []):
    """
    将UI文件转换为可继承的类。

    参数:
        uiPath (str): .ui文件路径
        customWidgets (list): 需要注册的自定义控件类列表

    返回:
        UiFileWidget (QWidget): 可继承的UI模板类
    """

    class UiFileWidget(QtWidgets.QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            # 下划线变量用于内部存储，避免外部访问
            self._ui_path = uiPath
            self._custom_widgets = customWidgets or []
            self._load_ui()

        def _load_ui(self):
            loader = QUiLoader()

            # 注册所有自定义控件，支持Qt Designer中提升的控件
            for widgetClass in self._custom_widgets:
                loader.registerCustomWidget(widgetClass)

            # 加载UI文件
            file = QtCore.QFile(self._ui_path)
            if not file.open(QtCore.QFile.ReadOnly):
                raise IOError(f"Cannot open {self._ui_path}: {file.errorString()}")

            self._ui_widget = loader.load(file, parentWidget=self)
            file.close()

            if not self._ui_widget:
                raise RuntimeError(f"Failed to load UI: {loader.errorString()}")

            # 将UI布局添加到当前窗口，边距为0
            layout = QtWidgets.QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self._ui_widget)

            # 递归绑定所有子控件到self，便于直接通过self.控件名访问
            def bindChildren(obj, parent):
                for child in obj.children():
                    if isinstance(child, QtCore.QObject) and child.objectName():
                        setattr(parent, child.objectName(), child)
                    bindChildren(child, parent)
            bindChildren(self._ui_widget, self)

    return UiFileWidget


"""
# ===================== 示例用法 =====================
if __name__ == "__main__":
    uiPath = r"E:\d_maya\z_bs\_test.ui"

    class AttrSliderWidget(QtWidgets.QPushButton):
        # 自定义控件示例：可在Qt Designer中提升为此类
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # 这里可以添加自定义逻辑
            self.setStyleSheet("QPushButton {"
                               "background-color: lightblue;"
                               "border: 1px solid gray;"
                               "padding: 5px; }"
                               "QPushButton:hover {"
                               "background-color: deepskyblue; }")

    # 创建可继承的UI类，注册自定义控件
    uiLoaderClass = uiFileLoader(uiPath=uiPath,
                                  customWidgets=[AttrSliderWidget])  # AttrSliderWidget提升为自定义控件

    # 继承并扩展UI逻辑
    class ShapeToolsWidget(uiLoaderClass):
        def __init__(self, parent=None):
            super().__init__()
            self.setWindowTitle("Custom Shape Tools")
            # 直接访问UI中的控件
            self.attrSliderWidget.setText("Hello, this is a custom widget!")

        def onButtonClicked(self):
            print("Button clicked!")

    # 实例化并显示窗口
    tool = ShapeToolsWidget()
    tool.show()
"""
