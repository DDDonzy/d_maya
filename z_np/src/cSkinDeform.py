import ctypes

import maya.OpenMaya as om1  # type: ignore
import maya.OpenMayaMPx as ompx  # type: ignore

from .cMemoryView import CMemoryManager
from . import cWeightsHandle as CWH
from . import cSkinDeformCython

from ._cRegistry import GLOBAL_DEFORMER_REGISTRY


class DeformerData:
    """
    变形器内存数据，以视图方式储存所有数据，放到全局变量中。
    变形器的数据不再从mayaAPI获取，直接从这个对象中获取。
    """

    __slots__ = (
        "topology",
        "tri_indices_2D",
        "tri_to_face_map",
        "influences_count",
        "vertex_count",
        "original_rawPoints_mgr",
        "original_rawPoints_mgr2D",
        "output_rawPoints_mgr",
        "output_rawPoints_mgr2D",
        "_influencesMatrix_mgr",
        "_bindPreMatrix_mgr",
        "_rotateMatrix_mgr",
        "_translateVector_mgr",
        "hashCode",
        "mObj",
        "mFnDep",
        "mFnMesh_original",
        "mFnMesh_output",
        "weightsLayer",
    )

    def __init__(self):
        self.vertex_count: int = 0
        self.topology: list[int] = None
        self.tri_indices_2D: CMemoryManager = None
        self.tri_to_face_map: CMemoryManager = None

        # 基本数据
        self.influences_count: int = 0
        self.original_rawPoints_mgr: CMemoryManager = None
        self.original_rawPoints_mgr2D: CMemoryManager = None
        self.output_rawPoints_mgr: CMemoryManager = None
        self.output_rawPoints_mgr2D: CMemoryManager = None

        self._influencesMatrix_mgr: CMemoryManager = None
        self._bindPreMatrix_mgr: CMemoryManager = None
        self._rotateMatrix_mgr: CMemoryManager = None
        self._translateVector_mgr: CMemoryManager = None

        # 缓存中的API类，避免重复调用API
        self.hashCode: str = None
        self.mObj: om1.MObject = None
        self.mFnDep: om1.MFnDependencyNode = None
        self.mFnMesh_original: om1.MFnMesh = None
        self.mFnMesh_output: om1.MFnMesh = None

        self.weightsLayer: dict[int, CWH.WeightsLayerData] = {}
        """ {骨骼index: 权重数据类}"""


class CythonSkinDeformer(ompx.MPxDeformerNode):
    __slots__ = ("DATA",)
    aWeights = om1.MObject()
    aWeightsLayer = om1.MObject()
    aWeightsLayerMask = om1.MObject()
    aWeightsLayerEnabled = om1.MObject()
    aWeightsLayerCompound = om1.MObject()
    aInfluenceMatrix = om1.MObject()
    aBindPreMatrix = om1.MObject()
    aRefresh = om1.MObject()
    """如果这些属性有变化，通知deform，更新权重"""

    def __init__(self):
        super(CythonSkinDeformer, self).__init__()
        self.DATA: DeformerData = DeformerData()
        self.__weights_is_dirty: bool = True
        self.__influencesMatrix_is_dirty: bool = True

    def postConstructor(self):
        # 预先构建变形器需要的API对象，避免重复调用
        self.mObj = self.thisMObject()
        self._refresh_plug = om1.MPlug(self.mObj, self.aRefresh)  # 提前获取 refresh 的plug ，避免api开销
        # 数据储存到全局内存
        self.DATA.mObj = self.mObj
        self.DATA.mFnDep = om1.MFnDependencyNode(self.DATA.mObj)
        self.DATA.hashCode = om1.MObjectHandle(self.DATA.mObj).hashCode()
        # 构建哈西字典，方便在别的区域，直接拿到这个变形器的对象
        GLOBAL_DEFORMER_REGISTRY[self.DATA.hashCode] = self  #

    def setDependentsDirty(self, plug, dirtyPlugArray):
        if plug == self.aRefresh:
            self.__weights_is_dirty = True
        if plug == self.aInfluenceMatrix or plug == self.aBindPreMatrix:
            self.__influencesMatrix_is_dirty = True
        return super(CythonSkinDeformer, self).setDependentsDirty(plug, dirtyPlugArray)

    def preEvaluation(self, context, evaluationNode):
        if context.isNormal():
            if evaluationNode.dirtyPlugExists(self.aInfluenceMatrix) or evaluationNode.dirtyPlugExists(self.aBindPreMatrix):
                self.__influencesMatrix_is_dirty = True
        return super(CythonSkinDeformer, self).preEvaluation(context, evaluationNode)

    def _update_topology_cache(self, mFnMesh: om1.MFnMesh):
        """
        仅在拓扑改变或首次加载时触发
        """
        tri_counts_MIntArray = om1.MIntArray()
        tri_vertex_indices_MIntArray = om1.MIntArray()

        mFnMesh.getTriangles(tri_counts_MIntArray, tri_vertex_indices_MIntArray)

        tri_counts = list(tri_counts_MIntArray)
        tri_vertex_indices = list(tri_vertex_indices_MIntArray)

        flat_tri_mgr = CMemoryManager.from_list(tri_vertex_indices, "i")
        num_tris = len(tri_vertex_indices) // 3

        self.DATA.tri_indices_2D = flat_tri_mgr.reshape((num_tris, 3))

        face_map_list = [0] * num_tris
        current_tri_idx = 0
        for face_id, count in enumerate(tri_counts):
            for _ in range(count):
                face_map_list[current_tri_idx] = face_id
                current_tri_idx += 1

        face_map_mgr = CMemoryManager.from_list(face_map_list, "i")
        self.DATA.tri_to_face_map = face_map_mgr

    def _setDirty(self):
        """
        - 用于笔刷调用，提醒Deform，更新权重
        - 设置自借点自身 “refresh” 属性，refresh 影响 outputGeometry
        """
        self._refresh_plug.setInt(0)
        self.__weights_is_dirty = True

    def deform(self, dataBlock, geoIter, localToWorldMatrix, multiIndex):
        # region ----------- envelope -----------------------------------------------------
        envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
        if envelope == 0.0:
            return
        # endregion

        # region ----------- Influences --------------------------------------------------
        influences_handle = dataBlock.inputArrayValue(self.aInfluenceMatrix)
        influences_count = influences_handle.elementCount()
        if self.DATA.influences_count != influences_count:
            """ 内存骨骼数量 和 maya 骨骼数量不一样，重新分配内存 """
            self.DATA.influences_count = influences_count
            self.DATA._influencesMatrix_mgr = CMemoryManager.allocate("d", (influences_count, 16))
            self.DATA._rotateMatrix_mgr = CMemoryManager.allocate("f", (influences_count, 9))
            self.DATA._translateVector_mgr = CMemoryManager.allocate("f", (influences_count, 3))
            """填充为单位矩阵，后续可以考虑删掉/优化"""
            for b in range(influences_count):
                for i in range(16):
                    self.DATA._influencesMatrix_mgr.view[b, i] = 1.0 if (i % 5 == 0) else 0.0
        # endregion

        # region ----------- Get Raw Points --------------------------------------------
        _laster_numVertex = self.DATA.vertex_count
        self.DATA.mFnMesh_original, self.DATA.original_rawPoints_mgr = self._get_original_points(dataBlock, multiIndex)
        if _laster_numVertex != self.DATA.vertex_count:
            self._update_topology_cache(self.DATA.mFnMesh_original)

        self.DATA.mFnMesh_output, self.DATA.output_rawPoints_mgr = self._get_output_points(dataBlock, multiIndex)
        self.DATA.original_rawPoints_mgr2D = self.DATA.original_rawPoints_mgr.reshape((self.DATA.vertex_count, 3))
        self.DATA.output_rawPoints_mgr2D = self.DATA.output_rawPoints_mgr.reshape((self.DATA.vertex_count, 3))

        # endregion

        # region ----------- Bind Pre Matrix -------------------------------------------
        if self.__influencesMatrix_is_dirty:
            bind_data_obj = dataBlock.inputValue(self.aBindPreMatrix).data()
            if bind_data_obj is None or bind_data_obj.isNull():
                return
            fn_bind_array = om1.MFnMatrixArrayData(bind_data_obj)
            bind_m_array = fn_bind_array.array()
            length = bind_m_array.length()
            if length == 0:
                return
            addr_base = int(bind_m_array[0].this)
            self.DATA._bindPreMatrix_mgr = CMemoryManager.from_ptr(addr_base, "d", (length, 16))
            # endregion

            # region ----------- Influences Matrix -----------------------------------------
            if self.DATA.influences_count <= 0:
                return
            matrix_handle = dataBlock.inputArrayValue(self.aInfluenceMatrix)
            dest_base_addr = self.DATA._influencesMatrix_mgr.ptr_addr
            for i in range(self.DATA.influences_count):
                matrix_handle.jumpToArrayElement(i)
                influence_idx = matrix_handle.elementIndex()

                mMatrix = matrix_handle.inputValue().asMatrix()
                src_addr = int(mMatrix.this)

                dest_addr = dest_base_addr + (influence_idx * 128)  # (4*4)*8
                ctypes.memmove(dest_addr, src_addr, 128)  # (4*4)*8
        # endregion

        # region ----------- Weights --------------------------------------------------
        # weights
        if self.__weights_is_dirty:
            self._update_weightsLayer(dataBlock)
        if self.DATA.weightsLayer[-1].weightsHandle.is_valid is False:
            return
        # endregion

        cSkinDeformCython.compute_deform_matrices(
            self.DATA._bindPreMatrix_mgr.view,
            self.DATA._influencesMatrix_mgr.view,
            self.DATA._rotateMatrix_mgr.view,
            self.DATA._translateVector_mgr.view,
        )

        cSkinDeformCython.run_skinning_core(
            self.DATA.original_rawPoints_mgr.view,
            self.DATA.output_rawPoints_mgr.view,
            self.DATA.weightsLayer[-1].weightsHandle.memory.view,
            self.DATA._rotateMatrix_mgr.view,
            self.DATA._translateVector_mgr.view,
            envelope,
        )
        self.__weights_is_dirty = False
        self.__influencesMatrix_is_dirty = False

    def _get_original_points(self, dataBlock: om1.MDataBlock, multiIndex) -> CMemoryManager:
        """获取maya original raw points 内存视图"""
        inputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_input)
        inputArrayHandle.jumpToElement(multiIndex)
        inputGeomObj = inputArrayHandle.outputValue().child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
        if inputGeomObj.isNull():
            return None

        fnMesh = om1.MFnMesh(inputGeomObj)
        vertex_count = fnMesh.numVertices()
        _ptr = int(fnMesh.getRawPoints())

        self.DATA.mFnMesh_original = fnMesh
        self.DATA.vertex_count = vertex_count

        return fnMesh, CMemoryManager.from_ptr(_ptr, "f", (vertex_count * 3,))

    def _get_output_points(self, dataBlock: om1.MDataBlock, multiIndex) -> CMemoryManager:
        """获取 maya output geometry raw points 内存视图"""
        outputArrayHandle = dataBlock.outputArrayValue(ompx.cvar.MPxGeometryFilter_outputGeom)
        outputArrayHandle.jumpToElement(multiIndex)
        outputGeomObj = outputArrayHandle.outputValue().asMesh()
        if outputGeomObj.isNull():
            return None

        fnMesh = om1.MFnMesh(outputGeomObj)
        _addr = int(fnMesh.getRawPoints())
        vertex_count = fnMesh.numVertices()

        self.DATA.mFnMesh_output = fnMesh
        return fnMesh, CMemoryManager.from_ptr(_addr, "f", (vertex_count * 3,))

    def _update_weightsLayer(self, dataBlock: om1.MDataBlock):
        # weights
        weights_handle = CWH.WeightsHandle.from_data_handle(dataBlock.inputValue(self.aWeights))
        self.DATA.weightsLayer[-1] = CWH.WeightsLayerData(-1, True, weights_handle, None)
        # layers
        inputArrayHandle: om1.MArrayDataHandle = dataBlock.inputArrayValue(self.aWeightsLayerCompound)
        for i in range(inputArrayHandle.elementCount()):
            inputArrayHandle.jumpToArrayElement(i)
            element_handle: om1.MDataHandle = inputArrayHandle.inputValue()
            weights_handle = CWH.WeightsHandle.from_data_handle(element_handle.child(self.aWeightsLayer))
            mask_handle = CWH.WeightsHandle.from_data_handle(element_handle.child(self.aWeightsLayerMask))
            enabled_handle: om1.MDataHandle = element_handle.child(self.aWeightsLayerEnabled)
            self.DATA.weightsLayer[i] = CWH.WeightsLayerData(i, enabled_handle.asBool(), weights_handle, mask_handle)

    @classmethod
    def nodeInitializer(cls):
        tAttr = om1.MFnTypedAttribute()
        mAttr = om1.MFnMatrixAttribute()
        nAttr = om1.MFnNumericAttribute()
        cAttr = om1.MFnCompoundAttribute()

        cls.aWeights = tAttr.create("cWeights", "cw", om1.MFnData.kMesh)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aWeights)

        cls.aInfluenceMatrix = mAttr.create("matrix", "bm")
        mAttr.setArray(True)
        mAttr.setHidden(True)
        mAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aInfluenceMatrix)

        cls.aBindPreMatrix = tAttr.create("bindPreMatrixArray", "bpm", om1.MFnData.kMatrixArray)
        tAttr.setHidden(True)
        cls.addAttribute(cls.aBindPreMatrix)

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

        cls.aRefresh = nAttr.create("refresh", "rf", om1.MFnNumericData.kInt, 0)
        nAttr.setStorable(False)
        nAttr.setHidden(True)
        nAttr.setKeyable(False)
        nAttr.setWritable(False)
        nAttr.setReadable(True)
        cls.addAttribute(cls.aRefresh)

        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom

        cls.attributeAffects(cls.aWeights, cls.aRefresh)
        cls.attributeAffects(cls.aInfluenceMatrix, cls.aRefresh)
        cls.attributeAffects(cls.aBindPreMatrix, cls.aRefresh)
        cls.attributeAffects(cls.aWeightsLayerCompound, cls.aRefresh)

        cls.attributeAffects(cls.aWeights, outputGeom)
        cls.attributeAffects(cls.aInfluenceMatrix, outputGeom)
        cls.attributeAffects(cls.aBindPreMatrix, outputGeom)
        cls.attributeAffects(cls.aWeightsLayerCompound, outputGeom)

        cls.attributeAffects(cls.aRefresh, outputGeom)
