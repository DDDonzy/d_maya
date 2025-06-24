from PySide2 import QtWidgets, QtGui, QtCore

from typing import Tuple, List
from enum import Enum
from maya.api import OpenMaya as om
from maya import cmds
import collections


class Status(Enum):
    noChange = 0
    add = 1
    delete = 2
    modify = 3
    position = 4
    uv = 5
    vertexOrder = 6
    topologize = 7

    @property
    def background_color(self) -> Tuple[int, int, int]:
        if self.value == 0:
            return (0, 0, 0)
        elif self.value == 1:
            return (0, 1, 0)
        elif self.value == 2:
            return (1, 0, 0)
        elif self.value >= 3:
            return (1, 1, 0)


class TreeNode:
    def __init__(
        self,
        name: str,
        status: Status = Status.noChange,
        parent: "TreeNode" = None,
    ):
        self.name = name
        self.status = status
        self.children = []
        self.parent = parent


class DagPathWrapper(om.MDagPath):
    """包装 MDagPath 并添加额外属性"""

    def __init__(self, *args, **kwargs):
        self.depth = kwargs.pop("depth", 0)
        self.index = kwargs.pop("index", 0)
        self.children = kwargs.pop("children", [])
        self.parent = kwargs.pop("parent", None)
        super().__init__(*args, **kwargs)


class IterHierarchy:
    def __init__(self, root: str | om.MDagPath, skipShape=True):
        # check input
        if isinstance(root, om.MDagPath):
            self.root_node: om.MDagPath = root
        elif isinstance(root, str):
            self.root_node: om.MDagPath = om.MSelectionList().add(root).getDagPath(0)
        else:
            raise Exception("Invalid root node, must be a string or MDagPath.")

        self.skipShape = skipShape

        # save the depth and index of each node for sorting
        self._depthAndIdx = collections.defaultdict(lambda: [0, 0])  # name: (depth, index)

        # result iterator list
        self._reset()

    def _reset(self):
        self.iterList = [self.root_node]

    def __iter__(self):
        self._reset()
        return self

    def __next__(self) -> Tuple[str, om.MDagPath]:
        if not self.iterList:
            raise StopIteration("End of iteration.")
        # get the current node
        current_dag = self.iterList.pop()
        name: str = current_dag.partialPathName()
        depth = current_dag.length()
        thisDepthIndex = self._depthAndIdx.get(depth, 0) + 1
        self._depthAndIdx[depth] = thisDepthIndex

        # get the children
        children: List[om.MDagPath] = []
        # is skip shape?
        for x in range(current_dag.childCount()):
            mObj: om.MObject = current_dag.child(x)
            if (not mObj.hasFn(om.MFn.kTransform)) and (not self.skipShape):
                continue
            children.append(om.MDagPath.getAPathTo(mObj))

        self.iterList.extend(reversed(children))

        return name, DagPathWrapper(
            current_dag,
            depth=depth,
            index=thisDepthIndex,
            children=children,
            parent=current_dag.pop(),
        )


class ModelComparatorLogic:
    """负责模型对比的核心逻辑，不依赖任何UI。"""

    def compare_hierarchies(self, root_old, root_new):
        """
        执行层级对比，并返回一个结构化的数据。

        Args:
            root_old (str): 旧版本根节点的完整路径。
            root_new (str): 新版本根节点的完整路径。

        Returns:
            tuple: 包含对比结果的元组，格式为 (old_tree, new_tree)。
                   每个tree都是TreeNode的根节点。
        """
        if not all([root_old, root_new, cmds.objExists(root_old), cmds.objExists(root_new)]):
            raise ValueError("请提供有效的新旧两个版本的根节点。")

        old_tree, new_tree = self._build_comparison_trees(root_old, root_new)
        return old_tree, new_tree

    # --- 模块化对比函数 ---
    def _get_transform_status(self, node_old, node_new):
        """对比世界矩阵。如果不同，返回Status.position。"""
        matrix_old = cmds.xform(node_old, q=True, matrix=True, worldSpace=True)
        matrix_new = cmds.xform(node_new, q=True, matrix=True, worldSpace=True)
        return Status.position if matrix_old != matrix_new else None

    def _get_shape_structure_status(self, node_old, node_new):
        """对比shape节点的存在性。如果结构不同，返回Status.modify。"""
        shape_old = cmds.listRelatives(node_old, shapes=True, noIntermediate=True, fullPath=True)
        shape_new = cmds.listRelatives(node_new, shapes=True, noIntermediate=True, fullPath=True)
        return Status.modify if bool(shape_old) != bool(shape_new) else None

    def _get_topology_status(self, node_old, node_new):
        """对比mesh的拓扑（点/边/面数量）。如果拓扑不同，返回Status.topologize。"""
        shape_old = cmds.listRelatives(node_old, shapes=True, noIntermediate=True, fullPath=True)
        shape_new = cmds.listRelatives(node_new, shapes=True, noIntermediate=True, fullPath=True)

        if shape_old and shape_new and cmds.nodeType(shape_old[0]) == "mesh" and cmds.nodeType(shape_new[0]) == "mesh":
            stats_old = (cmds.polyEvaluate(shape_old[0], vertex=True), cmds.polyEvaluate(shape_old[0], edge=True), cmds.polyEvaluate(shape_old[0], face=True))
            stats_new = (cmds.polyEvaluate(shape_new[0], vertex=True), cmds.polyEvaluate(shape_new[0], edge=True), cmds.polyEvaluate(shape_new[0], face=True))
            return Status.topologize if stats_old != stats_new else None
        return None

    def _get_node_status(self, node_old, node_new):
        """统一调用所有对比函数，并返回最高优先级的状态。"""
        try:
            for check_func in [
                self._get_topology_status,
                self._get_transform_status,
                self._get_shape_structure_status,
            ]:
                status = check_func(node_old, node_new)
                if status is not None:
                    return status
            return Status.noChange
        except Exception as e:
            print(f"对比节点 '{node_old}' 和 '{node_new}' 时出错: {e}")
            return Status.modify

    # --- 核心构建逻辑 ---
    def _build_comparison_trees(self, root_old, root_new):
        """构建和对比两个层级树，返回TreeNode根节点。"""
        # 直接构建树结构
        old_tree = self._build_tree(root_old)
        new_tree = self._build_tree(root_new)

        # 对比并更新状态
        self._compare_trees(old_tree, new_tree, root_old, root_new)

        return old_tree, new_tree

    def _build_tree(self, root_path):
        """使用IterHierarchy直接构建TreeNode树。"""
        if not root_path or not cmds.objExists(root_path):
            return None

        root_name = root_path.split("|")[-1].split(":")[-1]
        root_node = TreeNode(root_name, Status.noChange)

        # 使用字典临时存储节点，便于查找父节点
        node_map = {root_path: root_node}

        try:
            iter_hierarchy = IterHierarchy(root_path, skipShape=True)
            for name, dag_path in iter_hierarchy:
                full_path = dag_path.fullPathName()
                if full_path == root_path:
                    continue  # 跳过根节点

                # 创建当前节点
                short_name = name.split(":")[-1]
                current_node = TreeNode(short_name, Status.noChange)
                node_map[full_path] = current_node

                # 查找父节点并建立关系
                parent_path = "|".join(full_path.split("|")[:-1])
                if parent_path in node_map:
                    parent_node = node_map[parent_path]
                    current_node.parent = parent_node
                    parent_node.children.append(current_node)

        except Exception as e:
            print(f"构建树结构时出错 '{root_path}': {e}")

        return root_node

    def _compare_trees(self, old_tree, new_tree, old_root_path, new_root_path):
        """递归对比两个树并更新状态。"""
        # 创建子节点名称映射
        old_children = {child.name: child for child in old_tree.children}
        new_children = {child.name: child for child in new_tree.children}

        # 获取所有子节点名称
        all_names = set(old_children.keys()) | set(new_children.keys())

        for name in all_names:
            old_child = old_children.get(name)
            new_child = new_children.get(name)

            if old_child and new_child:
                # 节点在两边都存在，进行对比
                old_path = self._get_node_path(old_child, old_root_path)
                new_path = self._get_node_path(new_child, new_root_path)

                if old_path and new_path:
                    status = self._get_node_status(old_path, new_path)
                    old_child.status = status
                    new_child.status = status

                    # 递归处理子节点
                    self._compare_trees(old_child, new_child, old_root_path, new_root_path)

            elif old_child:
                # 节点只在旧版本存在（被删除）
                self._mark_tree_status(old_child, Status.delete)
                # 在新树中创建占位节点
                placeholder = TreeNode("", Status.noChange, new_tree)
                new_tree.children.append(placeholder)

            elif new_child:
                # 节点只在新版本存在（被添加）
                self._mark_tree_status(new_child, Status.add)
                # 在旧树中创建占位节点
                placeholder = TreeNode("", Status.noChange, old_tree)
                old_tree.children.append(placeholder)

    def _get_node_path(self, node, root_path):
        """根据节点获取其在Maya中的完整路径。"""
        if not node or not node.name:
            return None

        # 从根节点构建路径
        path_parts = []
        current = node
        while current and current.name:
            path_parts.append(current.name)
            current = current.parent

        if not path_parts:
            return None

        # 反转并组合路径
        path_parts.reverse()
        full_path = root_path
        for part in path_parts[1:]:  # 跳过根节点名称
            full_path += "|" + part

        return full_path if cmds.objExists(full_path) else None

    def _mark_tree_status(self, node, status):
        """递归标记节点及其所有子节点的状态。"""
        node.status = status
        for child in node.children:
            self._mark_tree_status(child, status)
