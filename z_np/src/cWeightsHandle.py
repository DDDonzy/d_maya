import math
import maya.OpenMaya as om1  # type: ignore

from . import cMemoryView
from . import cWeightsCoreCython


class WeightsHandle:
    def __init__(self, source):
        self.plug = None
        self.data_handle = None
        self.mesh_obj = om1.MObject()

        # True = 工具端 (MPlug)
        # False = 计算端 (MDataHandle)
        self._is_plug_mode = False

        # --- 模式 1: 工具端 ---
        if isinstance(source, om1.MPlug):
            self.plug = source
            self._is_plug_mode = True
            try:
                self.mesh_obj = self.plug.asMDataHandle().asMesh()
            except RuntimeError:
                self.mesh_obj = om1.MObject()

        # --- 模式 2: 计算端 ---
        elif isinstance(source, om1.MDataHandle):
            self.data_handle = source
            self._is_plug_mode = False
            try:
                self.mesh_obj = self.data_handle.asMesh()
            except RuntimeError:
                self.mesh_obj = om1.MObject()

        else:
            raise TypeError("Source 必须是 MPlug (工具) 或 MDataHandle (计算)！")

        self.mesh_fn = None
        if not self.mesh_obj.isNull() and self.mesh_obj.hasFn(om1.MFn.kMesh):
            self.mesh_fn = om1.MFnMesh(self.mesh_obj)

        self.max_capacity = 0
        self.length = 0
        self._init_lengths()

    def _init_lengths(self):
        if self.mesh_fn is None or self.mesh_fn.numVertices() == 0:
            return

        self.max_capacity = self.mesh_fn.numVertices() * 3
        if self.max_capacity == 0:
            return

        ptr_addr = int(self.mesh_fn.getRawPoints())
        full_view = cMemoryView.get_view_from_ptr(ptr_addr, "f", (self.max_capacity,))

        vl = self.max_capacity
        if vl > 0 and full_view[vl - 1] < -0.5:
            vl -= 1
        if vl > 0 and full_view[vl - 1] < -0.5:
            vl -= 1
        self.length = vl

    @property
    def is_valid(self):
        return (self.mesh_fn is not None) and (self.max_capacity > 0)

    def _rebuild_mesh(self, target_length: int):
        num_points = int(math.ceil(target_length / 3.0))
        num_points = max(3, num_points)

        v_count = om1.MIntArray()
        v_list = om1.MIntArray()
        v_count.append(3)
        v_list.append(0)
        v_list.append(1)
        v_list.append(2)

        base_pts = om1.MFloatPointArray()
        base_pts.setLength(num_points)

        mesh_data_obj = om1.MFnMeshData().create()
        new_mesh_fn = om1.MFnMesh()
        new_mesh_fn.create(num_points, 1, base_pts, v_count, v_list, mesh_data_obj)

        self.mesh_obj = mesh_data_obj
        self.mesh_fn = new_mesh_fn
        self.max_capacity = num_points * 3
        self.length = target_length

        if self._is_plug_mode:
            self.plug.setMObject(mesh_data_obj)  # 通知刷新
        elif self.data_handle is not None:
            self.data_handle.setMObject(mesh_data_obj)  # 仅更新容器

    def resize(self, length: int):
        if length > self.max_capacity:
            self._rebuild_mesh(length)
        else:
            self.length = length

    def get_view(self, shape=None):
        if not self.is_valid or self.length == 0:
            return None

        ptr_addr = int(self.mesh_fn.getRawPoints())
        full_view = cMemoryView.get_view_from_ptr(ptr_addr, "f", (self.max_capacity,))
        exact_1d_view = full_view[: self.length]

        if shape is not None:
            return cMemoryView.reshape_view(exact_1d_view, shape)

        return exact_1d_view

    def set_weights(self, src_data):
        if isinstance(src_data, (list, tuple)):
            src_view = cMemoryView.get_view_from_list(src_data, "f")
            if src_view is None:
                return
        elif isinstance(src_data, memoryview):
            src_view = src_data
        else:
            raise TypeError("src_data must be list, tuple, or memoryview")

        flat_src = src_view.cast("B").cast("f")
        target_length = flat_src.shape[0]

        self.resize(target_length)

        dest_addr = int(self.mesh_fn.getRawPoints())
        full_dest_view = cMemoryView.get_view_from_ptr(dest_addr, "f", (self.max_capacity,))

        full_dest_view[: self.length] = flat_src

        if self.max_capacity > self.length:
            cWeightsCoreCython.fill_float_array(full_dest_view[self.length :], -1.0)

        if self._is_plug_mode:
            self.plug.setMObject(self.mesh_obj)

    def fill_with_value(self, value: float):
        if not self.is_valid or self.length == 0:
            return

        dest_addr = int(self.mesh_fn.getRawPoints())
        full_dest_view = cMemoryView.get_view_from_ptr(dest_addr, "f", (self.max_capacity,))

        cWeightsCoreCython.fill_float_array(full_dest_view[: self.length], value)

        if self.max_capacity > self.length:
            cWeightsCoreCython.fill_float_array(full_dest_view[self.length :], -1.0)

        if self._is_plug_mode:
            self.plug.setMObject(self.mesh_obj)


class CSkinWeightManager:
    """
    节点权重管理器。
    用于在 UI 工具端安全地解析 cSkinDeform 节点的权重图层结构。
    """

    aWeights = "cWeights"
    aWeightsLayer = "cWeightsLayer"
    aWeightsLayerMask = "cWeightsLayerMask"
    aWeightsLayerCompound = "cWeightsLayers"
    aWeightsLayerEnabled = "cWeightsLayerEnabled"

    def __init__(self, node_name: str):
        self.node_name = node_name
        self.weights = None
        # 存储 Layer 字典的列表: [{'index': int, 'mesh': WeightsHandle, 'mask': WeightsHandle}]
        self.layers = []

        self._initialize_handles()

    def _initialize_handles(self):
        sel = om1.MSelectionList()
        try:
            sel.add(self.node_name)
        except RuntimeError:
            raise ValueError(f"❌ 场景中找不到节点 '{self.node_name}'！")

        dep_node = om1.MObject()
        sel.getDependNode(0, dep_node)
        fn_node = om1.MFnDependencyNode(dep_node)

        # 1. 解析 Base 层权重 (cBaseWeights)
        plug_base = fn_node.findPlug(CSkinWeightManager.aWeights, False)
        self.weights = WeightsHandle(plug_base)

        # 2. 解析所有 Layers 图层权重
        plug_layers = fn_node.findPlug(CSkinWeightManager.aWeightsLayerCompound, False)

        if not plug_layers.isNull() and plug_layers.isArray():
            attr_layer = fn_node.attribute(CSkinWeightManager.aWeightsLayer)
            attr_layer_mask = fn_node.attribute(CSkinWeightManager.aWeightsLayerMask)

            logical_indices = om1.MIntArray()
            plug_layers.getExistingArrayAttributeIndices(logical_indices)

            for i in range(logical_indices.length()):
                idx = logical_indices[i]
                plug_element = plug_layers.elementByLogicalIndex(idx)

                plug_mesh = plug_element.child(attr_layer)
                plug_mask = plug_element.child(attr_layer_mask)

                self.layers.append({
                    "index": idx,
                    "weights": WeightsHandle(plug_mesh),
                    "mask": WeightsHandle(plug_mask),
                })
