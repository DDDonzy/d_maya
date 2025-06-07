from PySide2 import QtWidgets, QtCore
import z_bs.ui.logic.treeViewFunction as tf

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from z_bs.ui.uiMain import ShapeToolsWidget


class EventHandler:
    """事件处理器类，用于处理UI的各种事件"""

    def __init__(self, ui):
        self.ui: ShapeToolsWidget = ui

    def handle_go_to_pose(self, obj, event):
        """处理双击图标跳转到pose的事件"""
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() == QtCore.Qt.LeftButton:
                index = self.ui.treeView.indexAt(event.pos())
                if not index.isValid():
                    return False
                try:
                    iconLabel = tf.get_treeViewItemIconLabel(self.ui.treeView, index)
                    if not isinstance(iconLabel, QtWidgets.QLabel):
                        return False
                    label_top_left = iconLabel.mapToGlobal(QtCore.QPoint(0, 0))
                    label_rect = QtCore.QRect(label_top_left, iconLabel.size())
                    mouse_pos = event.globalPos()
                    if label_rect.contains(mouse_pos):
                        self.ui.action_handler.go_to_pose()
                        return True
                except Exception as e:
                    print(f"Error in handle_go_to_pose: {e}")
        return False

    def handle_auto_set_weight(self, obj, event):
        """处理鼠标中键点击自动设置权重的事件"""
        if obj == self.ui.treeView.viewport():  # treeView event filter
            # auto set weight on middle mouse button click
            if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
                if event.button() == QtCore.Qt.MiddleButton:
                    index = self.ui.treeView.indexAt(event.pos())
                    if index.isValid():
                        self.ui.treeView.selectionModel().select(
                            index,
                            QtCore.QItemSelectionModel.ClearAndSelect | QtCore.QItemSelectionModel.Rows
                        )
                        self.ui.action_handler.auto_set_weight()
                    return True
        return False

    def handle_select_by_label(self, obj, event):
        """处理点击标签选择对象的事件"""
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if obj == self.ui.meshLabel:
                self.ui.action_handler.select_base_mesh()
                return True
            if obj == self.ui.bsLabel:
                self.ui.action_handler.select_bs_node()
                return True
        return False

    def handle_delete_dynamic_button(self, obj, event):
        """处理右键删除动态按钮的事件"""
        if (isinstance(obj, QtWidgets.QPushButton) and
            hasattr(self.ui, "dynamicButtonsDict") and
                obj in self.ui.dynamicButtonsDict):
            if (event.type() == QtCore.QEvent.MouseButtonPress and
                    event.button() == QtCore.Qt.RightButton):
                self.ui.action_handler.delete_dynamic_button(obj)
                return True
        return False

    def updateExpandButtonPos(self):
        header = self.ui.treeView.header()
        section = 0  # 你想放按钮的列号
        x = header.sectionPosition(section)
        y = 0
        h = header.height()
        # 按钮放在该列header的左侧
        self.ui.expandButton.move(x + 2, y + (h - self.ui.expandButton.height()) // 2)

    def event_filter(self, obj, event):
        """主事件过滤器，统一处理所有事件"""
        # auto set weight on middle mouse button click
        if self.handle_auto_set_weight(obj, event):
            return True
        # select by label
        if self.handle_select_by_label(obj, event):
            return True
        # go to pose
        if self.handle_go_to_pose(obj, event):
            return True
        # delete dynamic button
        if self.handle_delete_dynamic_button(obj, event):
            return True
        return False
