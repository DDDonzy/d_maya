import math
import maya.OpenMaya as om1  # type: ignore

from .cMemoryView import CMemoryManager
from . import cWeightsCoreCython  # 💥 需要重新导回 Cython 核心处理底层数组填充


class WeightsHandle:
    """
    权重数据装配器：负责 Maya 侧对象的生命周期、扩容和高级数据写入。
    底层内存暴露在 `memory` 中供核心层极速读取。
    """

    def __init__(self):
        self.plug = None
        self.data_handle = None
        self.mObj_mesh = None
        self.fn_mesh = None

        self._is_plug_mode = False
        self.max_capacity = 0
        self.length = 0

        # 💥 唯一对外暴露的底层内存管家（供 Cython 计算层直接提取裸数据）
        self.memory: CMemoryManager = None

    # =========================================================================
    # 1. 工厂方法
    # =========================================================================
    @classmethod
    def from_plug(cls, plug: om1.MPlug):
        instance = cls()
        instance.plug = plug
        instance._is_plug_mode = True
        try:
            instance.mObj_mesh = plug.asMObject()
        except RuntimeError:
            instance.mObj_mesh = om1.MObject()

        instance._setup_mesh()
        return instance

    @classmethod
    def from_data_handle(cls, data_handle: om1.MDataHandle):
        instance = cls()
        instance.data_handle = data_handle
        instance._is_plug_mode = False
        try:
            instance.mObj_mesh = data_handle.asMesh()
        except RuntimeError:
            instance.mObj_mesh = om1.MObject()

        instance._setup_mesh()
        return instance

    @classmethod
    def from_mesh(cls, fn_mesh):
        instance = cls()
        instance._is_plug_mode = False

        if isinstance(fn_mesh, om1.MFnMesh):
            instance.fn_mesh = fn_mesh
            instance.mObj_mesh = fn_mesh.object()
        else:
            instance.mObj_mesh = fn_mesh

        instance._setup_mesh()
        return instance

    @classmethod
    def from_attr_string(cls, attr_path: str):
        sel = om1.MSelectionList()
        try:
            sel.add(attr_path)
        except RuntimeError:
            raise ValueError(f"找不到指定的属性路径: {attr_path}")

        plug = om1.MPlug()
        sel.getPlug(0, plug)
        return cls.from_plug(plug)

    # =========================================================================
    # 2. 内部装配逻辑
    # =========================================================================
    def _setup_mesh(self):
        if self.fn_mesh is None and self.mObj_mesh and not self.mObj_mesh.isNull() and self.mObj_mesh.hasFn(om1.MFn.kMesh):
            self.fn_mesh = om1.MFnMesh(self.mObj_mesh)

        self._init_lengths()

    def _init_lengths(self):
        if self.fn_mesh is None or self.fn_mesh.numVertices() == 0:
            return

        self.max_capacity = self.fn_mesh.numVertices() * 3
        if self.max_capacity == 0:
            return

        # 💥 装配时，立刻初始化管家
        ptr_addr = int(self.fn_mesh.getRawPoints())
        self.memory = CMemoryManager.from_ptr(ptr_addr, "f", (self.max_capacity,))

        full_view = self.memory.view

        vl = self.max_capacity
        if vl > 0 and full_view[vl - 1] < -0.5:
            vl -= 1
        if vl > 0 and full_view[vl - 1] < -0.5:
            vl -= 1
        self.length = vl

    @property
    def is_valid(self):
        return (self.fn_mesh is not None) and (self.max_capacity > 0) and (self.memory is not None)

    # =========================================================================
    # 3. 容器生命周期管理
    # =========================================================================
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

        self.mObj_mesh = mesh_data_obj
        self.fn_mesh = new_mesh_fn
        self.max_capacity = num_points * 3
        self.length = target_length

        ptr_addr = int(self.fn_mesh.getRawPoints())
        self.memory = CMemoryManager.from_ptr(ptr_addr, "f", (self.max_capacity,))

        if self._is_plug_mode:
            self.plug.setMObject(mesh_data_obj)
        elif self.data_handle is not None:
            self.data_handle.setMObject(mesh_data_obj)

    def resize(self, length: int):
        if length > self.max_capacity:
            self._rebuild_mesh(length)
        else:
            self.length = length

    def commit(self):
        """通知 Maya 数据已更新"""
        if self._is_plug_mode and self.plug is not None and self.mObj_mesh is not None:
            self.plug.setMObject(self.mObj_mesh)

    # =========================================================================
    # 4. 高级数据写入接口 (保留高级方法，但全量采用内部管家提速)
    # =========================================================================
    def set_weights(self, src_data):

        src_mem_mgr = None

        if isinstance(src_data, (list, tuple)):
            src_mem_mgr = CMemoryManager.from_list(list(src_data), "f")
            if src_mem_mgr is None or src_mem_mgr.view is None:
                return
            src_view = src_mem_mgr.view
        elif isinstance(src_data, memoryview):
            src_view = src_data
        else:
            raise TypeError("src_data must be list, tuple, or memoryview")

        flat_src = src_view.cast("B").cast("f")
        target_length = flat_src.shape[0]

        self.resize(target_length)

        # 💥 极速原位拷贝 (直接使用内部管家)
        full_dest_view = self.memory.view
        full_dest_view[: self.length] = flat_src

        # 填充尾部无效数据为 -1.0
        if self.max_capacity > self.length:
            cWeightsCoreCython.fill_float_array(full_dest_view[self.length :], -1.0)

        self.commit()

    def fill_with_value(self, value: float):
        if not self.is_valid or self.length == 0:
            return

        full_dest_view = self.memory.view

        # 核心数据区填充
        cWeightsCoreCython.fill_float_array(full_dest_view[: self.length], value)

        # 尾部无效区填充
        if self.max_capacity > self.length:
            cWeightsCoreCython.fill_float_array(full_dest_view[self.length :], -1.0)

        self.commit()


class WeightsLayerData:
    """
    权重层数据结构，用于在 Python 层管理图层信息。
    """

    def __init__(
        self,
        index: int,
        enabled: bool,
        weightsHandle: WeightsHandle,
        maskHandle: WeightsHandle,
    ):

        self.index: int = index
        self.enabled: bool = enabled
        self.weightsHandle: WeightsHandle = weightsHandle
        self.maskHandle: WeightsHandle = maskHandle
