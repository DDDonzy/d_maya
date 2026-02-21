# -*- coding: utf-8 -*-
import maya.OpenMaya as om1
import maya.OpenMayaMPx as ompx
import ctypes
import numpy as np
import contextlib
import time


NODE_NAME = "numpySkinDeformer"
NODE_ID = om1.MTypeId(0x00080033)


class NumpySkinDeformer(ompx.MPxDeformerNode):
    aLayerData = om1.MObject()
    aWeights = om1.MObject()
    aBoneMatrix = om1.MObject()
    aBindPreMatrix = om1.MObject()

    def __init__(self):
        super(NumpySkinDeformer, self).__init__()

        # ============= 动态内存池状态机 ======================
        self.current_max_bones = 0
        self.dynamic_matrices_np = None
        self.bind_pre_matrices_np = None
        self.blended_matrices_np = None
        self.temp_xyz_pool = None
        # =================== DEBUG =====================
        self.compute_count = 0
        self.debug_time_dict = {}

    @contextlib.contextmanager
    def time_decorator(self, label):
        start_time = time.time()
        yield
        end_time = time.time()
        elapsed = end_time - start_time
        if label not in self.debug_time_dict:
            self.debug_time_dict[label] = []
        self.debug_time_dict[label].append(elapsed)

    def print_debug_times(self):
        if not self.debug_time_dict:
            return

        print("\n" + "=" * 80)
        print(f"{'Step Label':<30} | {'Calls':>8} | {'Avg (ms)':>12} | {'FPS':>10}")
        print("-" * 80)

        # 按耗时降序排列，让你一眼看到最慢的步骤
        sorted_items = sorted(self.debug_time_dict.items(), key=lambda x: sum(x[1]) / len(x[1]), reverse=True)

        for label, times in sorted_items:
            avg_s = sum(times) / len(times)
            if avg_s == 0:
                continue

            avg_ms = avg_s * 1000  # 转为毫秒更直观
            fps = 1.0 / avg_s if avg_s > 0 else 0

            # 使用格式化对齐：
            # Label 左对齐 30位
            # Calls 右对齐 8位
            # Avg   右对齐 12位 (保留4位小数)
            # FPS   右对齐 10位 (保留2位小数)
            print(f"{label:<30} | {len(times):>8} | {avg_ms:>12.4f} | {fps:>10.2f}")

        print("=" * 80 + "\n")

    @classmethod
    def nodeInitializer(cls):
        tAttr = om1.MFnTypedAttribute()
        mAttr = om1.MFnMatrixAttribute()
        # 1. 最终权重 (单层 kMesh，纯粹的 V * B 浮点池)
        cls.aWeights = tAttr.create("weightsData", "wtd", om1.MFnData.kMesh)
        cls.addAttribute(cls.aWeights)
        # 2. layerData (多层，未来可扩展为 V * (B+1) 的浮点池，末尾一列为 Mask 权重)
        cls.aLayerData = tAttr.create("layerData", "ld", om1.MFnData.kMesh)
        tAttr.setArray(True)
        tAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aLayerData)
        # 3. 骨骼矩阵
        cls.aBoneMatrix = mAttr.create("boneMatrix", "bm")
        mAttr.setArray(True)
        mAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aBoneMatrix)
        # 4. 骨骼矩阵的 Bind Pose 预变换矩阵
        cls.aBindPreMatrix = mAttr.create("bindPreMatrix", "bpm")
        mAttr.setArray(True)
        mAttr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.aBindPreMatrix)
        # 5. 定义属性影响关系
        outputGeom = ompx.cvar.MPxGeometryFilter_outputGeom
        cls.attributeAffects(cls.aWeights, outputGeom)
        cls.attributeAffects(cls.aBoneMatrix, outputGeom)
        cls.attributeAffects(cls.aBindPreMatrix, outputGeom)

    @staticmethod
    def _get_mesh_raw_numpy(fn_mesh):
        """
        极简底层内存挂载器：直接提取 MFnMesh 的原始指针，返回标准的 (V, 3) 视图。
        """
        num_verts = fn_mesh.numVertices()
        raw_ptr = fn_mesh.getRawPoints()

        ptr_addr = int(raw_ptr)
        c_ptr = ctypes.cast(ptr_addr, ctypes.POINTER(ctypes.c_float))
        return np.ctypeslib.as_array(c_ptr, shape=(num_verts, 3))

    @staticmethod
    def _copy_mmatrix_to_numpy(maya_mat, target_np_array, bone_id):
        target_np_array[bone_id, 0, 0] = maya_mat(0, 0)
        target_np_array[bone_id, 0, 1] = maya_mat(0, 1)
        target_np_array[bone_id, 0, 2] = maya_mat(0, 2)
        target_np_array[bone_id, 0, 3] = maya_mat(0, 3)
        target_np_array[bone_id, 1, 0] = maya_mat(1, 0)
        target_np_array[bone_id, 1, 1] = maya_mat(1, 1)
        target_np_array[bone_id, 1, 2] = maya_mat(1, 2)
        target_np_array[bone_id, 1, 3] = maya_mat(1, 3)
        target_np_array[bone_id, 2, 0] = maya_mat(2, 0)
        target_np_array[bone_id, 2, 1] = maya_mat(2, 1)
        target_np_array[bone_id, 2, 2] = maya_mat(2, 2)
        target_np_array[bone_id, 2, 3] = maya_mat(2, 3)
        target_np_array[bone_id, 3, 0] = maya_mat(3, 0)
        target_np_array[bone_id, 3, 1] = maya_mat(3, 1)
        target_np_array[bone_id, 3, 2] = maya_mat(3, 2)
        target_np_array[bone_id, 3, 3] = maya_mat(3, 3)

    def _get_final_weights(self, dataBlock, num_verts, active_bones_count):
        """
        运行期极速读取：读取 weightsData 属性，重塑为 (V, B) 张量，零计算！
        """
        weight_mesh_obj = dataBlock.inputValue(self.aWeights).asMesh()

        if weight_mesh_obj.isNull():
            return np.zeros((num_verts, active_bones_count), dtype=np.float32)

        fn_w_mesh = om1.MFnMesh(weight_mesh_obj)
        dummy_verts = fn_w_mesh.numVertices()
        expected_floats = num_verts * active_bones_count

        if dummy_verts * 3 >= expected_floats:
            # 1. 提取出 (dummy_verts, 3) 的原始视图
            raw_3d_view = self._get_mesh_raw_numpy(fn_w_mesh)

            # 2. .reshape(-1) 光速展平为 1 维视图 -> 切片 -> 重新塑形为 (V, B)
            return raw_3d_view.reshape(-1)[:expected_floats].reshape((num_verts, active_bones_count))

        return np.zeros((num_verts, active_bones_count), dtype=np.float32)

    def deform(self, dataBlock, geoIter, localToWorldMatrix, multiIndex):
        if self.compute_count >= 100:
            self.print_debug_times()
            self.debug_time_dict.clear()
            self.compute_count = 0
        self.compute_count += 1

        with self.time_decorator("Total Deform Time"):
            # ===================================== Envelope ================================================
            with self.time_decorator("Envelope Fetch"):
                envelope = dataBlock.inputValue(ompx.cvar.MPxGeometryFilter_envelope).asFloat()
                if envelope == 0.0:
                    return
            # ===================================== Original Input ========================================
            with self.time_decorator("Original Mesh Fetch"):
                inputAttr = ompx.cvar.MPxGeometryFilter_input
                inputArrayHandle = dataBlock.outputArrayValue(inputAttr)
                inputArrayHandle.jumpToElement(multiIndex)
                inputGeomObj = inputArrayHandle.outputValue().child(ompx.cvar.MPxGeometryFilter_inputGeom).asMesh()
                if inputGeomObj.isNull():
                    return
                fn_input_mesh = om1.MFnMesh(inputGeomObj)
                num_verts = fn_input_mesh.numVertices()
                ori_np_view = self._get_mesh_raw_numpy(fn_input_mesh)
            # ===================================== output ========================================
            with self.time_decorator("Output Mesh Fetch"):
                outputGeomPlug = ompx.cvar.MPxGeometryFilter_outputGeom
                outputArrayHandle = dataBlock.outputArrayValue(outputGeomPlug)
                outputArrayHandle.jumpToElement(multiIndex)
                outputGeomObj = outputArrayHandle.outputValue().asMesh()
                if outputGeomObj.isNull():
                    return
                fn_output_mesh = om1.MFnMesh(outputGeomObj)
                out_np_view = self._get_mesh_raw_numpy(fn_output_mesh)
            # ===================================== matrix ========================================
            with self.time_decorator("Bone Count & Matrix Fetch"):
                mat_handle = dataBlock.inputArrayValue(self.aBoneMatrix)
                num_bones = mat_handle.elementCount()
                # ===================================== bind Pre matrix ========================================
                bind_handle = dataBlock.inputArrayValue(self.aBindPreMatrix)
                num_binds = bind_handle.elementCount()
                # ========================================= joint index ==================================================
                max_bone_idx = -1
                for i in range(num_bones):
                    mat_handle.jumpToArrayElement(i)
                    idx = mat_handle.elementIndex()
                    if idx > max_bone_idx:
                        max_bone_idx = idx
                for i in range(num_binds):
                    bind_handle.jumpToArrayElement(i)
                    idx = bind_handle.elementIndex()
                    if idx > max_bone_idx:
                        max_bone_idx = idx
                if max_bone_idx == -1:
                    return
                active_bones_count = max_bone_idx + 1
                # ========================================= 如果骨骼数量发生扩张，重新申请扩容的 NumPy 内存池 ==================================================
                if active_bones_count > self.current_max_bones:
                    self.current_max_bones = active_bones_count
                    self.dynamic_matrices_np = np.zeros((self.current_max_bones, 4, 4), dtype=np.float64)
                    self.bind_pre_matrices_np = np.zeros((self.current_max_bones, 4, 4), dtype=np.float64)
                    self.blended_matrices_np = np.zeros((self.current_max_bones, 4, 4), dtype=np.float64)
                # ========================================= 将矩阵数据灌入内存池 ==================================================
                for i in range(num_bones):
                    mat_handle.jumpToArrayElement(i)
                    bone_id = mat_handle.elementIndex()
                    m = mat_handle.inputValue().asMatrix()
                    self._copy_mmatrix_to_numpy(m, self.dynamic_matrices_np, bone_id)
                for i in range(num_binds):
                    bind_handle.jumpToArrayElement(i)
                    bone_id = bind_handle.elementIndex()
                    m = bind_handle.inputValue().asMatrix()
                    self._copy_mmatrix_to_numpy(m, self.bind_pre_matrices_np, bone_id)
            # ========================================= 读取权重数据，零计算 ==================================================
            with self.time_decorator("Weights Fetch"):
                weights = self._get_final_weights(dataBlock, num_verts, active_bones_count)
            # =======================================NumPy 极致向量化蒙皮运算 (预处理)================================================
            with self.time_decorator("Preprocessing for Skinning"):
                # ------------------------------------- Matrix_final = Matrix_bind_pre * Matrix -------------------------------------
                np.matmul(
                    self.bind_pre_matrices_np[:active_bones_count],
                    self.dynamic_matrices_np[:active_bones_count],
                    out=self.blended_matrices_np[:active_bones_count],
                )
            # =======================================NumPy 极致向量化蒙皮运算 (核心)================================================
            with self.time_decorator("Core Skinning Computation"):
                if self.temp_xyz_pool is None or self.temp_xyz_pool.shape[0] != num_verts:
                    self.temp_xyz_pool = np.zeros((num_verts, 3), dtype=np.float32)
                out_np_view.fill(0.0)
                # ------------------------ 旋转缩放矩阵 (B, 3, 3) 和 平移向量 (B, 3) ----------------------
                valid_matrices = self.blended_matrices_np[:active_bones_count]
                M_rot_scale = valid_matrices[:, :3, :3].astype(np.float32)
                M_trans = valid_matrices[:, 3, :3].astype(np.float32)

                for b in range(active_bones_count):
                    w = weights[:, b : b + 1]
                    if not np.any(w):
                        continue
                    # ---------------- (original point * rotation+scale + translation) * w ----------------
                    np.dot(ori_np_view, M_rot_scale[b], out=self.temp_xyz_pool)
                    self.temp_xyz_pool += M_trans[b]
                    self.temp_xyz_pool *= w
                    out_np_view += self.temp_xyz_pool

                if envelope != 1.0:
                    # ------------------------- (B - A) * w + A -------------------------
                    out_np_view -= ori_np_view
                    out_np_view *= envelope
                    out_np_view += ori_np_view


def nodeCreator():
    return ompx.asMPxPtr(NumpySkinDeformer())


def initializePlugin(mobj):
    mplugin = ompx.MFnPlugin(mobj, "TA_Geek", "1.0", "Any")
    mplugin.registerNode(NODE_NAME, NODE_ID, nodeCreator, NumpySkinDeformer.nodeInitializer, ompx.MPxNode.kDeformerNode)


def uninitializePlugin(mobj):
    mplugin = ompx.MFnPlugin(mobj)
    mplugin.deregisterNode(NODE_ID)
