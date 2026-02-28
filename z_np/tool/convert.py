import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.OpenMaya as om1  # type: ignore #
import maya.api.OpenMayaAnim as oma2
import ctypes
import numpy as np

from m_utils.time_decorator import time_decorator


# =====================================================================
# 函数 1：提取 SkinCluster 权重与骨骼数量 (使用 API 2.0)
# =====================================================================
@time_decorator
def get_skinWeights(skin_cluster_name):
    """
    输入: skinCluster 名字 (字符串)
    输出: 一维权重数组 (tuple), 骨骼数量 (int), 原生骨骼对象列表 (MDagPathArray)
    """

    # get mesh
    mesh = cmds.skinCluster(skin_cluster_name, q=1, g=1)[0]
    sel = om2.MGlobal.getSelectionListByName(skin_cluster_name)
    sel.add(mesh)
    skin_dep = sel.getDependNode(0)
    skin_fn = oma2.MFnSkinCluster(skin_dep)
    mesh_dag = sel.getDagPath(1)

    # 获取当前蒙皮绑定的几何体路径
    geom_paths = skin_fn.getOutputGeometry()

    if not geom_paths:
        raise RuntimeError(f"未找到 {skin_cluster_name} 绑定的几何体")

    # 获取骨骼列表与数量
    inf_dags = skin_fn.influenceObjects()
    num_bones = len(inf_dags)

    # 提取所有顶点的权重 (扁平化 Tuple)
    weights_tuple, _ = skin_fn.getWeights(mesh_dag, om2.MObject())

    return weights_tuple, num_bones


# =====================================================================
# 函数 2：一维权重转为 XYZ Point Float Array (Numpy Nx3 结构)
# =====================================================================


@time_decorator
def weights_to_xyz(weights_1d):
    """
    输入: 一维权重数组 (Tuple 或 List)
    输出: Numpy (N, 3) 形状的浮点数组
    说明: 自动将权重补齐为 3 的倍数，用于映射到 Maya 的点坐标，无效占位设置为 -1.0
    """
    weights_np = np.array(weights_1d, dtype=np.float32)
    total_floats = len(weights_np)

    # 计算需要的虚拟点数量（每个点占3个float，且至少保证3个点以构成面）
    num_points = int(np.ceil(total_floats / 3.0))
    num_points = max(3, num_points)

    # 💡 核心修改：使用 np.full 创建一个全 -1.0 的数组，而不是全 0
    padded_flat = np.full(num_points * 3, -1.0, dtype=np.float32)

    # 将实际权重填入前面
    padded_flat[:total_floats] = weights_np

    # 变形成 (N, 3) 形状的二维数组
    xyz_points_array = padded_flat.reshape((num_points, 3))

    # 如果你主流程中还需要 total_floats 可以一起 return，
    # 但根据你的解耦思路，这里我们只 return 数组即可。
    return xyz_points_array


@time_decorator
def xyz_to_weights(xyz_points_array):
    """
    输入: Numpy (N, 3) 形状的浮点数组
    输出: 去除补齐的 -1.0 后的一维权重数组 (Numpy 1D array)
    说明: 自动丢弃所有占位符，无需传入 valid_length
    """
    # 展平回一维数组
    flat_weights = np.array(xyz_points_array, dtype=np.float32).flatten()

    # 💡 核心修改：利用权重 >= 0 的特性，直接用布尔索引一键过滤！
    # 速度极快，且完美按原顺序保留了所有的真实权重
    valid_weights = flat_weights[flat_weights >= 0.0]

    return valid_weights


# =====================================================================
# 函数 4：为节点的 MatrixArray 属性赋值 (使用 API 2.0)
# =====================================================================
@time_decorator
def set_bindMatrixArray(node_name, attr_name, matrix_list):
    """
    输入: 目标节点名 (str), 属性名 (str, 例如 "bindPreMatrixArray"), 矩阵列表 (list of 16-floats 或 om2.MMatrix)
    输出: None
    """
    sel = om2.MGlobal.getSelectionListByName(node_name)
    dep_node = sel.getDependNode(0)
    fn_node = om2.MFnDependencyNode(dep_node)
    # 寻找目标属性 Plug
    plug = fn_node.findPlug(attr_name, False)

    # 构造 MMatrixArray
    mat_array = om2.MMatrixArray()
    for mat in matrix_list:
        if isinstance(mat, om2.MMatrix):
            mat_array.append(mat)
        else:
            # 如果传入的是 16 个浮点数的 List，转为 MMatrix
            mat_array.append(om2.MMatrix(mat))

    # 创建 MatrixArray 数据对象并写入 Plug
    mat_data = om2.MFnMatrixArrayData().create(mat_array)
    plug.setMObject(mat_data)


# =====================================================================
# 函数 5：设置权重到 kMesh 属性上 (零拷贝直写)
# =====================================================================
@time_decorator
def set_xyz_to_mesh_attr(node_name, attr_name, xyz_points_array):
    """
    输入: 节点名(str), 属性名(str), Numpy (N, 3) 形状的浮点数组
    输出: None
    """
    num_points = xyz_points_array.shape[0]

    # 1. 构造骗过 Maya 的最小拓扑 (至少 3 个点连成 1 个面)
    v_count = om1.MIntArray()
    v_list = om1.MIntArray()
    if num_points >= 3:
        v_count.append(3)
        v_list.append(0)
        v_list.append(1)
        v_list.append(2)

    base_pts = om1.MFloatPointArray()
    base_pts.setLength(num_points)

    # 2. 创建底层的 MFnMeshData 和 MFnMesh
    mesh_data_obj = om1.MFnMeshData().create()
    new_mesh_fn = om1.MFnMesh()
    new_mesh_fn.create(
        num_points,
        1 if num_points >= 3 else 0,
        base_pts,
        v_count,
        v_list,
        mesh_data_obj,
    )

    # 3. 获取底层物理指针
    raw_ptr = new_mesh_fn.getRawPoints()
    ptr_addr = int(raw_ptr)

    # 4. Numpy 内存直写 (毫秒级)
    c_ptr = ctypes.cast(ptr_addr, ctypes.POINTER(ctypes.c_float))
    pts_np_view = np.ctypeslib.as_array(c_ptr, shape=(num_points, 3))
    pts_np_view[:, :] = xyz_points_array  # 直接覆盖内存

    # 5. 将写好的 mesh_data_obj 赋值给目标属性插头
    sel_list = om1.MSelectionList()
    sel_list.add(node_name)
    dep_node = om1.MObject()
    sel_list.getDependNode(0, dep_node)

    fn_node = om1.MFnDependencyNode(dep_node)
    plug = fn_node.findPlug(attr_name, False)
    plug.setMObject(mesh_data_obj)


# =====================================================================
# 函数 6：从 kMesh 属性上提取权重为 XYZ 数组 (零开销提取)
# =====================================================================
@time_decorator
def get_xyz_from_mesh_attr(node_name, attr_name):
    """
    输入: 节点名(str), 属性名(str)
    输出: Numpy (N, 3) 形状的浮点数组 (若没数据则返回 None)
    """
    # 1. 获取目标节点的 Plug
    sel_list = om1.MSelectionList()
    sel_list.add(node_name)
    dep_node = om1.MObject()
    sel_list.getDependNode(0, dep_node)

    fn_node = om1.MFnDependencyNode(dep_node)
    plug = fn_node.findPlug(attr_name, False)

    # 获取 MObject 数据
    mesh_data_obj = plug.asMObject()
    if mesh_data_obj.isNull():
        return None

    # 2. 包装为 MFnMesh 并获取点数
    mesh_fn = om1.MFnMesh(mesh_data_obj)
    num_points = mesh_fn.numVertices()
    if num_points == 0:
        return None

    # 3. 提取底层物理指针
    raw_ptr = mesh_fn.getRawPoints()
    ptr_addr = int(raw_ptr)
    # 4. 通过 ctypes 转换为 Numpy 数组
    c_ptr = ctypes.cast(ptr_addr, ctypes.POINTER(ctypes.c_float))
    pts_np = np.ctypeslib.as_array(c_ptr, shape=(num_points, 3)).copy()

    return pts_np


@time_decorator
def convert_skin_to_cSkin(skin_cluster_name):

    mesh = cmds.skinCluster(skin_cluster_name, q=1, g=1)[0]
    deformer = cmds.deformer(mesh, type="cSkinDeformer")[0]
    w, _ = get_skinWeights(skin_cluster_name)
    xyz = weights_to_xyz(w)
    set_xyz_to_mesh_attr(deformer, "cWeights", xyz)

    inf_list = cmds.skinCluster(skin_cluster_name, q=1, inf=1)
    bindMatrix_list = []
    for idx, influence in enumerate(inf_list):
        mat = cmds.getAttr(f"{skin_cluster_name}.bindPreMatrix[{idx}]")
        bindMatrix_list.append(mat)
        cmds.connectAttr(f"{influence}.worldMatrix[0]", f"{deformer}.matrix[{idx}]")

    set_bindMatrixArray(deformer, "bindPreMatrixArray", bindMatrix_list)
    cmds.setAttr(f"{deformer}.influencesCount", len(inf_list))

