import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2
import maya.OpenMaya as om1
import numpy as np
import ctypes
import re


def create_memory_mesh_from_array(np_1d_array, dummy_vtx_count):
    """辅助函数：将一维 NumPy 数组包装成 MFnMeshData"""
    v_count = om1.MIntArray()
    v_list = om1.MIntArray()
    if dummy_vtx_count >= 3:
        v_count.append(3)
        v_list.append(0)
        v_list.append(1)
        v_list.append(2)

    base_pts = om1.MFloatPointArray()
    base_pts.setLength(dummy_vtx_count)

    mesh_data_obj = om1.MFnMeshData().create()
    new_mesh_fn = om1.MFnMesh()
    new_mesh_fn.create(dummy_vtx_count, 1 if dummy_vtx_count >= 3 else 0, base_pts, v_count, v_list, mesh_data_obj)

    raw_ptr = new_mesh_fn.getRawPoints()
    try:
        ptr_addr = int(raw_ptr)
    except TypeError:
        ptr_addr = int(re.search(r"at (0x[0-9a-fA-F]+)", repr(raw_ptr)).group(1), 16)

    c_ptr = ctypes.cast(ptr_addr, ctypes.POINTER(ctypes.c_float))
    pts_np_view = np.ctypeslib.as_array(c_ptr, shape=(dummy_vtx_count, 3))

    # 填入数据
    pts_np_view[:, :] = np_1d_array.reshape((dummy_vtx_count, 3))
    return mesh_data_obj


def bake_and_initialize_system(mesh_name, skin_cluster, deformer_name):
    print("========== 启动系统初始化烘焙 (运行期与编辑期数据分离) ==========")

    # 1. OM2 极速提取权重
    sel = om2.MGlobal.getSelectionListByName(skin_cluster)
    skin_fn = oma2.MFnSkinCluster(sel.getDependNode(0))

    sel = om2.MGlobal.getSelectionListByName(mesh_name)
    mesh_path = sel.getDagPath(0)
    num_verts = om2.MFnMesh(mesh_path).numVertices

    weights_tuple, inf_count = skin_fn.getWeights(mesh_path, om2.MObject())
    w_np = np.array(weights_tuple, dtype=np.float32).reshape((num_verts, inf_count))

    # ==========================================
    # 2. 准备编辑期数据: LayerData[0] (V, B+1)
    # ==========================================
    mask_col = np.ones((num_verts, 1), dtype=np.float32)
    layer_data_np = np.hstack((w_np, mask_col))

    layer_total_floats = num_verts * (inf_count + 1)
    layer_dummy_vtx = int(np.ceil(layer_total_floats / 3.0))

    layer_flat = np.zeros(layer_dummy_vtx * 3, dtype=np.float32)
    layer_flat[:layer_total_floats] = layer_data_np.flatten()

    layer_mesh_obj = create_memory_mesh_from_array(layer_flat, layer_dummy_vtx)

    # ==========================================
    # 3. 准备运行期数据: Weights (V, B)
    # ==========================================
    weights_total_floats = num_verts * inf_count
    weights_dummy_vtx = int(np.ceil(weights_total_floats / 3.0))

    weights_flat = np.zeros(weights_dummy_vtx * 3, dtype=np.float32)
    weights_flat[:weights_total_floats] = w_np.flatten()

    weights_mesh_obj = create_memory_mesh_from_array(weights_flat, weights_dummy_vtx)

    # ==========================================
    # 4. 写入节点插槽
    # ==========================================
    sel_om1 = om1.MSelectionList()
    sel_om1.add(deformer_name)
    deformer_obj = om1.MObject()
    sel_om1.getDependNode(0, deformer_obj)
    deformer_fn = om1.MFnDependencyNode(deformer_obj)

    # A. 清理现有的所有 LayerData
    layer_plug = deformer_fn.findPlug("layerData", False)
    existing_indices = om1.MIntArray()
    layer_plug.getExistingArrayAttributeIndices(existing_indices)
    for i in range(existing_indices.length()):
        cmds.removeMultiInstance(f"{deformer_name}.layerData[{existing_indices[i]}]", b=True)

    # B. 写入 LayerData[0]
    layer_plug.elementByLogicalIndex(0).setMObject(layer_mesh_obj)

    # C. 写入 Weights 属性
    weights_plug = deformer_fn.findPlug("weightsData", False)
    weights_plug.setMObject(weights_mesh_obj)

    print("✅ 初始化完成！已清空历史 Layer。")
    print(f" -> 运行期权重写入完成 ({weights_total_floats} floats)")
    print(f" -> 编辑期 Layer[0] 写入完成 ({layer_total_floats} floats)")


if __name__ == "__main__":
    bake_and_initialize_system("maya_sk", "skinCluster1", "numpySkinDeformer1")
