# -*- coding: utf-8 -*-

"""
模型版本对比工具 v6.0 (模块化对比版)

- [优化] ModelComparatorLogic: 核心对比逻辑模块化，将不同对比项（变换、拓扑等）拆分为独立函数，方便扩展。
- [优化] UI性能: 在逻辑层预先获取节点类型，避免UI层重复查询Maya，提升刷新性能。
- [精简] 移除脚本末尾的独立运行示例代码。
"""

import maya.cmds as cmds
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore, QtGui
import collections

# --- 全局工具实例，用于实现单例模式 ---
APP_INSTANCE = None


def get_maya_main_window():
    """获取Maya主窗口的指针"""
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_ptr), QtWidgets.QWidget)


# ==============================================================================
# 1. 逻辑层 (Action / Model)
#    - 无任何UI依赖，可独立于脚本中调用
#    - 负责数据处理和对比算法
# ==============================================================================
class ModelComparatorLogic:
    """负责模型对比的核心逻辑，不依赖任何UI。"""

    def compare_hierarchies(self, root_old, root_new):
        """
        执行层级对比，并返回一个结构化的数据字典。

        Args:
            root_old (str): 旧版本根节点的完整路径。
            root_new (str): 新版本根节点的完整路径。

        Returns:
            dict: 包含对比结果的字典，格式为 {'old': [...], 'new': [...]}。
        """
        if not all([root_old, root_new, cmds.objExists(root_old), cmds.objExists(root_new)]):
            raise ValueError("请提供有效的新旧两个版本的根节点。")

        old_tree, new_tree = self._build_comparison_recursive(root_old, root_new)
        return {"old": old_tree, "new": new_tree}

    # --- 模块化对比函数 ---
    # 每个函数只负责一项对比，返回True代表“有差异”，False代表“无差异”。

    def _is_transform_different(self, node_old, node_new):
        """对比世界矩阵。如果不同，返回True。"""
        # 使用isClose进行容差比较可能更稳健，但这里遵循原逻辑保持精确对比
        matrix_old = cmds.xform(node_old, q=True, matrix=True, worldSpace=True)
        matrix_new = cmds.xform(node_new, q=True, matrix=True, worldSpace=True)
        return matrix_old != matrix_new

    def _is_shape_structure_different(self, node_old, node_new):
        """对比shape节点的存在性。如果结构不同（一个有shape一个没有），返回True。"""
        shape_old = cmds.listRelatives(node_old, shapes=True, noIntermediate=True, fullPath=True)
        shape_new = cmds.listRelatives(node_new, shapes=True, noIntermediate=True, fullPath=True)
        return bool(shape_old) != bool(shape_new)

    def _is_topology_different(self, node_old, node_new):
        """对比mesh的拓扑（点/边/面数量）。如果拓扑不同，返回True。"""
        shape_old = cmds.listRelatives(node_old, shapes=True, noIntermediate=True, fullPath=True)
        shape_new = cmds.listRelatives(node_new, shapes=True, noIntermediate=True, fullPath=True)

        # 仅当双方都有mesh shape时才进行拓扑对比
        if shape_old and shape_new and cmds.nodeType(shape_old[0]) == "mesh" and cmds.nodeType(shape_new[0]) == "mesh":
            stats_old = (cmds.polyEvaluate(shape_old[0], vertex=True), cmds.polyEvaluate(shape_old[0], edge=True), cmds.polyEvaluate(shape_old[0], face=True))
            stats_new = (cmds.polyEvaluate(shape_new[0], vertex=True), cmds.polyEvaluate(shape_new[0], edge=True), cmds.polyEvaluate(shape_new[0], face=True))
            return stats_old != stats_new
        return False  # 如果不是两个mesh，则认为拓扑方面无差异

    # --- 对比调度器 ---
    def _get_node_differences(self, node_old, node_new):
        """
        统一调用所有对比函数，并返回一个包含所有差异原因的列表。

        Returns:
            list: 一个包含所有差异描述字符串的列表，例如 ["变换", "拓扑"]。
                  如果无差异，则返回空列表。
        """
        reasons = []
        try:
            # 在此添加或移除对比项，非常方便
            if self._is_transform_different(node_old, node_new):
                reasons.append("变换")

            if self._is_shape_structure_different(node_old, node_new):
                reasons.append("Shape结构")

            if self._is_topology_different(node_old, node_new):
                reasons.append("拓扑")

            # 以后可以轻松添加新的对比项:
            # if self._is_uv_different(node_old, node_new):
            #     reasons.append("UV")

        except Exception as e:
            print(f"对比节点 '{node_old}' 和 '{node_new}' 时出错: {e}")
            return ["Error"]

        return reasons

    # --- 核心递归与数据构建 ---
    def _build_comparison_recursive(self, old_parent_path, new_parent_path):
        """递归地构建和对比两个层级，返回节点信息列表。"""
        old_children_map = self._get_ordered_children_map(old_parent_path)
        new_children_map = self._get_ordered_children_map(new_parent_path)

        all_keys = list(old_children_map.keys())
        for key in new_children_map:
            if key not in old_children_map:
                all_keys.append(key)

        old_items_list, new_items_list = [], []

        for name in all_keys:
            is_in_old = name in old_children_map
            is_in_new = name in new_children_map
            node_data_old, node_data_new = {}, {}

            if is_in_old and is_in_new:
                old_path, new_path = old_children_map[name], new_children_map[name]
                diff_reasons = self._get_node_differences(old_path, new_path)

                status = "Modified" if diff_reasons else "Unchanged"
                details = ", ".join(diff_reasons)

                children_old, children_new = self._build_comparison_recursive(old_path, new_path)
                node_data_old = self._create_node_data(name, status, details, old_path, children_old)
                node_data_new = self._create_node_data(name, status, details, new_path, children_new)

            elif is_in_old:
                old_path = old_children_map[name]
                children_old, _ = self._build_comparison_recursive(old_path, None)
                node_data_old = self._create_node_data(name, "Deleted", "", old_path, children_old)
                node_data_new = self._create_node_data()

            elif is_in_new:
                new_path = new_children_map[name]
                _, children_new = self._build_comparison_recursive(None, new_path)
                node_data_old = self._create_node_data()
                node_data_new = self._create_node_data(name, "Added", "", new_path, children_new)

            old_items_list.append(node_data_old)
            new_items_list.append(node_data_new)

        return old_items_list, new_items_list

    def _get_ordered_children_map(self, parent_path):
        """获取子物体的有序字典 {短名称: 完整路径}。"""
        if not parent_path or not cmds.objExists(parent_path):
            return collections.OrderedDict()
        children_paths = cmds.listRelatives(parent_path, children=True, type="transform", fullPath=True) or []
        ordered_map = collections.OrderedDict()
        for path in children_paths:
            short_name = path.split("|")[-1].split(":")[-1]
            if short_name not in ordered_map:
                ordered_map[short_name] = path
        return ordered_map

    def _get_node_display_type(self, path):
        """获取节点的显示类型（用于UI图标），避免UI层重复查询。"""
        if not path or not cmds.objExists(path):
            return "default"

        shapes = cmds.listRelatives(path, shapes=True, noIntermediate=True)
        if shapes and cmds.nodeType(shapes[0]) == "mesh":
            return "mesh"
        elif cmds.nodeType(path) == "transform":
            return "transform"
        else:
            return "default"

    def _create_node_data(self, name="", status="Placeholder", details="", path="", children=None):
        """创建一个标准化的节点信息字典，包含UI所需的全部信息。"""
        return {
            "name": name,
            "status": status,
            "details": details,
            "path": path,
            "node_type": self._get_node_display_type(path),  # 预先获取节点类型
            "children": children if children is not None else [],
        }


# ==============================================================================
# 2. UI层 (View)
#    - 只负责UI的创建、布局和外观
#    - 提供外部接口用于更新UI内容和获取用户输入
# ==============================================================================
class FixedRowHeightDelegate(QtWidgets.QStyledItemDelegate):
    """一个自定义委托，用于强制设置固定的行高"""

    def __init__(self, height, parent=None):
        super(FixedRowHeightDelegate, self).__init__(parent)
        self._height = height

    def sizeHint(self, option, index):
        size = super(FixedRowHeightDelegate, self).sizeHint(option, index)
        size.setHeight(self._height)
        return size


class ModelComparatorUI(QtWidgets.QDialog):
    """只负责UI的创建和显示，不包含任何逻辑。"""

    def __init__(self, parent=get_maya_main_window()):
        super(ModelComparatorUI, self).__init__(parent)

        self.setWindowTitle("模型版本对比工具 v6.0 (模块化对比版)")
        self.setMinimumSize(900, 700)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self._setup_ui()
        self._init_icons()
        self._apply_delegates()

    def _setup_ui(self):
        """创建所有UI控件并布局。"""
        self.old_version_le = QtWidgets.QLineEdit()
        self.old_version_le.setReadOnly(True)
        self.old_version_le.setPlaceholderText("从场景中拾取旧版本根节点")
        self.get_old_btn = QtWidgets.QPushButton("<< V1 (旧)")

        self.new_version_le = QtWidgets.QLineEdit()
        self.new_version_le.setReadOnly(True)
        self.new_version_le.setPlaceholderText("从场景中拾取新版本根节点")
        self.get_new_btn = QtWidgets.QPushButton("<< V2 (新)")

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.get_old_btn)
        top_layout.addWidget(self.old_version_le)
        top_layout.addSpacing(20)
        top_layout.addWidget(self.get_new_btn)
        top_layout.addWidget(self.new_version_le)

        self.tree_old = self._create_tree_view()
        self.tree_new = self._create_tree_view()
        self.model_old = QtGui.QStandardItemModel()
        self.model_new = QtGui.QStandardItemModel()
        self.tree_old.setModel(self.model_old)
        self.tree_new.setModel(self.model_new)
        self._init_models()

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        left_widget = self._create_labeled_widget("旧版本 (V1)", self.tree_old)
        right_widget = self._create_labeled_widget("新版本 (V2)", self.tree_new)
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(right_widget)

        self.run_comparison_btn = QtWidgets.QPushButton("执行对比")
        self.run_comparison_btn.setStyleSheet("background-color: #5D9C59; padding: 5px; font-weight: bold;")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.splitter)
        main_layout.addWidget(self.run_comparison_btn)

    def _init_models(self):
        self.model_old.setHorizontalHeaderLabels(["旧版本 (V1)", "状态"])
        self.model_new.setHorizontalHeaderLabels(["新版本 (V2)", "状态"])
        # 设置列顺序和宽度
        self.tree_old.setColumnWidth(0, 220)  # 名称列宽度
        self.tree_old.setColumnWidth(1, 80)  # 状态列宽度
        self.tree_old.header().moveSection(1, 0)  # 名称列移到最左（通常已在最左）
        self.tree_new.setColumnWidth(0, 220)  # 名称列宽度
        self.tree_new.setColumnWidth(1, 80)  # 状态列宽度
        self.tree_new.header().moveSection(1, 0)  # 名称列移到最左（通常已在最左）

    def _init_icons(self):
        """初始化节点类型图标。"""
        self.icon_type_mesh = QtGui.QIcon(":/mesh.svg")
        self.icon_type_transform = QtGui.QIcon(":/transform.svg")
        self.icon_type_default = QtGui.QIcon(":/question.svg")

    def _apply_delegates(self):
        """应用自定义行高委托。"""
        delegate = FixedRowHeightDelegate(32, self)
        self.tree_old.setItemDelegate(delegate)
        self.tree_new.setItemDelegate(delegate)

    def _create_tree_view(self):
        tree = QtWidgets.QTreeView()
        tree.setAlternatingRowColors(True)
        tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tree.setIndentation(20)
        tree.setIconSize(QtCore.QSize(24, 24))
        return tree

    def _create_labeled_widget(self, title, tree_view):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(title)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(tree_view)
        return widget

    def get_root_paths(self):
        return self.old_version_le.text(), self.new_version_le.text()

    def set_root_path(self, version_key, path):
        if version_key == "old":
            self.old_version_le.setText(path)
        elif version_key == "new":
            self.new_version_le.setText(path)

    def clear_trees(self):
        self.model_old.clear()
        self.model_new.clear()
        self._init_models()  # 重新设置标题和列宽

    def populate_trees(self, comparison_data):
        self.clear_trees()
        old_root_item = self.model_old.invisibleRootItem()
        new_root_item = self.model_new.invisibleRootItem()
        self._populate_recursive(old_root_item, comparison_data.get("old", []))
        self._populate_recursive(new_root_item, comparison_data.get("new", []))
        self.tree_old.expandAll()
        self.tree_new.expandAll()

    def _populate_recursive(self, parent_item, children_data):
        for node_data in children_data:
            if node_data.get("status") == "Placeholder":
                item = self._create_placeholder_item()
                parent_item.appendRow(item)
            else:
                items = self._create_items_from_data(node_data)
                parent_item.appendRow(items)
            if node_data.get("children"):
                if node_data.get("status") == "Placeholder":
                    self._populate_recursive(item, node_data["children"])
                else:
                    self._populate_recursive(items[0], node_data["children"])

    def _create_items_from_data(self, node_data):
        """为左侧树创建两列：名称、状态。"""
        name = node_data.get("name")
        status = node_data.get("status")
        details = node_data.get("details")
        path = node_data.get("path")
        node_type = node_data.get("node_type", "default")

        item_name = QtGui.QStandardItem(name)
        item_name.setData(path, QtCore.Qt.UserRole)
        item_name.setToolTip(f"路径: {path}\n状态: {status}\n详情: {details}")

        # 设置图标和高亮
        if node_type == "mesh":
            item_name.setIcon(self.icon_type_mesh)
        elif node_type == "transform":
            item_name.setIcon(self.icon_type_transform)
        else:
            item_name.setIcon(self.icon_type_default)

        if status != "Unchanged":
            font = QtGui.QFont()
            font.setBold(True)
            font.setItalic(True)
            item_name.setFont(font)
            color_map = {"Added": QtGui.QColor(0, 150, 0), "Deleted": QtGui.QColor(200, 0, 0), "Modified": QtGui.QColor(0, 0, 220), "Error": QtGui.QColor(255, 100, 0)}
            if status in color_map:
                item_name.setForeground(QtGui.QBrush(color_map[status]))

        # 状态列
        item_status = QtGui.QStandardItem(status)
        item_status.setFlags(item_status.flags() & ~QtCore.Qt.ItemIsEditable)

        return [item_name, item_status]

    def _create_placeholder_item(self):
        item = QtGui.QStandardItem("")
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsSelectable)
        return item


# ==============================================================================
# 3. 控制器 (Controller / Event Handler)
#    - 连接UI和逻辑层
#    - 处理所有事件（按钮点击、双击、滚动等）
# ==============================================================================
class ModelComparatorController:
    """控制器，负责连接UI和逻辑，处理用户事件。"""

    def __init__(self):
        self.ui = ModelComparatorUI()
        self.logic = ModelComparatorLogic()
        self.is_syncing_scroll = False
        self._connect_signals()

    def show(self):
        self.ui.show()

    def _connect_signals(self):
        self.ui.get_old_btn.clicked.connect(lambda: self._handle_get_root("old"))
        self.ui.get_new_btn.clicked.connect(lambda: self._handle_get_root("new"))
        self.ui.run_comparison_btn.clicked.connect(self._handle_run_comparison)

        self.ui.tree_old.doubleClicked.connect(self._handle_item_double_clicked)
        self.ui.tree_new.doubleClicked.connect(self._handle_item_double_clicked)

        self.ui.tree_old.verticalScrollBar().valueChanged.connect(self._sync_scroll_new)
        self.ui.tree_new.verticalScrollBar().valueChanged.connect(self._sync_scroll_old)

    def _handle_get_root(self, version_key):
        selection = cmds.ls(selection=True)
        if not selection:
            cmds.warning("请在场景中选择一个物体。")
            return
        root_name = selection[0]
        self.ui.set_root_path(version_key, root_name)

    def _handle_run_comparison(self):
        root_old, root_new = self.ui.get_root_paths()
        try:
            comparison_data = self.logic.compare_hierarchies(root_old, root_new)
            self.ui.populate_trees(comparison_data)
        except ValueError as e:
            cmds.warning(str(e))
        except Exception as e:
            cmds.error(f"执行对比时发生未知错误: {e}")

    def _handle_item_double_clicked(self, index):
        full_path = index.data(QtCore.Qt.UserRole)
        if full_path and cmds.objExists(full_path):
            cmds.select(full_path, replace=True)
            print(f"已选中: {full_path}")
        else:
            print(f"无法选中，物体不存在: {full_path}")

    def _sync_scroll_new(self, value):
        if self.is_syncing_scroll:
            return
        self.is_syncing_scroll = True
        self.ui.tree_new.verticalScrollBar().setValue(value)
        self.is_syncing_scroll = False

    def _sync_scroll_old(self, value):
        if self.is_syncing_scroll:
            return
        self.is_syncing_scroll = True
        self.ui.tree_old.verticalScrollBar().setValue(value)
        self.is_syncing_scroll = False

    def close_ui(self):
        self.ui.close()


# --- 执行入口 ---
def show_comparator_tool():
    """
    显示模型对比工具UI。
    使用全局变量确保同一时间只有一个实例。
    """
    global APP_INSTANCE
    if APP_INSTANCE:
        APP_INSTANCE.close_ui()
    APP_INSTANCE = ModelComparatorController()
    APP_INSTANCE.show()
    return APP_INSTANCE


# 在Maya Python脚本编辑器中执行此函数以启动工具
if __name__ == "__main__":
    show_comparator_tool()
