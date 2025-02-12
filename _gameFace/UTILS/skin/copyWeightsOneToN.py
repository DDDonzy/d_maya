import maya.cmds as cmds
from maya.api import OpenMaya as om
from UTILS.getHistory import get_history


def copyWeightsOneToN(sour_mesh, target_mesh_list, **kwargs):
    sour_skin_node = get_history(sour_mesh, 'skinCluster')
    if not sour_skin_node:
        om.MGlobal.displayInfo(f"Can not find skinCluster in '{sour_mesh}'.")
        return
    sour_skin_node = sour_skin_node[0]
    influence_list = cmds.skinCluster(sour_skin_node, q=1, inf=1)
    skinning_method = cmds.getAttr(sour_skin_node + '.skinningMethod')
    maxInfluences = cmds.getAttr(sour_skin_node + '.maxInfluences')
    maintainMaxInfluences = cmds.getAttr(sour_skin_node + '.maintainMaxInfluences')
    new_skin_list = []
    influenceAssociation = kwargs.get('influenceAssociation', 'closestJoint')
    surfaceAssociation = kwargs.get('surfaceAssociation', 'closestPoint')
    for target_mesh in target_mesh_list:
        if get_history(target_mesh, 'skinCluster'):
            om.MGlobal.displayInfo(f"{target_mesh} has skinCluster, skip")
            continue
        target_skin_node = cmds.skinCluster(target_mesh,
                                            influence_list,
                                            tsb=1,
                                            rui=False,
                                            mi=maxInfluences,
                                            omi=maintainMaxInfluences,
                                            sm=skinning_method)[0]
        cmds.copySkinWeights(ss=sour_skin_node,
                             ds=target_skin_node,
                             noMirror=1,
                             surfaceAssociation=surfaceAssociation,
                             influenceAssociation=influenceAssociation)
        new_skin_list.append(target_skin_node)
    return new_skin_list


def copyWeightsOneToN_cmd():
    sour_mesh = cmds.ls(sl=1)[0]
    target_mesh_list = cmds.ls(sl=1)[1:]
    copyWeightsOneToN(sour_mesh, target_mesh_list)
    return target_mesh_list

# copyWeightsOneToN_cmd()
