# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import numpy as np
import math

# ==================== 配置区域 (Config) ====================
CONFIG = {
    # 场景对象名称
    "REST_MESH": "Rest_Mesh",  # 原始 T-Pose 模型
    "TARGET_MESH": "Sculpt_Mesh",  # 雕刻好的目标模型
    "SKIN_NODE": "skinCluster1",  # [手动输入] 蒙皮节点名称
    # 需要计算的骨骼列表
    "BONES": ["Bone_Root", "Bone_Top"],
    # 求解参数
    "ITERATIONS": 10,  # 迭代次数 (无阻尼模式下通常5-10次即可)
    "TOLERANCE": 1e-5,  # 收敛精度
    "WEIGHT_THR": 0.4,  # 权重阈值
    # 限制参数
    "MAX_ANGLE": 60.0,  # [全局限制] 最大允许旋转角度
}
# ==========================================================


def get_dag_path(name):
    """通过名字获取 DAG Path"""
    try:
        sel = om.MSelectionList()
        sel.add(name)
        return sel.getDagPath(0)
    except:
        return None


def get_rest_matrices(bone_names):
    """记录初始矩阵 (用于角度限制参考)"""
    matrices = {}
    for name in bone_names:
        dag = get_dag_path(name)
        if dag:
            fn = om.MFnTransform(dag)
            matrices[name] = fn.transformation().asMatrix()
    return matrices


def get_influence_index(skin_fn, bone_name):
    """获取骨骼索引"""
    influences = skin_fn.influenceObjects()
    for i in range(len(influences)):
        inf_name = influences[i].partialPathName()
        if bone_name == inf_name or bone_name == inf_name.split("|")[-1]:
            return i
    return -1


def constrain_angle(mat_current, mat_rest, max_deg):
    """全局角度限制"""
    tm_curr = om.MTransformationMatrix(mat_current)
    tm_rest = om.MTransformationMatrix(mat_rest)

    q_curr = tm_curr.rotation(True)
    q_rest = tm_rest.rotation(True)

    q_diff = q_curr * q_rest.inverse()
    if q_diff.w < 0:
        q_diff.negateIt()
        q_curr.negateIt()

    val = max(min(q_diff.w, 1.0), -1.0)
    angle_rad = 2.0 * math.acos(val)
    angle_deg = math.degrees(angle_rad)

    if angle_deg <= max_deg:
        return mat_current

    t = math.radians(max_deg) / angle_rad
    q_clamped = om.MQuaternion.slerp(q_rest, q_curr, t)

    tm_final = om.MTransformationMatrix(mat_current)
    tm_final.setRotation(q_clamped)
    return tm_final.asMatrix()


def run_solver():
    print(f">>> 开始计算 (SkinCluster: {CONFIG['SKIN_NODE']})...")

    # 1. 初始化对象
    rest_dag = get_dag_path(CONFIG["REST_MESH"])
    target_dag = get_dag_path(CONFIG["TARGET_MESH"])

    # 获取手动指定的 SkinCluster
    try:
        sel_skin = om.MSelectionList()
        sel_skin.add(CONFIG["SKIN_NODE"])
        skin_node = sel_skin.getDependNode(0)
        skin_fn = oma.MFnSkinCluster(skin_node)
    except:
        cmds.error(f"初始化失败：找不到蒙皮节点 '{CONFIG['SKIN_NODE']}'，请检查名字是否正确。")
        return

    if not (rest_dag and target_dag):
        cmds.error(f"初始化失败：找不到模型。")
        return

    rest_fn = om.MFnMesh(rest_dag)
    target_fn = om.MFnMesh(target_dag)

    # 2. 数据准备
    num_verts = rest_fn.numVertices
    p_target = np.array(target_fn.getPoints(om.MSpace.kWorld))[:, :3]

    weights_flat, _ = skin_fn.getWeights(rest_dag, om.MObject())
    # 自动 Reshape 保护
    try:
        num_influences = len(skin_fn.influenceObjects())
        weights_all = np.array(weights_flat).reshape(num_verts, num_influences)
    except:
        weights_all = np.array(weights_flat).reshape(num_verts, -1)

    rest_matrices = get_rest_matrices(CONFIG["BONES"])

    # 3. 迭代
    cmds.undoInfo(openChunk=True)
    try:
        for it in range(CONFIG["ITERATIONS"]):
            max_move = 0.0
            p_current = np.array(rest_fn.getPoints(om.MSpace.kWorld))[:, :3]

            for bone_name in CONFIG["BONES"]:
                if bone_name not in rest_matrices:
                    continue

                col_idx = get_influence_index(skin_fn, bone_name)
                if col_idx == -1:
                    continue

                indices = np.where(weights_all[:, col_idx] > CONFIG["WEIGHT_THR"])[0]
                if len(indices) < 3:
                    continue

                P = p_current[indices]
                Q = p_target[indices]

                # SVD 核心
                cen_P, cen_Q = np.mean(P, axis=0), np.mean(Q, axis=0)
                H = np.dot((P - cen_P).T, (Q - cen_Q))
                U, S, Vt = np.linalg.svd(H)
                R = np.dot(Vt.T, U.T)

                if np.linalg.det(R) < 0:
                    Vt[2, :] *= -1
                    R = np.dot(Vt.T, U.T)

                # Numpy -> Maya Matrix
                R_maya = R.T
                mat_list = [R_maya[0, 0], R_maya[0, 1], R_maya[0, 2], 0.0, R_maya[1, 0], R_maya[1, 1], R_maya[1, 2], 0.0, R_maya[2, 0], R_maya[2, 1], R_maya[2, 2], 0.0, 0.0, 0.0, 0.0, 1.0]
                mat_rot = om.MMatrix(mat_list)

                # 计算位移 (无阻尼)
                cp_rot = om.MPoint(cen_P) * mat_rot
                t_vec = om.MVector(cen_Q) - om.MVector(cp_rot)

                mat_list[12], mat_list[13], mat_list[14] = t_vec.x, t_vec.y, t_vec.z
                mat_delta = om.MMatrix(mat_list)

                # 应用
                bone_dag = get_dag_path(bone_name)
                bone_fn = om.MFnTransform(bone_dag)

                mat_new = bone_fn.transformation().asMatrix() * mat_delta

                # 全局限制
                mat_final = constrain_angle(mat_new, rest_matrices[bone_name], CONFIG["MAX_ANGLE"])

                tm_final = om.MTransformationMatrix(mat_final)
                bone_fn.setTranslation(tm_final.translation(om.MSpace.kWorld), om.MSpace.kWorld)
                bone_fn.setRotation(tm_final.rotation(True), om.MSpace.kWorld)

                move_dist = t_vec.length()
                if move_dist > max_move:
                    max_move = move_dist

            if max_move < CONFIG["TOLERANCE"]:
                print(f"迭代 {it + 1}: 完美收敛。")
                break

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        cmds.undoInfo(closeChunk=True)
        cmds.refresh()
        print(">>> 计算完成")


if __name__ == "__main__":
    run_solver()
