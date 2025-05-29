import re
from UTILS.ui.getMayaMainWindow import getMayaControl
from enum import Enum
from PySide2.QtWidgets import QTreeView, QLabel
from PySide2.QtCore import QModelIndex
from typing import Iterator, Tuple




def _match_pattern(text, pattern):
    """检查文本中是否包含通配符模式（忽略大小写）"""
    pattern = pattern.replace("*", ".*")
    return bool(re.search(pattern, text, re.IGNORECASE))

class SelectedItemType(Enum):
    blendShape_node = 1
    blendShape_group = 2
    blendShape_target = 3
    blendShape_target_group = 4
    blendShape_target_inbetween = 5


class TreeViewIterator:
    """TreeView树形结构迭代器（非递归实现）"""

    def __init__(self, tree_view: QTreeView):
        self.tree_view = tree_view
        self.model = tree_view.model()

    def __iter__(self) -> Iterator[Tuple[QModelIndex, int]]:
        """迭代返回(index, indent_level)"""
        root = self.model.invisibleRootItem()
        stack = []

        for i in reversed(range(root.rowCount())):
            child_item = root.child(i)
            if child_item:
                stack.append((0, self.model.indexFromItem(child_item)))

        while stack:
            indent, index = stack.pop()
            yield indent, index  # return

            item = self.model.itemFromIndex(index)
            if item:
                for i in reversed(range(item.rowCount())):
                    child_item = item.child(i)
                    if child_item:
                        stack.append((indent + 1, self.model.indexFromItem(child_item)))


def get_item_text(tree_view: QTreeView, index: QModelIndex) -> str:
    """根据index获取widget中的文本"""
    # 尝试从widget获取文本
    widget = tree_view.indexWidget(index)
    if widget:
        widget_list = widget.children()
        if widget_list and len(widget_list) > 1:
            name_label = widget_list[1]
            if isinstance(name_label, QLabel):
                return name_label.text()

    # 如果widget中没有，尝试从item data获取
    item = tree_view.model().itemFromIndex(index)
    if item:
        return item.text() or str(item.data()) or ""

    return ""


def hide_item_by_index(tree_view: QTreeView, index: QModelIndex) -> bool:

    if index.isValid():
        tree_view.setRowHidden(index.row(), index.parent(), True)


panel = getMayaControl("shapePanel1")
tree_view = panel.findChild(QTreeView)


def filter_blendshape_items(tree_view: QTreeView, filter_str: str = "", filter_type: SelectedItemType = None):
    """
    过滤BlendShape树形结构中的项
    :param tree_view: QTreeView实例
    :param filter_str: 过滤字符串
    :param filter_type: 过滤的项目类型，如果为None则使用默认过滤逻辑
    """
    if not tree_view:
        return

    model = tree_view.model()
    if not model:
        return

    # 收集所有需要处理的项
    filterable_items = []
    parent_indices = set()  # 用于存储需要显示的父节点

    for _, index in TreeViewIterator(tree_view):
        item = model.itemFromIndex(index)
        if not item:
            continue

        item_data = item.data()
        if not item_data:
            continue

        try:
            item_type = SelectedItemType(item_data)

            # 根据filter_type参数决定处理哪些项
            if filter_type is None:
                # 默认行为：只处理 BlendShape_node 和 blendShape_group
                if item_type.value < 3:
                    filterable_items.append((index, item, item_type))
            else:
                # 按指定类型过滤：只处理指定类型的项
                if item_type == filter_type:
                    filterable_items.append((index, item, item_type))

        except (ValueError, TypeError):
            continue

    if not filter_str:
        # 清空过滤：显示所有可过滤项
        for index, _, _ in filterable_items:
            tree_view.setRowHidden(index.row(), index.parent(), False)
        return

    # 应用过滤
    filter_world_list = filter_str.split("&")
    for index, item, item_type in filterable_items:
        should_show = False

        # 根据filter_type决定过滤逻辑
        if filter_type is None:
            # 默认行为：非组类型才参与文本匹配
            if item_type != SelectedItemType.blendShape_group:
                text = get_item_text(tree_view, index)
                match = _match_pattern(text, filter_str)
                match_b = any([_match_pattern(text, f_str) for f_str in filter_world_list])
                if text and (match or match_b):
                    should_show = True
        else:
            # 指定类型过滤：直接进行文本匹配
            text = get_item_text(tree_view, index)
            match = _match_pattern(text, filter_str)
            match_b = any([_match_pattern(text, f_str) for f_str in filter_world_list])
            if text and (match or match_b):
                should_show = True

        if should_show:
            # 记录需要显示的父节点路径
            parent_index = index.parent()
            while parent_index.isValid():
                parent_indices.add(parent_index)
                parent_index = parent_index.parent()

        # 设置可见性
        tree_view.setRowHidden(index.row(), index.parent(), not should_show)

    # 显示匹配项的所有父节点
    for parent_index in parent_indices:
        tree_view.setRowHidden(parent_index.row(), parent_index.parent(), False)


# f_s = ""
# f_s2 = ""
# filter_blendshape_items(tree_view,filter_str = f_s if not f_s else "!@#$%^&*()",filter_type = SelectedItemType(2))
# filter_blendshape_items(tree_view,f_s ,SelectedItemType(1))
# filter_blendshape_items(tree_view,f_s2,SelectedItemType(3))


# # 2. 获取当前选中项的文本
# selected_indices = tree_view.selectedIndexes()
# if selected_indices:
#     selected_index = selected_indices[0]
#     item = tree_view.model().itemFromIndex(selected_index)
#     selected_type = item.data()
#     print("\nSelected Item:")
#     print("Type:", SelectedItemType(selected_type))
#     print("Text:", get_item_text(tree_view, selected_index))
