import ctypes

import maya.OpenMaya as om1  # type: ignore
import maya.OpenMayaMPx as ompx  # type: ignore

from z_np.src2.cMemoryView import CMemoryManager
from z_np.src2 import cWeightsHandle as CWH
from z_np.src2 import cSkinDeformCython


from z_np.src2.cSkinMemoryContext import SkinMemoryContext
from z_np.src2._cRegistry2 import SkinRegistry


from z_np.src2 import _profile


class CythonSkinDeformer(ompx.MPxDeformerNode):
    __slots__ = ("DATA",)
    aGeomMatrix = om1.MObject()
    aWeights = om1.MObject()
    aWeightsLayer = om1.MObject()
    aWeightsLayerMask = om1.MObject()
    aWeightsLayerEnabled = om1.MObject()
    aWeightsLayerCompound = om1.MObject()
    aInfluenceMatrix = om1.MObject()
    aBindPreMatrix = om1.MObject()
    aRefresh = om1.MObject()

    def __init__(self):
        super(CythonSkinDeformer, self).__init__()
        self.DATA: SkinMemoryContext = SkinMemoryContext()

        self._weights_is_dirty: bool = True
        self._influencesMatrix_is_dirty: bool = True
        self._bindPreMatrix_is_dirty: bool = True
        self._geoMatrix_is_dirty: bool = True
        self._geo_matrix = om1.MMatrix()
        self._get_matrix_i = om1.MMatrix()
        self._geo_matrix_is_identity = True


    def postConstructor(self):
        # 预先构建变形器需要的API对象，避免重复调用
        self.mObject = self.thisMObject()
        self.plug_refresh = om1.MPlug(self.mObject, self.aRefresh)  # 提前获取 refresh 的plug ，避免api开销

        # 数据储存到全局内存 (将自身的关键 API 对象写入数据总线)
        self.DATA.mObject = self.mObject
        self.DATA.mFnDep = om1.MFnDependencyNode(self.DATA.mObject)
        self.DATA.hashCode = om1.MObjectHandle(self.DATA.mObject).hashCode()

        # ！！！自身类，方便别的节点调用
        SkinRegistry.register(self.mObject, self)

    def setDependentsDirty(self, plug, dirtyPlugArray):
        weights_plugs = (
            self.aRefresh,
            self.aWeights,
            self.aWeightsLayerCompound,
            self.aWeightsLayerMask,
            self.aWeightsLayer,
            self.aWeightsLayerEnabled,
        )
        if plug in weights_plugs:
            self._weights_is_dirty = True

        elif plug == self.aInfluenceMatrix:
            self._influencesMatrix_is_dirty = True

        elif plug == self.aBindPreMatrix:
            self._bindPreMatrix_is_dirty = True
        elif plug == self.aGeomMatrix:
            self._geoMatrix_is_dirty = True

        return super(CythonSkinDeformer, self).setDependentsDirty(plug, dirtyPlugArray)

    def preEvaluation(self, context, evaluationNode):
        if context.isNormal():
            if evaluationNode.dirtyPlugExists(self.aGeomMatrix):
                self._geoMatrix_is_dirty = True

            if evaluationNode.dirtyPlugExists(self.aInfluenceMatrix):
                self._influencesMatrix_is_dirty = True

            if evaluationNode.dirtyPlugExists(self.aBindPreMatrix):
                self._bindPreMatrix_is_dirty = True
            # fmt:off
            if (   evaluationNode.dirtyPlugExists(self.aWeights)
                or evaluationNode.dirtyPlugExists(self.aWeightsLayerCompound)
                or evaluationNode.dirtyPlugExists(self.aWeightsLayerMask)
                or evaluationNode.dirtyPlugExists(self.aWeightsLayer)
                or evaluationNode.dirtyPlugExists(self.aWeightsLayerEnabled)
                or evaluationNode.dirtyPlugExists(self.aRefresh)
                ):
                self._weights_is_dirty = True
            # on 

        return super(CythonSkinDeformer, self).preEvaluation(context, evaluationNode)

    def update_base_topology(self, mFnMesh: om1.MFnMesh):
        """
        🧠 [Engine 核心] 提取并更新所有基础物理拓扑
        供 GPU渲染、Raycast 射线检测、Smooth 算法、Grow 扩张
        仅在变形器首次初始化，或模型顶点数发生改变时。
        """
        current_vertex_count = mFnMesh.numVertices()

        # 极速缓存拦截
        if self.DATA.vertex_count == current_vertex_count and self.DATA.tri_indices_2D is not None:
            return

        # ==========================================
        # 1. 提取面 (GPU 实体渲染 & 笔刷 Raycast 完美共享)
        # ==========================================
        tri_counts_mIntArray = om1.MIntArray()
        tri_vertex_indices_mIntArray = om1.MIntArray()
        mFnMesh.getTriangles(tri_counts_mIntArray, tri_vertex_indices_mIntArray)

        tri_counts = list(tri_counts_mIntArray)
        tri_vertex_indices = list(tri_vertex_indices_mIntArray)
        num_tris = len(tri_vertex_indices) // 3

        flat_tri_mgr = CMemoryManager.from_list(tri_vertex_indices, "i")
        self.DATA.tri_indices_2D = flat_tri_mgr.reshape((num_tris, 3))

        face_map_list = [0] * num_tris
        current_tri_idx = 0
        for face_id, count in enumerate(tri_counts):
            for _ in range(count):
                face_map_list[current_tri_idx] = face_id
                current_tri_idx += 1
        self.DATA.tri_to_face_map = CMemoryManager.from_list(face_map_list, "i")

        # ==========================================
        # 2. 提取边 (GPU 线框渲染专用，纯净无 offset)
        # ==========================================
        num_edges = mFnMesh.numEdges()
        self.DATA.base_edge_indices = CMemoryManager.allocate("i", (num_edges * 2,))
        edge_view = self.DATA.base_edge_indices.view
        util = om1.MScriptUtil()
        edge_ptr = util.asInt2Ptr()

        idx = 0
        for i in range(num_edges):
            mFnMesh.getEdgeVertices(i, edge_ptr)
            edge_view[idx] = om1.MScriptUtil.getInt2ArrayItem(edge_ptr, 0, 0)
            edge_view[idx + 1] = om1.MScriptUtil.getInt2ArrayItem(edge_ptr, 0, 1)
            idx += 2

        # ==========================================
        # 3. 提取顶点邻接表 (CSR格式：为 Smooth 和 Grow 算法铺路！)
        # ==========================================
        # 💥 降维打击：直接利用第 2 步提取出的边 (Edges) 反推邻接关系！
        # 彻底抛弃娇贵的 MItMeshVertex，完美避开 Object does not exist 的底层 Bug！

        adj_list = [[] for _ in range(current_vertex_count)]

        # 遍历刚才提取出来的所有边
        for i in range(num_edges):
            v1 = edge_view[i * 2]
            v2 = edge_view[i * 2 + 1]
            # 边是双向的：v1 的邻居有 v2，v2 的邻居有 v1
            adj_list[v1].append(v2)
            adj_list[v2].append(v1)

        # 转换为 CSR 极速查找格式
        offsets_list = [0] * (current_vertex_count + 1)
        indices_list = []
        current_offset = 0

        for i in range(current_vertex_count):
            neighbors = adj_list[i]
            indices_list.extend(neighbors)

            offsets_list[i] = current_offset
            current_offset += len(neighbors)

        offsets_list[current_vertex_count] = current_offset  # 封口

        # 安全存入黑板
        self.DATA.adj_offsets = CMemoryManager.from_list(offsets_list, "i")
        self.DATA.adj_indices = CMemoryManager.from_list(indices_list, "i")

        # ==========================================
        # 💥 4. 终极优化：一次性申请笔刷计算需要的内存池！
        # ==========================================
        self.DATA.pool_node_epochs = CMemoryManager.allocate("i", (current_vertex_count,))
        self.DATA.pool_dist = CMemoryManager.allocate("f", (current_vertex_count,))
        self.DATA.pool_queue = CMemoryManager.allocate("i", (current_vertex_count,))
        self.DATA.pool_in_queue = CMemoryManager.allocate("b", (current_vertex_count,))  # 用 int8 当 bool 即可
        self.DATA.pool_touched = CMemoryManager.allocate("i", (current_vertex_count,))

        # 初始化世代簿全为 0
        epochs_view = self.DATA.pool_node_epochs.view
        for i in range(current_vertex_count):
            epochs_view[i] = 0

        # 最后更新总顶点数，表示拓扑提取彻底完成
        self.DATA.vertex_count = current_vertex_count

    def _setDirty(self):
        """
        - 用于笔刷调用，提醒Deform，更新权重
        - 设置自身 “refresh” 属性，refresh 影响 outputGeometry
        """
        current_val = self.plug_refresh.asInt()
        self.plug_refresh.setInt((current_val + 1) % 2)
        self._weights_is_dirty = True

    def deform(self, dataBlock: om1.MDataBlock, geoIter, localToWorldMatrix, multiIndex):
        with _profile.MicroProfiler(target_runs=100, enable=False) as prof:
            # fmt:off
            # region ----------- envelope -----------------------------------------------------
            envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
            if envelope == 0.0:
                return
            # endregion

            # region ----------- Get Raw Points --------------------------------------------
            # original mesh
            mFnMesh, vertexCount, memoryManger = self._get_original_data(dataBlock, multiIndex)
            self.DATA.mFnMesh_original         = mFnMesh
            self.DATA.rawPoints_original       = memoryManger
            self.DATA.rawPoints2D_original     = memoryManger.reshape((vertexCount, 3))

            # output mesh
            mFnMesh, vertexCount, memoryManger = self._get_output_data(dataBlock, multiIndex)
            self.DATA.mFnMesh_output           = mFnMesh
            self.DATA.rawPoints_output         = memoryManger
            self.DATA.rawPoints2D_output       = memoryManger.reshape((vertexCount, 3))

            # check topology
            # 统一由引擎接管所有拓扑的提取和下发
            if self.DATA.vertex_count != vertexCount:
                self.update_base_topology(self.DATA.mFnMesh_original)
            prof.step("1_GetMesh_Points")
            # endregion

            # region ----------- Influences --------------------------------------------------
            influences_handle = dataBlock.inputArrayValue(self.aInfluenceMatrix)
            influences_count = influences_handle.elementCount()
            prof.step("2.0_pool")
            if self.DATA.influences_count != influences_count:
                """ 内存骨骼数量 和 maya 骨骼数量不一样，重新分配内存 """
                self.DATA.influences_count      = influences_count
                self.DATA._influencesMatrix_mgr = CMemoryManager.allocate("d", (influences_count, 16))
                self.DATA._rotateMatrix_mgr     = CMemoryManager.allocate("f", (influences_count, 9))
                self.DATA._translateVector_mgr  = CMemoryManager.allocate("f", (influences_count, 3))
                """填充为单位矩阵，后续可以考虑删掉/优化"""
                for b in range(influences_count):
                    for i in range(16):
                        self.DATA._influencesMatrix_mgr.view[b, i] = 1.0 if (i % 5 == 0) else 0.0
            prof.step("2.1_pool")
            # ----------- Influences Matrix -----------------------------------------
            if self._influencesMatrix_is_dirty:
                if influences_count > 0:
                    dest_base_addr = self.DATA._influencesMatrix_mgr.ptr_addr
                    for i in range(influences_count):
                        influences_handle.jumpToArrayElement(i)
                        influence_idx = influences_handle.elementIndex()
                        src_addr = int(influences_handle.inputValue().asMatrix().this)
                        dest_addr = dest_base_addr + (influence_idx * 128)  # (4*4)*8
                        ctypes.memmove(dest_addr, src_addr, 128)            # (4*4)*8
                    self._influencesMatrix_is_dirty = False
            prof.step("3_GetInfluences")
            # ----------- Bind Pre Matrix -------------------------------------------
            if self._bindPreMatrix_is_dirty:
                bind_data_obj = dataBlock.inputValue(self.aBindPreMatrix).data()
                if not bind_data_obj.isNull():
                    fn_bind_array = om1.MFnMatrixArrayData(bind_data_obj)
                    bind_m_array = fn_bind_array.array()
                    length = bind_m_array.length()
                    if length > 0:
                        addr_base = int(bind_m_array[0].this)
                        self.DATA._bindPreMatrix_mgr = CMemoryManager.from_ptr(addr_base, "d", (length, 16))
                    self._bindPreMatrix_is_dirty = False
            prof.step("4_GetBindMatrix")
            # -----------  Geometry Matrix ------------------
            if self._geoMatrix_is_dirty:
                geo_matrix_handle = dataBlock.inputValue(self.aGeomMatrix)
                self._geo_matrix = geo_matrix_handle.asMatrix()
                self._get_matrix_i = self._geo_matrix.inverse()
                self._geo_matrix_is_identity = self._geo_matrix.isEquivalent(om1.MMatrix.identity)
                self.DATA.geo_matrix = self._geo_matrix
                self._geoMatrix_is_dirty = False
            prof.step("4.1_GeometryMatrix")
            # endregion

            # region ----------- Weights --------------------------------------------------
            if self._weights_is_dirty:
                self.DATA.weightsLayer = self._get_weights_layers_data(dataBlock)
                self._weights_is_dirty = False

            if self.DATA.weightsLayer[-1].weightsHandle.is_valid is False:
                return
            prof.step("5_Weights")
            # endregion

            # region ----------- Cal --------------------------------------------------
            cSkinDeformCython.compute_deform_matrices(
                int(self._geo_matrix.this),
                int(self._get_matrix_i.this),
                self.DATA._bindPreMatrix_mgr.view,
                self.DATA._influencesMatrix_mgr.view,
                self.DATA._rotateMatrix_mgr.view,
                self.DATA._translateVector_mgr.view,
                self._geo_matrix_is_identity,
            )
            prof.step("6_PreData")

            cSkinDeformCython.run_skinning_core(
                self.DATA.rawPoints_original.view,
                self.DATA.rawPoints_output.view,
                self.DATA.weightsLayer[-1].weightsHandle.memory.view,
                self.DATA._rotateMatrix_mgr.view,
                self.DATA._translateVector_mgr.view,
                envelope,
            )
            prof.step("7_Skin")
            # endregion
            # fmt:on

    def _get_mesh_data(self, mesh_obj: om1.MObject) -> tuple[om1.MFnMesh, int, CMemoryManager]:
        """从 MFnMesh 提取为底层 C 内存视图元组"""
        if mesh_obj.isNull():
            return None, 0, None
        mFnMesh = om1.MFnMesh(mesh_obj)
        vertex_count = mFnMesh.numVertices()
        rawPoints_mgr = CMemoryManager.from_ptr(int(mFnMesh.getRawPoints()), "f", (vertex_count * 3,))
        return mFnMesh, vertex_count, rawPoints_mgr

    def _get_original_data(self, dataBlock: om1.MDataBlock, multiIndex) -> tuple[om1.MFnMesh, int, CMemoryManager]:
        """获取 maya original raw points 内存视图 (只读)"""
        inputArrayHandle = dataBlock.inputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        inputArrayHandle.jumpToElement(multiIndex)
        inputGeomObj = inputArrayHandle.inputValue().child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        return self._get_mesh_data(inputGeomObj)

    def _get_output_data(self, dataBlock: om1.MDataBlock, multiIndex) -> tuple[om1.MFnMesh, int, CMemoryManager]:
        """获取 maya output geometry raw points 内存视图 (可写)"""
        outputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_outputGeom)
        outputArrayHandle.jumpToElement(multiIndex)
        outputGeomObj = outputArrayHandle.outputValue().asMesh()
        return self._get_mesh_data(outputGeomObj)

    def _get_weights_layers_data(self, dataBlock: om1.MDataBlock) -> dict[int, CWH.WeightsLayerData]:
        """
        提取基础权重与所有权重图层数据
        返回: 包含所有图层数据的字典 {layer_index: WeightsLayerData}
        """
        layer_data_dict = {}

        # 提取基础权重 (Base Weights, 默认归档为 -1 层)
        base_weights_val = dataBlock.inputValue(self.aWeights)
        base_weights_handle = CWH.WeightsHandle.from_data_handle(base_weights_val)
        layer_data_dict[-1] = CWH.WeightsLayerData(-1, True, base_weights_handle, None)

        # 提取层 (Compound Layers)
        layer_array_handle = dataBlock.inputArrayValue(self.aWeightsLayerCompound)
        element_count = layer_array_handle.elementCount()

        for i in range(element_count):
            layer_array_handle.jumpToArrayElement(i)
            logical_idx = layer_array_handle.elementIndex()
            element_handle = layer_array_handle.inputValue()
            weights_handle = CWH.WeightsHandle.from_data_handle(element_handle.child(self.aWeightsLayer))
            mask_handle = CWH.WeightsHandle.from_data_handle(element_handle.child(self.aWeightsLayerMask))
            enabled_handle = element_handle.child(self.aWeightsLayerEnabled)

            layer_data_dict[logical_idx] = CWH.WeightsLayerData(
                logical_idx,
                enabled_handle.asBool(),
                weights_handle,
                mask_handle,
            )

        return layer_data_dict

    @classmethod
    def nodeInitializer(cls):
        # fmt:off
        tAttr = om1.MFnTypedAttribute()
        mAttr = om1.MFnMatrixAttribute()
        nAttr = om1.MFnNumericAttribute()
        cAttr = om1.MFnCompoundAttribute()

        cls.aGeomMatrix           = mAttr.create("geomMatrix", "gm")
        mAttr.setHidden(True)
        mAttr.setKeyable(False)
        cls.addAttribute(cls.aGeomMatrix)

        cls.aWeights              = tAttr.create("cWeights", "cw", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aWeights)
        cls.aInfluenceMatrix      = mAttr.create("matrix", "bm")
        mAttr.setArray(True)
        mAttr.setHidden(True)
        mAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aInfluenceMatrix)
        cls.aBindPreMatrix        = tAttr.create("bindPreMatrixArray", "bpm", om1.MFnData.kMatrixArray)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aBindPreMatrix)
        cls.aWeightsLayer         = tAttr.create("cWeightsLayer", "cwl", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.aWeightsLayerMask     = tAttr.create("cWeightsLayerMask", "cwlm", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.aWeightsLayerEnabled  = nAttr.create("cWeightsLayerEnabled", "cwle", om1.MFnNumericData.kBoolean, False)
        nAttr.setHidden(True)
        cls.aWeightsLayerCompound = cAttr.create("cWeightsLayers", "cwls")
        cAttr.setArray(True)
        cAttr.setHidden(True)
        cAttr.setUsesArrayDataBuilder(True)
        cAttr.addChild(cls.aWeightsLayerEnabled)
        cAttr.addChild(cls.aWeightsLayer)
        cAttr.addChild(cls.aWeightsLayerMask)
        cls.addAttribute(cls.aWeightsLayerCompound)
        cls.aRefresh              = nAttr.create("refresh", "rf", om1.MFnNumericData.kInt, 0)
        nAttr.setStorable(False)
        nAttr.setHidden(True)
        nAttr.setKeyable(False)
        nAttr.setWritable(False)
        nAttr.setReadable(True)
        cls.addAttribute(cls.aRefresh)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom

        cls.attributeAffects(cls.aGeomMatrix, cls.aRefresh)
        cls.attributeAffects(cls.aWeights, cls.aRefresh)
        cls.attributeAffects(cls.aInfluenceMatrix, cls.aRefresh)
        cls.attributeAffects(cls.aBindPreMatrix, cls.aRefresh)
        cls.attributeAffects(cls.aWeightsLayerCompound, cls.aRefresh)

        cls.attributeAffects(cls.aGeomMatrix, outputGeom)
        cls.attributeAffects(cls.aWeights, outputGeom)
        cls.attributeAffects(cls.aInfluenceMatrix, outputGeom)
        cls.attributeAffects(cls.aBindPreMatrix, outputGeom)
        cls.attributeAffects(cls.aWeightsLayerCompound, outputGeom)
        cls.attributeAffects(cls.aRefresh, outputGeom)

        # fmt:on
