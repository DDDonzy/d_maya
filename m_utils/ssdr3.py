from maya import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

import numpy as np

import m_utils.apiundo as apiundo
from m_utils.dag.getHistory import get_history


class SSDR:
    """使用加权SVD求解器调整骨骼的皮肤变形工具"""

    def __init__(
        self,
        skin_mesh,
        sculpt_mesh,
        weight_tolerance=0.001,
        user_input_influences: list[str] | None = None,
    ):
        """初始化SSDR求解器

        Args:
            skin_mesh (str): 蒙皮网格名称
            sculpt_mesh (str): 目标网格名称
            weight_tolerance (float): 权重阈值, 低于此值的影响忽略
            user_input_influences (list[str] | None): 用户指定的影响节点列表, 如果提供则只求解这些节点, 否则求解所有影响节点
        """
        self.skin_mesh_name = skin_mesh
        self.sculpt_mesh_name = sculpt_mesh
        self.weight_tolerance = weight_tolerance
        self.user_input_influences = user_input_influences

        # 数据缓存
        self.skin_dag = None
        self.sculpt_dag = None
        self.fn_skin = None
        self.fn_sculpt = None

        self.orig_points = None
        self.sculpt_points = None
        self.weights = None
        self.bind_pre_matrices = None
        self.influences = None
        self.influences_world_matrices = None
        self.num_influences = 0
        self.active_influences = []

        self._initialize()

    def _get_dagPath(self, node_name):
        """获取节点的DAG路径"""
        sel = om.MSelectionList()
        sel.add(node_name)
        return sel.getDagPath(0)

    def _initialize(self):
        """初始化所有数据和缓存"""
        # 获取对象
        self.skin_dag = self._get_dagPath(self.skin_mesh_name)
        self.sculpt_dag = self._get_dagPath(self.sculpt_mesh_name)

        skin_node = get_history(self.skin_mesh_name, type="skinCluster")[0]
        m_sel = om.MSelectionList()
        m_sel.add(skin_node)
        self.fn_skin = oma.MFnSkinCluster(m_sel.getDependNode(0))
        self.fn_sculpt = om.MFnMesh(self.sculpt_dag)

        # 获取网格点
        self.sculpt_points = np.array(self.fn_sculpt.getPoints(om.MSpace.kObject))[:, :3]

        # 获取骨骼影响和权重
        self.influences = self.fn_skin.influenceObjects()
        self.num_influences = len(self.influences)
        weights_flat, _ = self.fn_skin.getWeights(self.skin_dag, om.MObject())
        self.weights = np.array(weights_flat).reshape(-1, self.num_influences)

        # 获取bindPre矩阵和原始点
        plug_bind = self.fn_skin.findPlug("bindPreMatrix", False)
        plug_orig = self.fn_skin.findPlug("originalGeometry", False).elementByLogicalIndex(0)
        self.orig_points = np.array(om.MFnMesh(plug_orig.asMObject()).getPoints(om.MSpace.kObject))[:, :3]

        # 初始化numpy数据
        self._get_influence_matrices(plug_bind)
        self._get_active_influences()

    def _get_influence_matrices(self, plug_bind):
        """设置所有影响节点的矩阵"""
        self.bind_pre_matrices = np.zeros((self.num_influences, 4, 4))
        self.influences_world_matrices = np.zeros((self.num_influences, 4, 4))

        for inf_idx, inf_dag in enumerate(self.influences):
            # Bind Pre Matrix
            m_obj = plug_bind.elementByLogicalIndex(inf_idx).asMObject()
            self.bind_pre_matrices[inf_idx] = np.array(om.MFnMatrixData(m_obj).matrix()).reshape(4, 4)
            # World Matrix
            self.influences_world_matrices[inf_idx] = np.array(inf_dag.inclusiveMatrix()).reshape(4, 4)

    def _get_active_influences(self):
        """筛选出需要求解的影响节点（影响顶点数>=3）"""
        self.active_influences = []
        filleter = bool(self.user_input_influences)

        for inf_idx, inf_dag in enumerate(self.influences):
            if filleter and inf_dag.partialPathName() not in self.user_input_influences:
                continue

            affected_vertices = np.where(self.weights[:, inf_idx] > self.weight_tolerance)[0]

            if len(affected_vertices) < 3:
                continue

            inf_fn = om.MFnTransform(inf_dag)
            self.active_influences.append(
                {
                    "index": inf_idx,
                    "dag": inf_dag,
                    "transform": inf_fn,
                    "base_xform": inf_fn.transformation(),
                    "vert_indices": affected_vertices,
                    "vert_weights": self.weights[affected_vertices, inf_idx][:, np.newaxis],
                    "sculpt_points": self.sculpt_points[affected_vertices],
                }
            )

    def calculate_skin_points(self):
        """使用当前骨骼矩阵计算皮肤网格点位置

        Returns:
            np.ndarray: 变形后的网格点，形状 (num_vertices, 3)
        """
        joint_transforms = (self.bind_pre_matrices @ self.influences_world_matrices).reshape(self.num_influences, 16)
        skin_matrices = (self.weights @ joint_transforms).reshape(-1, 4, 4)
        raw_points_h = np.c_[self.orig_points, np.ones(len(self.orig_points))]
        deformed_h = np.einsum("vk,vkl->vl", raw_points_h, skin_matrices)
        return deformed_h[:, :3]

    def solve_iteration(self):
        """执行一次迭代求解"""
        curr_skin_points = self.calculate_skin_points()

        for data in self.active_influences:
            idx = data["index"]
            W = data["vert_weights"]
            src_pts = curr_skin_points[data["vert_indices"]]
            dst_pts = data["sculpt_points"]

            w_sum = np.sum(W)
            if w_sum < 1e-6:
                continue

            # 计算加权重心
            center_src = np.sum(src_pts * W, axis=0) / w_sum
            center_dst = np.sum(dst_pts * W, axis=0) / w_sum

            # 去中心化
            X = src_pts - center_src
            Y = dst_pts - center_dst

            # 加权SVD
            H = (X * W).T @ Y
            U, _, Vt = np.linalg.svd(H)
            R = U @ Vt

            # 修正反射
            if np.linalg.det(R) < 0:
                Vt[2, :] *= -1
                R = U @ Vt

            # 计算平移
            T = center_dst - center_src @ R

            # 构造delta矩阵
            delta_mat = np.eye(4)
            delta_mat[:3, :3] = R
            delta_mat[3, :3] = T

            # 更新世界矩阵
            self.influences_world_matrices[idx] = self.influences_world_matrices[idx] @ delta_mat

            # Debug
            # self.apply_to_scene()

    def solve(self, iterations):
        """运行指定次数的求解迭代

        Args:
            iterations (int): 迭代次数
        """
        print(f">>> 开始SSDR求解 ({self.skin_mesh_name})  共{iterations}次迭代")

        for iter_idx in range(iterations):
            print(f">>> 迭代 {iter_idx + 1}/{iterations}")
            self.solve_iteration()

        print(">>> 求解完成")

    @staticmethod
    def apply_to_scene_replace_object(name):
        return name + "_ssdr"

    def apply_to_scene(self, replace_object_func=None):
        """将求解结果应用到场景（带undo/redo），支持对象替换"""

        # 1. 构建执行计划：存储 (目标对象Transform, 新矩阵, 旧矩阵)
        execution_plan = []

        for data in self.active_influences:
            orig_dag = data["dag"]
            world_mat = self.influences_world_matrices[data["index"]]

            # 确定目标对象名称
            target_name = replace_object_func(orig_dag.partialPathName()) if replace_object_func else orig_dag.partialPathName()

            if not cmds.objExists(target_name):
                continue

            # 获取目标 DAG
            sel = om.MSelectionList()
            sel.add(target_name)
            target_dag = sel.getDagPath(0)
            target_fn = om.MFnTransform(target_dag)

            # 2. 计算：使用目标对象自身的父级逆矩阵 (修复空间偏移 Bug)
            parent_inv_mat = target_dag.exclusiveMatrixInverse()
            target_local_mat = om.MMatrix(world_mat) * parent_inv_mat

            # 缓存新旧矩阵
            old_mat = target_fn.transformation()
            new_mat = om.MTransformationMatrix(target_local_mat)

            execution_plan.append({"fn": target_fn, "new": new_mat, "old": old_mat})

        # 3. 定义 redo 和 undo
        def redo():
            for item in execution_plan:
                item["fn"].setTransformation(item["new"])

        def undo():
            for item in execution_plan:
                item["fn"].setTransformation(item["old"])

        # 4. 执行
        try:
            redo()
            apiundo.commit(redo, undo)
        except Exception as e:
            print(f"应用失败: {e}")

    def run(self, iterations=20):
        """
        完整的求解流程：求解+应用到场景

        Args:
            iterations (int): 迭代次数，默认20
        """
        self.solve(iterations)
        self.apply_to_scene(self.apply_to_scene_replace_object)


# 使用示例
if __name__ == "__main__":
    ssdr = SSDR(
        skin_mesh="M_Head_base",
        sculpt_mesh="M_Head_base1",
        weight_tolerance=0.001,
    )
    ssdr.run(iterations=20)
