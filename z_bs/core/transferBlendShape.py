from maya import cmds
from z_bs.core.wrap import createWrap, createProximityWrap
from z_bs.core.bsFunctions import TargetData, add_target, add_sculptGeo, get_targetDataList, get_bsBaseGeometry, create_blendShapeNode
from z_bs.utils.duplicateMesh import duplicate_mesh
from functools import partial
# Query which model the blendShape node belongs to

# Define target blendShape data structure
from typing import List


# Pre-configured wrap function with default settings
pre_configured_wrap = partial(createProximityWrap,
                              wrapMode=1,
                              falloffScale=50,
                              smoothInfluences=0,
                              smoothNormals=0)
# Pre-configured wrap function with default settings
pre_configured_wrap2 = partial(createWrap,
                               falloffMode=1,
                               maxDistance=1,
                               weightThreshold=0,
                               autoWeightThreshold=1,
                               exclusiveBind=True)


def transferBlendShape(sourceBlendShape="", targetDataList: List[TargetData] = [],
                       destinationMesh="", destinationBlendShape=None,
                       wrapFunction=pre_configured_wrap):
    """
    Transfer blendShape targets between different topology models using wrap

    Args:
        sourceBlendShape (str): Source blendShape node name
        targetsDataToRemap (List[TargetData]): List of target data to transfer
        destinationMesh (str): Destination mesh name
        destinationBlendShape (str, optional): Destination blendShape node name
        wrapFunction (function): Wrap function to use for transfer
    """
    # get source geometry
    source_geometry, newTargetName = get_bsBaseGeometry(sourceBlendShape)
    # get target data, if not targetDataList:
    if not targetDataList:
        targetDataList = get_targetDataList(sourceBlendShape)
    # if new_bsNode == None....  then create new blendshapes node
    if destinationBlendShape is None:
        destinationBlendShape = create_blendShapeNode(objectName=destinationMesh, name="transferBlendShape")
    elif not cmds.objExists(destinationBlendShape):
        destinationBlendShape = create_blendShapeNode(objectName=destinationMesh, name="transferBlendShape")
    # do wrap
    wrapMesh = duplicate_mesh(destinationMesh, "TRANSFER_MESH")
    wrapNode, wrapBase = wrapFunction(source_geometry, wrapMesh)

    # get source bs node data
    bsData = get_targetDataList(sourceBlendShape)

    # iterate the target that needs remap
    for sourceTargetData in targetDataList:
        if not cmds.objExists(f"{destinationBlendShape}.{sourceTargetData.targetName}"):
            newTargetName, newTargetIdx = add_target(destinationBlendShape, sourceTargetData.targetName)  # create new target and get data
        else:
            try:
                targetNameList = cmds.listAttr(f'{destinationBlendShape}.weight', m=True) or []
                targetIndexList = cmds.getAttr(f'{destinationBlendShape}.weight', mi=True) or []
                newTargetIdx = targetIndexList[targetNameList.index(sourceTargetData.targetName)]
            except:
                continue
        newTargetData = TargetData(destinationBlendShape,
                                   newTargetIdx,
                                   sourceTargetData.inbetweenIdx,
                                   sourceTargetData.weight,
                                   sourceTargetData.postDeformersMode,
                                   sourceTargetData.targetName)
        sourceTargetAttr = f"{sourceTargetData.node}.inputTarget[0].inputTargetGroup[{sourceTargetData.targetIdx}]"
        newTargetAttr = f"{newTargetData.node}.inputTarget[0].inputTargetGroup[{newTargetIdx}]"

        # postDeformersMode
        cmds.setAttr(f"{newTargetAttr}.postDeformersMode", sourceTargetData.postDeformersMode)
        if sourceTargetData.postDeformersMode == 2:
            targetMatrix_sourceConnect = cmds.listConnections(f"{sourceTargetAttr}.targetMatrix", s=1, d=0) or []
            if targetMatrix_sourceConnect:
                cmds.connectAttr(targetMatrix_sourceConnect[0], f"{newTargetAttr}.targetMatrix")

        # disconnect bs weights to set value and bake weights
        bake_weight = cmds.getAttr(f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]")
        weight_sourceConnect = cmds.listConnections(f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]", p=1, s=1, d=0) or []
        if weight_sourceConnect:
            cmds.disconnectAttr(weight_sourceConnect[0], f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]")

        # transfer
        cmds.setAttr(f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]", sourceTargetData.weight)
        cmds.setAttr(f"{destinationBlendShape}.weight[{newTargetIdx}]", sourceTargetData.weight)
        print(f"Transfer: [{sourceTargetData.targetName}] - {sourceTargetData.node}.w[{sourceTargetData.targetIdx}]-[{sourceTargetData.inbetweenIdx}] to {destinationBlendShape}")
        add_sculptGeo(wrapMesh, newTargetData, True)
        # end remap
        cmds.setAttr(f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]", 0)
        cmds.setAttr(f"{destinationBlendShape}.weight[{newTargetIdx}]", 0)

        if weight_sourceConnect:
            cmds.connectAttr(weight_sourceConnect[0], f"{sourceBlendShape}.weight[{sourceTargetData.targetIdx}]")
            cmds.connectAttr(weight_sourceConnect[0], f"{destinationBlendShape}.weight[{newTargetData.targetIdx}]")
    # delete wrap
    cmds.delete(wrapMesh, wrapBase)
