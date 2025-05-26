from PySide2 import QtWidgets, QtQuick, QtCore
from maya import cmds


def load_qml(path=r"e:\\d_maya\\qml\\ui.qml"):
    view = QtQuick.QQuickView()
    view.setSource(QtCore.QUrl.fromLocalFile(path))
    if view.status() == QtQuick.QQuickView.Error:
        for error in view.errors():
            raise RuntimeError("QML Error:", error.toString())
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
    container = QtWidgets.QWidget.createWindowContainer(view)
    container._view = view
    container.setStyleSheet("border:0px; background:transparent;")
    view.setFlags(QtCore.Qt.FramelessWindowHint)
    return container



from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtQuick, QtCore

class QmlWidget(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QmlWidget, self).__init__(parent)
        
        self.setObjectName("MyQmlDockWidget")
        if cmds.workspaceControl(f"{self.objectName()}WorkspaceControl", exists=True):
            cmds.deleteUI(f"{self.objectName()}WorkspaceControl")
        
        layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(load_qml())
        layout.setContentsMargins(0, 0, 0, 0)

widget = QmlWidget()
widget.show(dockable=True)
