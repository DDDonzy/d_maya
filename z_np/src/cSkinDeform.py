import ctypes
import maya.OpenMaya as om1  # type: ignore
import maya.OpenMayaMPx as ompx  # type: ignore

from . import cMemoryView
from . import cWeightsHandle
from . import cSkinDeformCython
from . import cWeightsCoreCython


class CythonSkinDeformer(ompx.MPxDeformerNode):
    aInfluenceMatrix = om1.MObject()
    aBindPreMatrix = om1.MObject()

    aWeights = om1.MObject()

    aWeightsLayer = om1.MObject()
    aWeightsLayerMask = om1.MObject()
    aWeightsLayerEnabled = om1.MObject()

    def __init__(self):
        super(CythonSkinDeformer, self).__init__()
        self.current_influences_count = 0
        self.current_vertex_count = 0

        # 纯 ctypes 底层容器引用
        # 由于 maya 矩阵输入是数组插槽，所以无法获取连续内存地址，只能在这里自己开辟连续内存，然后在 deform 前把数据 memcpy 过去，供 Cython 侧直接访问
        self._c_influences_matrices = None  # 变形矩阵 4x4*N
        # 为了加速计算，变形矩阵拆分为 旋转+缩放矩阵 3x3 和 位移向量 3，分别存储在两个连续内存块里
        self._c_rotate_matrices = None  # 旋转矩阵 3x3*N
        self._c_translate_vectors = None  # 位移向量 3*N

        # 提前映射的 MemoryView 缓存
        self.influences_matrices_view = None
        self.rotate_matrices_view = None
        self.translate_vectors_view = None

    @classmethod
    def nodeInitializer(cls):
        tAttr = om1.MFnTypedAttribute()
        mAttr = om1.MFnMatrixAttribute()
        nAttr = om1.MFnNumericAttribute()
        cAttr = om1.MFnCompoundAttribute()

        # 存储权重数据，用于最终变形计算
        # 由于 kMesh getRawPoint 直接映射底层内存地址
        # 把权重一维数组reshape成 N x 3 的形式，存住在rawPoints中，供 Cython 侧直接访问
        # 需要注意，vertex 数量和骨骼数量的乘积可能会非常大，必须保证 Maya 里这个 kMesh 的顶点数量足够
        cls.aWeights = tAttr.create("cWeights", "cw", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aWeights)

        # 骨骼矩阵，数组插槽形式，每个元素是一个 4x4 矩阵，
        # 由于 Maya 数组插槽不保证连续内存，所以无法直接映射给 Cython 侧访问，只能在 deform 前把数据 memcpy 到连续内存池里，供 Cython 侧访问
        cls.aInfluenceMatrix = mAttr.create("matrix", "bm")
        mAttr.setArray(True)
        mAttr.setHidden(True)
        mAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aInfluenceMatrix)

        # BindPoseMatrix 的逆矩阵数组，数组数据 MMatrixArrayData，直接映射 Maya 底层内存给 Cython 侧访问
        # 由于不是插槽形式，所以 Cython 侧可以直接获取连续内存地址，设置参数有点麻烦，需要使用 MatrixArrayData
        cls.aBindPreMatrix = tAttr.create("bindPreMatrixArray", "bpm", om1.MFnData.kMatrixArray)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aBindPreMatrix)

        # 权重层，权重和遮罩两个子属性，数组插槽形式
        # 同样使用 kMesh 来存储权重数据，利用 getRawPoints 获取连续内存地址，供 Cython 侧直接访问
        # cWeightsLayer 存储权重信息，格式同 aWeights，供 Cython 侧直接访问
        # cWeightsLayerMask 存储遮罩信息，0-1 浮点数，乘在权重上实现局部权重调整的功能
        cls.aWeightsLayer = tAttr.create("cWeightsLayer", "cwl", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.aWeightsLayerMask = tAttr.create("cWeightsLayerMask", "cwlm", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.aWeightsLayerEnabled = nAttr.create("cWeightsLayerEnabled", "cwle", om1.MFnNumericData.kBoolean, False)
        nAttr.setHidden(True)
        cls.aWeightsLayerCompound = cAttr.create("cWeightsLayers", "cwls")
        cAttr.setArray(True)
        cAttr.setHidden(True)
        cAttr.setUsesArrayDataBuilder(True)
        cAttr.addChild(cls.aWeightsLayerEnabled)
        cAttr.addChild(cls.aWeightsLayer)
        cAttr.addChild(cls.aWeightsLayerMask)
        cls.addAttribute(cls.aWeightsLayerCompound)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.aWeights, outputGeom)
        cls.attributeAffects(cls.aInfluenceMatrix, outputGeom)
        cls.attributeAffects(cls.aBindPreMatrix, outputGeom)
        cls.attributeAffects(cls.aWeightsLayerCompound, outputGeom)

    def _ensure_pool_size(self, dataBlock):
        """
        根据当前骨骼数量需求，动态调整内存池大小。
        如果骨骼数量为 0 或未变化，则保持现状，返回当前数量。
        否则重新申请连续内存块，并更新当前数量记录，返回新的骨骼数量。
        """
        mat_handle = dataBlock.inputArrayValue(self.aInfluenceMatrix)
        influences_count = mat_handle.elementCount()

        if (influences_count <= 0) or (influences_count == self.current_influences_count):
            return influences_count

        # 使用 ctypes 申请连续内存！
        self._c_influences_matrices = ((ctypes.c_double * 16) * influences_count)()
        self._c_rotate_matrices = ((ctypes.c_float * 9) * influences_count)()
        self._c_translate_vectors = ((ctypes.c_float * 3) * influences_count)()

        # 使用 cMemoryView 获取地址视图
        influences_matrices_addr = ctypes.addressof(self._c_influences_matrices)
        self.influences_matrices_view = cMemoryView.get_view_from_ptr(influences_matrices_addr, "d", (influences_count, 16))  # double

        rotate_matrices_addr = ctypes.addressof(self._c_rotate_matrices)
        self.rotate_matrices_view = cMemoryView.get_view_from_ptr(rotate_matrices_addr, "f", (influences_count, 9))  # float

        translate_vectors_addr = ctypes.addressof(self._c_translate_vectors)
        self.translate_vectors_view = cMemoryView.get_view_from_ptr(translate_vectors_addr, "f", (influences_count, 3))  # float

        # 填充单位矩阵作为初始值
        for b in range(influences_count):
            for i in range(16):
                self._c_influences_matrices[b][i] = 1.0 if (i % 5 == 0) else 0.0

        self.current_influences_count = influences_count
        return influences_count

    def _get_bind_matrices_view(self, dataBlock):
        """
        获取 bind pre matrices 的 MemoryView 视图，供 Cython 侧直接访问
        直接映射 Maya 底层 C++ 内存，返回给 Cython 核心使用
        """
        bind_data_obj = dataBlock.inputValue(self.aBindPreMatrix).data()
        if bind_data_obj is None or bind_data_obj.isNull():
            return None

        fn_bind_array = om1.MFnMatrixArrayData(bind_data_obj)
        bind_m_array = fn_bind_array.array()

        length = bind_m_array.length()
        if length == 0:
            return None

        addr_base = int(bind_m_array[0].this)
        return cMemoryView.get_view_from_ptr(addr_base, "d", (length, 16))

    def _get_influences_matrices_view(self, dataBlock):
        """
        * 获取 influences matrices 的 MemoryView 视图，供 Cython 侧直接访问
        * 由于 Maya 数组插槽不保证连续内存，所以只能逐个元素复制到申请的连续内存`self.influences_matrices_view`，返回这个连续内存的视图给 Cython 使用
        """
        if self.current_influences_count <= 0:
            return None

        mat_handle = dataBlock.inputArrayValue(self.aInfluenceMatrix)
        num_elements = mat_handle.elementCount()

        # memoryview 对于二维及以上的多维视图切片操作不友好，所以这里把二维视图拍平成一维
        # 在一维视图上进行切片操作，计算出每个矩阵在连续内存中的起始位置和结束位置，进行批量设置矩阵数据
        # 视图都是同一块内存，设置后，直接访问二维视图时就能得到正确的 16 元素矩阵数据了，无需再次 reshape
        total_elements = self.current_influences_count * 16
        flat_dest_view = cMemoryView.reshape_view(self.influences_matrices_view, (total_elements,))

        for i in range(num_elements):
            mat_handle.jumpToElement(i)
            influence_idx = mat_handle.elementIndex()
            if influence_idx >= self.current_influences_count:
                continue

            m_obj = mat_handle.inputValue().asMatrix()
            src_addr = int(m_obj.this)

            i_matrix_view = cMemoryView.get_view_from_ptr(src_addr, "d", (16,))

            start_idx = influence_idx * 16
            end_idx = start_idx + 16

            flat_dest_view[start_idx:end_idx] = i_matrix_view

        return self.influences_matrices_view

    def _get_original_points_view(self, dataBlock, multiIndex):
        inputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        inputArrayHandle.jumpToElement(multiIndex)
        inputGeomObj = inputArrayHandle.outputValue().child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        if inputGeomObj.isNull():
            return None

        fn_input_mesh = om1.MFnMesh(inputGeomObj)
        self.current_vertex_count = fn_input_mesh.numVertices()

        ori_pts_addr = int(fn_input_mesh.getRawPoints())
        return cMemoryView.get_view_from_ptr(ori_pts_addr, "f", (self.current_vertex_count * 3,))

    def _get_output_points_view(self, dataBlock, multiIndex):
        outputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_outputGeom)
        outputArrayHandle.jumpToElement(multiIndex)
        outputGeomObj = outputArrayHandle.outputValue().asMesh()
        if outputGeomObj.isNull():
            return None

        out_pts_addr = int(om1.MFnMesh(outputGeomObj).getRawPoints())
        return cMemoryView.get_view_from_ptr(out_pts_addr, "f", (self.current_vertex_count * 3,))

    def _compute_blended_weights_inplace(self, dataBlock):
        # 1. 准备画布（逻辑同前，保持 WeightsHandle 封装）
        weights_handle = cWeightsHandle.WeightsHandle(dataBlock.inputValue(self.aWeights))
        total_len = self.current_vertex_count * self.current_influences_count
        if total_len == 0:
            return None

        weights_handle.resize(total_len)
        weights_handle.fill_with_value(0.0)
        canvas_view = weights_handle.get_view()

        layer_array_handle = dataBlock.inputArrayValue(self.aWeightsLayerCompound)

        # 获取物理上存在的元素数量
        num_physical = layer_array_handle.elementCount()
        if num_physical == 0:
            return None

        has_layers_active = False

        for i in range(num_physical):
            layer_array_handle.jumpToArrayElement(i)

            compound_handle = layer_array_handle.inputValue()

            # --- 业务逻辑 ---
            if compound_handle.child(self.aWeightsLayerEnabled).asBool():
                w_h_obj = compound_handle.child(self.aWeightsLayer)
                m_h_obj = compound_handle.child(self.aWeightsLayerMask)

                layer_wrapper = cWeightsHandle.WeightsHandle(w_h_obj)
                mask_wrapper = cWeightsHandle.WeightsHandle(m_h_obj)

                if layer_wrapper.is_valid and mask_wrapper.is_valid:
                    cWeightsCoreCython.accumulate_layer_weights(
                        canvas_view,
                        layer_wrapper.get_view(),
                        mask_wrapper.get_view(),
                        self.current_vertex_count,
                        self.current_influences_count,
                    )
                    has_layers_active = True

        # 4. 归一化处理
        if has_layers_active:
            cWeightsCoreCython.normalize_weights(
                canvas_view,
                self.current_vertex_count,
                self.current_influences_count,
            )
        return canvas_view

    def deform(self, dataBlock, geoIter, localToWorldMatrix, multiIndex):

        # envelope
        envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if envelope == 0.0:
            return

        # original raw points view
        ori_pts_view = self._get_original_points_view(dataBlock, multiIndex)
        if ori_pts_view is None:
            return

        # output raw points view
        out_pts_view = self._get_output_points_view(dataBlock, multiIndex)
        if out_pts_view is None:
            return

        # update pool size
        current_influences_count = self._ensure_pool_size(dataBlock)
        if current_influences_count <= 0:
            return

        # get bind matrices view
        bind_view = self._get_bind_matrices_view(dataBlock)
        if bind_view is None:
            return

        # get influences matrices view
        influences_matrices_view = self._get_influences_matrices_view(dataBlock)
        if influences_matrices_view is None:
            return

        # # get weights view
        # weights_handle = cWeightsHandle.WeightsHandle(dataBlock.inputValue(self.aWeights))
        # weights_view = weights_handle.get_view()
        # if (weights_view is None) or (len(weights_view) < self.current_vertex_count * current_influences_count):
        #     return

        final_weights_view = self._compute_blended_weights_inplace(dataBlock)
        if final_weights_view is None:
            return

        # cython core
        cSkinDeformCython.compute_deform_matrices(
            bind_view,
            influences_matrices_view,
            self.rotate_matrices_view,
            self.translate_vectors_view,
        )

        cSkinDeformCython.run_skinning_core(
            ori_pts_view,
            out_pts_view,
            final_weights_view,
            self.rotate_matrices_view,
            self.translate_vectors_view,
            envelope,
        )
