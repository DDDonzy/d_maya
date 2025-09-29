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

    jnt = cmds.createNode("joint")
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
        weights = WeightsData(
            mesh=mesh_dag.partialPathName(),
            component=list(selections_vertex_idx),
            influenceIndex=[jnt_idx],
            influenceName=[jnt],
            weights=component_weights if inf_list > 1 else [1.0] * len(selections_vertex_idx),
            blendWeights=[0.0] * len(selections_vertex_idx),
        )
        skin.auto_setWeights(weights)

    return jnt


if __name__ == "__main__":
    autoProp(autoSkin=True)
