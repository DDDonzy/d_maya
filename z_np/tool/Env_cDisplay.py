import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2
import z_np.src2.cWeightsHandle as weightsHandle

import z_np.tool._reload as reload
import z_np.tool._reloadPlugin as reloadPlugin


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


def convert_skin_to_cSkin(skin_cluster_name):

    mesh = cmds.skinCluster(skin_cluster_name, q=1, g=1)[0]
    deformer = cmds.deformer(mesh, type="cSkinDeformer")[0]

    inf_list = cmds.skinCluster(skin_cluster_name, q=1, inf=1)
    bindMatrix_list = []
    for idx, influence in enumerate(inf_list):
        mat = cmds.getAttr(f"{skin_cluster_name}.bindPreMatrix[{idx}]")
        bindMatrix_list.append(mat)
        cmds.connectAttr(f"{influence}.worldMatrix[0]", f"{deformer}.matrix[{idx}]")

    set_bindMatrixArray(deformer, "bindPreMatrixArray", bindMatrix_list)
    cmds.setAttr(f"{skin_cluster_name}.envelope", 0.0)
    return deformer




reload.reload_modules_in_path(r"E:\d_maya\z_np\src2")
reloadPlugin.reload_all_plugins()



cmds.file("C:/Users/Donzy/Desktop/ng_test.ma", o=1, f=1)
cmds.createNode("WeightPreviewShape")
cmds.connectAttr("cSkinDeformer1.refresh","WeightPreviewShape1.refresh")
cmds.setAttr("WeightPreviewShape1.layer",-1)
