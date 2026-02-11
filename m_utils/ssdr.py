# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import numpy as np
import math
import traceback
import pprint as pp


CONFIG = {
    "REST_MESH": "pCube1",
    "TARGET_MESH": "pCube2",
    "SKIN_NODE": "skinCluster1",
    "BONES": cmds.skinCluster("skinCluster1", q=1, inf=1),
    "ITERATIONS": 5,
    "TOLERANCE": 1e-5,
    "WEIGHT_THR": 0.001,  # 既然使用了加权，阈值可以设小一点，让更多点参与贡献但低权重影响极小
    "MAX_ANGLE": 60.0,
}


def get_dag_path(name):
    """通过名字获取 DAG Path"""
    try:
        sel = om.MSelectionList()
        sel.add(name)
        return sel.getDagPath(0)
    except Exception:
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
    # 钳制数值防止 acos 越界
    val = max(min(q_diff.w, 1.0), -1.0)
    angle_rad = 2.0 * math.acos(val)
    angle_deg = math.degrees(angle_rad)
    if angle_deg <= max_deg:
        return mat_current
    t = math.radians(max_deg) / angle_rad

    # Slerp 插值回原始角度
    q_clamped = om.MQuaternion.slerp(q_rest, q_curr, t)
    tm_final = om.MTransformationMatrix(mat_current)
    tm_final.setRotation(q_clamped)
    return tm_final.asMatrix()


def run_solver_weighted():
    print(f">>> 开始加权计算 (SkinCluster: {CONFIG['SKIN_NODE']})...")

    # 1. 初始化对象与数据
    rest_dag = get_dag_path(CONFIG["REST_MESH"])
    target_dag = get_dag_path(CONFIG["TARGET_MESH"])

    try:
        sel_skin = om.MSelectionList()
        sel_skin.add(CONFIG["SKIN_NODE"])
        skin_fn = oma.MFnSkinCluster(sel_skin.getDependNode(0))
        rest_fn = om.MFnMesh(rest_dag)
        target_fn = om.MFnMesh(target_dag)
    except:
        cmds.error("初始化失败，请检查模型名称和蒙皮节点。")
        return

    # 顶点数
    num_verts = rest_fn.numVertices
    # 雕刻模型点位置
    p_target_all = np.array(target_fn.getPoints(om.MSpace.kObject))[:, :3]
    # 蒙皮骨骼和对应的index
    inf_map = {name: idx for idx, name in enumerate(cmds.skinCluster(CONFIG["SKIN_NODE"], q=1, inf=1))}
    # maya 权重
    weights_flat, _ = skin_fn.getWeights(rest_dag, om.MObject())
    # maya 权重转 np，按骨骼序列排序
    weights_all = np.array(weights_flat).reshape(num_verts, -1)
    # bind pose 矩阵
    rest_matrices = get_rest_matrices(CONFIG["BONES"])

    # 2. 预计算骨骼数据 (加入权重数组缓存)
    bone_cache = []
    for bone_name in CONFIG["BONES"]:
        col_idx = inf_map.get(bone_name, -1)
        if col_idx == -1 or bone_name not in rest_matrices:
            # 检测骨骼是否在蒙皮中
            continue

        indices = np.where(weights_all[:, col_idx] > CONFIG["WEIGHT_THR"])[0]  # 当前骨骼影响点的idx
        if len(indices) < 3:
            # 只有影响点数大于3个点的骨骼才可以svd计算
            continue

        # 缓存该骨骼对应的权重，并进行归一化（可选，但推荐）
        w = weights_all[indices, col_idx]

        bone_cache.append({
            "name": bone_name,  # 骨骼名称
            "indices": indices,  # 当前骨骼点的点序号
            "W": w[:, np.newaxis],  # 当前骨骼影响点的权重，变成 (N, 1) 方便 numpy 广播运算
            "Q": p_target_all[indices],  # 当前骨骼影响的点，对应雕刻模型的位置
        })
    pp.pprint(bone_cache)

    # 3. 迭代求解器
    try:
        for it in range(CONFIG["ITERATIONS"]):
            max_move = 0.0
            p_current_all = np.array(rest_fn.getPoints(om.MSpace.kObject))[:, :3]

            for data in bone_cache:
                bone_name, indices, Q, W = data["name"], data["indices"], data["Q"], data["W"]
                P = p_current_all[indices]

                # --- 加权 SVD 核心步骤 ---
                # 1. 计算加权重心
                sum_w = np.sum(W)
                cen_P = np.sum(P * W, axis=0) / sum_w
                cen_Q = np.sum(Q * W, axis=0) / sum_w

                # 2. 去中心化
                P_centered = P - cen_P
                Q_centered = Q - cen_Q

                # 3. 构建加权协方差矩阵 H = (P*W)^T * Q
                # W 是 (N, 1), P_centered 是 (N, 3), Q_centered 是 (N, 3)
                H = np.dot((P_centered * W).T, Q_centered)

                # 4. SVD 求解旋转
                U, S, Vt = np.linalg.svd(H)
                R_trans = np.dot(Vt.T, U.T).T  # 保持原代码的转置逻辑适配 Maya

                if np.linalg.det(R_trans.T) < 0:  # 修正反射
                    Vt[2, :] *= -1
                    R_trans = np.dot(Vt.T, U.T).T

                # --- 构造 Maya 矩阵 ---
                mat_list = [R_trans[0, 0], R_trans[0, 1], R_trans[0, 2], 0.0, R_trans[1, 0], R_trans[1, 1], R_trans[1, 2], 0.0, R_trans[2, 0], R_trans[2, 1], R_trans[2, 2], 0.0, 0.0, 0.0, 0.0, 1.0]
                mat_rot = om.MMatrix(mat_list)

                # 5. 计算加权位移 t = cen_Q - R * cen_P
                cp_rot = om.MPoint(cen_P) * mat_rot
                t_vec = om.MVector(cen_Q) - om.MVector(cp_rot)

                mat_list[12], mat_list[13], mat_list[14] = t_vec.x, t_vec.y, t_vec.z
                mat_delta = om.MMatrix(mat_list)

                # --- 应用变换与约束 ---
                bone_fn = om.MFnTransform(get_dag_path(bone_name))
                mat_new = bone_fn.transformation().asMatrix() * mat_delta
                mat_final = constrain_angle(mat_new, rest_matrices[bone_name], CONFIG["MAX_ANGLE"])

                tm_final = om.MTransformationMatrix(mat_final)
                bone_fn.setTranslation(tm_final.translation(om.MSpace.kWorld), om.MSpace.kWorld)
                bone_fn.setRotation(tm_final.rotation(True), om.MSpace.kWorld)

                max_move = max(max_move, t_vec.length())

            if max_move < CONFIG["TOLERANCE"]:
                print(f"迭代 {it + 1}: 已收敛。")
                break
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    finally:
        cmds.refresh()
        print(">>> 加权计算完成")


if __name__ == "__main__":
    run_solver_weighted()
