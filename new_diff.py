# -*- coding: utf-8 -*-

"""
模型版本对比工具 v7.0 (OpenMaya 优化版)

- [优化] 核心逻辑: 完全重写对比逻辑以使用 maya.api.OpenMaya。
           - 使用用户提供的 IterHierarchy 类进行层级遍历。
           - 使用用户提供的 NodeData 类存储节点信息，取代了字典。
- [优化] 性能: 采用两阶段方法：
           1. 使用 OpenMaya 快速构建完整的节点树。
           2. 递归地比较和重组树以进行差异分析。
           这大大减少了对 `maya.cmds` 的调用，显著提升了在大型层级上的性能。
- [重构] 将核心逻辑封装在新的 ModelComparatorLogicOM 类中。
- [适配] UI 和控制器层已更新，以与新的 NodeData 结构无缝协作。
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui  # type: ignore
from PySide2 import QtWidgets, QtCore, QtGui
from typing import List, Tuple, Optional, Dict, OrderedDict  # noqa: F401

# --- 全局工具实例，用于实现单例模式 ---
APP_INSTANCE = None


def get_maya_main_window():
    """获取Maya主窗口的指针"""
    main_win_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_ptr), QtWidgets.QWidget)


# ==============================================================================
# 1. 提供的类 (Provided Classes)
#    - 这是用户要求集成的数据结构和迭代器。
# ==============================================================================


class IterHierarchy:
    def __init__(self, rootDag, shape=True):
        if isinstance(rootDag, om.MDagPath):
            self.root_node = rootDag
        elif isinstance(rootDag, str):
            self.root_node = om.MSelectionList().add(rootDag).getDagPath(0)
        else:
            raise Exception("Invalid root node, must be a string or MDagPath.")
        self.shape = shape
        self._reset()

    def _reset(self):
        self.iterList = [self.root_node]

    def __iter__(self):
        self._reset()
        return self

    def __next__(self) -> Tuple[str, om.MDagPath]:
        if not self.iterList:
            raise StopIteration
        current_dag = self.iterList.pop()
        children = []
        for x in range(current_dag.childCount()):
            mObj = current_dag.child(x)
            if (not mObj.hasFn(om.MFn.kTransform)) and (not self.shape):
                continue
            children.append(om.MDagPath.getAPathTo(mObj))
        self.iterList.extend(reversed(children))
        name: str = current_dag.partialPathName()
        dag: om.MDagPath = current_dag
        return name, dag


class NodeData:
    """一个数据类，用于存储关于单个节点的所有相关信息。"""

    def __init__(self, dag: om.MDagPath):
        self.name: str = dag.partialPathName() if dag else ""
        self.dag: Optional[om.MDagPath] = dag
        self.children: List["NodeData"] = []
        self.status: str = "Unchanged"  # "Unchanged", "Modified", "Added", "Deleted", "Placeholder"
        self.details: str = ""
        self.node_type: str = "default"  # "mesh", "transform", "default"
        if dag:
            self._set_node_type()

    def _set_node_type(self):
        """使用OpenMaya确定节点类型以供UI显示。"""
        try:
            if self.dag.hasFn(om.MFn.kMesh):
                self.node_type = "mesh"
                return

            # 检查是否有mesh shape
            if self.dag.hasFn(om.MFn.kTransform) and self.dag.numberOfShapesDirectlyBelow() > 0:
                for i in range(self.dag.numberOfShapesDirectlyBelow()):
                    shape_dag = om.MDagPath(self.dag)
                    shape_dag.extendToShape(i)
                    if shape_dag.hasFn(om.MFn.kMesh):
                        self.node_type = "mesh"
                        return

            if self.dag.hasFn(om.MFn.kTransform):
                self.node_type = "transform"

        except Exception:
            self.node_type = "default"


# ==============================================================================
# 2. 逻辑层 (Action / Model) - OpenMaya版本
#    - 使用OpenMaya API进行高性能的对比。
# ==============================================================================
class ModelComparatorLogicOM:
    """负责模型对比的核心逻辑，使用OpenMaya API以实现高性能。"""

    # --- 阶段 1: 构建层级树 ---

    def _build_tree_from_root(self, root_path_str: str) -> Optional[NodeData]:
        """
        [最终版] 采纳用户建议，使用更优雅的 for 循环。
        通过 next() 先处理根节点，再用 for 循环处理所有后代节点。
        """
        if not root_path_str or not cmds.objExists(root_path_str):
            return None

        iterator = IterHierarchy(root_path_str,False)

        # 1. 首先，安全地获取迭代器的第一个元素。
        # 我们知道它一定是根节点。
        _root_name, root_dag = next(iterator)

        root_node = NodeData(root_dag)
        node_map = {root_dag.fullPathName(): root_node}

        # 3. 现在，直接使用 for 循环遍历迭代器中“剩余”的所有后代节点。
        # 循环体逻辑非常纯粹，只处理子节点。
        for name, dag in iterator:
            node = NodeData(dag)
            node_map[dag.fullPathName()] = node

            # 查找并链接到父节点
            parent_dag = om.MDagPath(dag)
            parent_dag.pop()
            parent_path_str = parent_dag.fullPathName()

            if parent_path_str in node_map:
                node_map[parent_path_str].children.append(node)
        return root_node


    # --- 阶段 2: 对比和重组 ---

    def compare_hierarchies(self, root_old_str: str, root_new_str: str) -> Dict:
        """执行层级对比，并返回一个包含NodeData对象的结构化字典。"""
        if not all([root_old_str, root_new_str, cmds.objExists(root_old_str), cmds.objExists(root_new_str)]):
            raise ValueError("请提供有效的新旧两个版本的根节点。")

        old_root_node = self._build_tree_from_root(root_old_str)
        new_root_node = self._build_tree_from_root(root_new_str)

        if not old_root_node or not new_root_node:
            raise ValueError("无法为提供的根节点构建层级树。")

        # 对比根节点本身
        diff_reasons = self._get_node_differences(old_root_node, new_root_node)
        if diff_reasons:
            old_root_node.status = new_root_node.status = "Modified"
            old_root_node.details = new_root_node.details = ", ".join(diff_reasons)

        # 递归地对比和重组子节点
        self._compare_and_restructure_children(old_root_node, new_root_node)

        # UI期望得到一个列表
        
        return {"old": [old_root_node], "new": [new_root_node]}

    def _compare_and_restructure_children(self, parent_old: NodeData, parent_new: NodeData):
        """递归地对比子节点，并用占位符重组列表以保持对齐。"""
        old_children_map = {c.name: c for c in parent_old.children}
        new_children_map = {c.name: c for c in parent_new.children}
        all_names = sorted(list(set(old_children_map.keys()) | set(new_children_map.keys())))

        structured_old_children, structured_new_children = [], []

        for name in all_names:
            child_old = old_children_map.get(name)
            child_new = new_children_map.get(name)

            if child_old and child_new:
                diff_reasons = self._get_node_differences(child_old, child_new)
                if diff_reasons:
                    child_old.status = child_new.status = "Modified"
                    child_old.details = child_new.details = ", ".join(diff_reasons)
                else:
                    child_old.status = child_new.status = "Unchanged"

                self._compare_and_restructure_children(child_old, child_new)
                structured_old_children.append(child_old)
                structured_new_children.append(child_new)

            elif child_old:  # 在旧版中被删除
                self._set_status_recursively(child_old, "Deleted")
                structured_old_children.append(child_old)
                structured_new_children.append(self._create_placeholder_for(child_old))

            elif child_new:  # 在新版中添加
                self._set_status_recursively(child_new, "Added")
                structured_new_children.append(child_new)
                structured_old_children.append(self._create_placeholder_for(child_new))

        parent_old.children = structured_old_children
        parent_new.children = structured_new_children

    def _set_status_recursively(self, node: NodeData, status: str):
        """递归地为一个节点及其所有子节点设置状态。"""
        node.status = status
        for child in node.children:
            self._set_status_recursively(child, status)

    def _create_placeholder_for(self, node: NodeData) -> NodeData:
        """为添加/删除的节点创建一个匹配的占位符节点。"""
        placeholder = NodeData(None)
        placeholder.status = "Placeholder"
        placeholder.children = [self._create_placeholder_for(child) for child in node.children]
        return placeholder

    # --- 模块化对比函数 (OpenMaya 版本) ---

    def _get_node_differences(self, node_old: NodeData, node_new: NodeData) -> list:
        """统一调用所有对比函数，并返回一个包含所有差异原因的列表。"""
        reasons = []
        try:
            if self._is_transform_different(node_old.dag, node_new.dag):
                reasons.append("变换")
            if self._is_shape_structure_different(node_old.dag, node_new.dag):
                reasons.append("Shape结构")
            if self._is_topology_different(node_old, node_new):
                reasons.append("拓扑")
        except Exception as e:
            print(f"对比节点 '{node_old.name}' 和 '{node_new.name}' 时出错: {e}")
            return ["Error"]
        return reasons

    def _is_transform_different(self, dag_old: om.MDagPath, dag_new: om.MDagPath) -> bool:
        """对比世界矩阵。如果不同，返回True。"""
        old_matrix = om.MFnTransform(dag_old).transformation().asMatrix()
        new_matrix = om.MFnTransform(dag_new).transformation().asMatrix()
        return not old_matrix.isEquivalent(new_matrix, 1e-6)

    def _is_shape_structure_different(self, dag_old: om.MDagPath, dag_new: om.MDagPath) -> bool:
        """对比shape节点的存在性。如果结构不同，返回True。"""
        return dag_old.numberOfShapesDirectlyBelow() != dag_new.numberOfShapesDirectlyBelow()

    def _is_topology_different(self, node_old: NodeData, node_new: NodeData) -> bool:
        """对比mesh的拓扑（点/边/面数量）。如果拓扑不同，返回True。"""
        if node_old.node_type != "mesh" or node_new.node_type != "mesh":
            return False

        try:
            mesh_dag_old = om.MDagPath(node_old.dag)
            mesh_dag_old.extendToShape()
            mfn_mesh_old = om.MFnMesh(mesh_dag_old)
            stats_old = (mfn_mesh_old.numVertices, mfn_mesh_old.numEdges, mfn_mesh_old.numPolygons)

            mesh_dag_new = om.MDagPath(node_new.dag)
            mesh_dag_new.extendToShape()
            mfn_mesh_new = om.MFnMesh(mesh_dag_new)
            stats_new = (mfn_mesh_new.numVertices, mfn_mesh_new.numEdges, mfn_mesh_new.numPolygons)

            return stats_old != stats_new
        except Exception:
            # 如果无法获取网格，则认为它们没有差异，以避免误报
            return False


# ==============================================================================
# 3. UI层 (View) - 已适配NodeData
#    - 只负责UI的创建、布局和外观
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
    """UI类，已更新为使用NodeData对象而不是字典。"""

    def __init__(self, parent=get_maya_main_window()):
        super(ModelComparatorUI, self).__init__(parent)
        self.setWindowTitle("模型版本对比工具 v7.0 (OpenMaya 优化版)")
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
        self.tree_old.setColumnWidth(0, 220)
        self.tree_old.setColumnWidth(1, 80)
        self.tree_new.setColumnWidth(0, 220)
        self.tree_new.setColumnWidth(1, 80)

    def _init_icons(self):
        self.icon_type_mesh = QtGui.QIcon(":/mesh.svg")
        self.icon_type_transform = QtGui.QIcon(":/transform.svg")
        self.icon_type_default = QtGui.QIcon(":/question.svg")

    def _apply_delegates(self):
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
        self._init_models()

    def populate_trees(self, comparison_data: Dict):
        self.clear_trees()
        old_root_item = self.model_old.invisibleRootItem()
        new_root_item = self.model_new.invisibleRootItem()
        self._populate_recursive(old_root_item, comparison_data.get("old", []))
        self._populate_recursive(new_root_item, comparison_data.get("new", []))
        self.tree_old.expandAll()
        self.tree_new.expandAll()

    def _populate_recursive(self, parent_item: QtGui.QStandardItem, children_data: List[NodeData]):
        for node_data in children_data:
            if node_data.status == "Placeholder":
                # 创建两列的占位符
                placeholder_name = QtGui.QStandardItem("")
                placeholder_name.setFlags(placeholder_name.flags() & ~QtCore.Qt.ItemIsSelectable)
                placeholder_status = QtGui.QStandardItem("")
                placeholder_status.setFlags(placeholder_status.flags() & ~QtCore.Qt.ItemIsSelectable)
                parent_item.appendRow([placeholder_name, placeholder_status])
                # 递归地为子节点创建占位符
                if node_data.children:
                    self._populate_recursive(placeholder_name, node_data.children)
            else:
                items = self._create_items_from_data(node_data)
                parent_item.appendRow(items)
                if node_data.children:
                    self._populate_recursive(items[0], node_data.children)

    def _create_items_from_data(self, node_data: NodeData) -> List[QtGui.QStandardItem]:
        """从NodeData对象创建QStandardItem。"""
        full_path = node_data.dag.fullPathName() if node_data.dag else "N/A"
        tooltip = f"路径: {full_path}\n状态: {node_data.status}\n详情: {node_data.details}"

        item_name = QtGui.QStandardItem(node_data.name)
        item_name.setData(full_path, QtCore.Qt.UserRole)
        item_name.setToolTip(tooltip)

        # 设置图标
        if node_data.node_type == "mesh":
            item_name.setIcon(self.icon_type_mesh)
        elif node_data.node_type == "transform":
            item_name.setIcon(self.icon_type_transform)
        else:
            item_name.setIcon(self.icon_type_default)

        # 设置高亮
        if node_data.status != "Unchanged":
            font = QtGui.QFont()
            font.setBold(True)
            font.setItalic(True)
            item_name.setFont(font)
            color_map = {"Added": QtGui.QColor(0, 150, 0), "Deleted": QtGui.QColor(200, 0, 0), "Modified": QtGui.QColor(0, 0, 220), "Error": QtGui.QColor(255, 100, 0)}
            if node_data.status in color_map:
                item_name.setForeground(QtGui.QBrush(color_map[node_data.status]))

        item_status = QtGui.QStandardItem(node_data.status)
        item_status.setToolTip(tooltip)
        return [item_name, item_status]


# ==============================================================================
# 4. 控制器 (Controller / Event Handler)
#    - 连接UI和新的OpenMaya逻辑层
# ==============================================================================
class ModelComparatorController:
    """控制器，负责连接UI和逻辑，处理用户事件。"""

    def __init__(self):
        self.ui = ModelComparatorUI()
        self.logic = ModelComparatorLogicOM()  # <-- 使用新的OM逻辑类
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

    def _handle_get_root(self, version_key: str):
        selection = cmds.ls(selection=True, type="transform")
        if not selection:
            cmds.warning("请在场景中选择一个变换节点。")
            return
        self.ui.set_root_path(version_key, selection[0])

    def _handle_run_comparison(self):
        self.ui.run_comparison_btn.setText("对比中...")
        self.ui.run_comparison_btn.setEnabled(False)

        root_old, root_new = self.ui.get_root_paths()
        try:
            comparison_data = self.logic.compare_hierarchies(root_old, root_new)
            global XXX
            XXX = comparison_data  # 用于调试
            print(comparison_data)
            self.ui.populate_trees(comparison_data)
        except ValueError as e:
            cmds.warning(str(e))
        except Exception as e:
            cmds.error(f"执行对比时发生未知错误: {e}")
            import traceback

            traceback.print_exc()
        finally:
            self.ui.run_comparison_btn.setText("执行对比")
            self.ui.run_comparison_btn.setEnabled(True)

    def _handle_item_double_clicked(self, index: QtCore.QModelIndex):
        full_path = index.data(QtCore.Qt.UserRole)
        if full_path and cmds.objExists(full_path):
            cmds.select(full_path, replace=True)
            cmds.viewFit()
            print(f"已选中: {full_path}")
        else:
            print(f"无法选中，物体 '{full_path}' 不存在。")

    def _sync_scroll_new(self, value: int):
        if self.is_syncing_scroll:
            return
        self.is_syncing_scroll = True
        self.ui.tree_new.verticalScrollBar().setValue(value)
        self.is_syncing_scroll = False

    def _sync_scroll_old(self, value: int):
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
        try:
            APP_INSTANCE.close_ui()
        except Exception:
            pass  # UI可能已被手动关闭
    APP_INSTANCE = ModelComparatorController()
    APP_INSTANCE.show()
    return APP_INSTANCE


# 在Maya Python脚本编辑器中执行此函数以启动工具
if __name__ == "__main__":
    show_comparator_tool()
