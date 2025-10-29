"""
================================================================================
Automatic Prop Joint Creation and Skinning Tool
================================================================================

[ 脚本目的 ]
该脚本提供了一个名为 `autoProp` 的自动化工具，用于在 Maya 中快速为一个网格
(mesh) 或其选定的组件部分创建一个“道具”或“辅助”骨骼 (prop joint)。
创建后，脚本可以选择性地将这个新骨骼自动蒙皮到对应的网格组件上。

这在需要为特定区域（如盔甲、配饰、肌肉）添加一个独立的控制器时非常有用。

[ 工作流程 ]
1.  智能选择检测:
    - 脚本首先会检查用户的当前选择，并按以下优先级获取组件和权重：
        a. **软选择 (Soft Selection)**: 如果软选择已激活，脚本会获取所有受影响的
           顶点及其对应的权重值。
        b. **组件选择 (Component Selection)**: 如果没有软选择，脚本会获取当前选中
           的顶点（或从边/面转换的顶点），并将权重设置为 1.0。
        c. **对象选择 (Object Selection)**: 如果只选择了物体而没有选择组件，脚本
           会默认使用该物体的所有顶点。

2.  中心点计算与骨骼创建:
    - 根据获取到的顶点位置，脚本会计算出这些顶点的几何中心（边界框中心）。
    - 在这个中心位置创建一个新的骨骼 (joint)。

3.  自动蒙皮 (可选):
    - 如果 `autoSkin` 参数为 `True` (默认值)，脚本会执行以下蒙皮操作：
        a. **检查蒙皮节点**: 如果目标网格上没有 `skinCluster` 节点，则创建一个
           新的，并将新骨骼作为影响。
        b. **添加影响**: 如果已存在 `skinCluster` 节点，则将新创建的骨骼添加为
           一个新的影响对象。
        c. **设置权重**: 使用自定义的 `D_FnSkin` 工具类，将之前获取到的权重
           (软选择权重或 1.0) 精确地设置到对应的顶点上。

[ 如何使用 ]
1.  在 Maya 中选择一个网格物体，或者选择该物体上的一些顶点/边/面。
2.  (可选) 开启软选择 (按 'b' 键) 并调整衰减范围。
3.  在 Maya 的脚本编辑器中执行 `autoProp()` 函数。

[ 返回值 ]
- 函数会返回新创建的骨骼的名称 (string)。

[ 依赖项 ]
- `numpy`: 用于高效的数组和矩阵运算。
- `UTILS` 模块: 依赖于项目内部的自定义工具，如 `D_FnSkin` (蒙皮处理)
  和 `get_soft_selection_component` (组件获取)。

================================================================================
"""

import numpy as np

from maya.api import OpenMaya as om
from maya import cmds


from UTILS.deform.skin.fnSkin import D_FnSkin, WeightsData
from UTILS.todo.get_softComponent import get_selection_component, get_soft_selection_component
from UTILS.dag.getHistory import get_history


def autoProp(autoSkin=True):
    try:
        sel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
        mesh_dag: om.MDagPath = sel.getDagPath(0)
        name = mesh_dag.partialPathName().replace("Shape", "")
    except Exception:
        cmds.error("Please select mesh and its components.")
        raise

    fnMesh: om.MFnMesh = om.MFnMesh(mesh_dag)

    try:
        # soft selection components
        soft_component_dict = get_soft_selection_component()
        selections_vertex_idx = list(soft_component_dict.keys())
        component_weights = list(soft_component_dict.values())
    except Exception:
        try:
            selections_vertex_idx = get_selection_component()
            component_weights = [1.0] * len(selections_vertex_idx)
        except Exception:
            selections_vertex_idx = range(fnMesh.numVertices)

    # create joint
    pos_mAry = [fnMesh.getPoint(x, om.MSpace.kWorld) for x in selections_vertex_idx]
    pos_nAry = np.array([[p.x, p.y, p.z] for p in pos_mAry])

    min_pos = pos_nAry.min(axis=0)
    max_pos = pos_nAry.max(axis=0)
    center_pos = (max_pos + min_pos) * 0.5
    center_matrix = om.MMatrix()
    center_matrix[12], center_matrix[13], center_matrix[14] = center_pos

    jnt = cmds.createNode("joint", name=f"JNT_prop_{name}")
    cmds.xform(jnt, ws=1, matrix=center_matrix)

    if autoSkin:
        #  bind skin
        try:
            skin_node = cmds.skinCluster(mesh_dag.fullPathName(), jnt, tsb=1, rui=0, name=f"{mesh_dag.partialPathName()}_skinCluster", inf=jnt)[0]
        except Exception:
            skin_node = get_history(mesh_dag.fullPathName(), type="skinCluster")[0]
            if skin_node:
                cmds.skinCluster(skin_node, e=1, ai=jnt, wt=0)

        # set weights
        skin: D_FnSkin = D_FnSkin(skin_node)
        inf_list = skin.influenceObjects()
        for i, x in enumerate(inf_list):
            if x.partialPathName() == jnt:
                jnt_idx = i  # influence index
                break
        weights = component_weights if len(inf_list) > 1 else [1.0] * len(selections_vertex_idx)
        data: WeightsData = WeightsData(
            mesh=mesh_dag.partialPathName(),
            component=list(selections_vertex_idx),
            influenceIndex=[jnt_idx],
            influenceName=[jnt],
            weights=weights,
            blendWeights=[0.0] * len(selections_vertex_idx),
        )
        skin.auto_setWeights(data)

    return jnt


if __name__ == "__main__":
    autoProp(autoSkin=True)
