from maya import cmds
from z_bs.core.wrap import createWrap, createProximityWrap
from z_bs.core.bsFunctions import TargetData, add_target, add_sculptGeo, get_targetDataList, get_bsBaseGeometry, create_blendShapeNode, get_targetIndex
from z_bs.utils.duplicateMesh import duplicate_mesh
from functools import partial
# Query which model the blendShape node belongs to

# Define target blendShape data structure
from typing import Dict, List


# Pre-configured wrap function with default settings
pre_configured_wrap = partial(
    createProximityWrap,
    wrapMode=1,
    falloffScale=50,
    smoothInfluences=0,
    smoothNormals=0,
)
# Pre-configured wrap function with default settings
pre_configured_wrap2 = partial(
    createWrap,
    falloffMode=1,
    maxDistance=1,
    weightThreshold=0,
    autoWeightThreshold=1,
    exclusiveBind=True,
)


def transferBlendShape(sourceBlendShape="", targetDataList: List[TargetData] = [], destinationMesh="", destinationBlendShape=None, wrapFunction=pre_configured_wrap, preview=False):
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
    # do wrap
    wrapMesh = duplicate_mesh(destinationMesh, "TRANSFER_MESH")
    wrapNode, wrapBase = wrapFunction(source_geometry, wrapMesh)
    if preview:
        return wrapNode, wrapBase, wrapMesh

    # get target data, if not targetDataList:
    if not targetDataList:
        targetDataList = get_targetDataList(sourceBlendShape)
    # if new_bsNode == None....  then create new blendshapes node
    if (destinationBlendShape is None) or (not cmds.objExists(destinationBlendShape)):
        destinationBlendShape = create_blendShapeNode(objectName=destinationMesh, name="transferBlendShape")
        order = cmds.getAttr(f"{sourceBlendShape}.deformationOrder")
        cmds.setAttr(f"{destinationBlendShape}.deformationOrder", order)
        print(order)

    # transfer source and target data
    transferTargetDict: Dict[str, List[TargetData]] = {}
    sourceTargetDict: Dict[str, List[TargetData]] = {}
    """
    transferTargetDict = {name: [item5000,
                                 item5500,
                                 item6000]}
    sourceTargetDict = {name: [item5000,
                               item5500,
                               item6000]}
    """
    # iterate the target that needs transfer
    for sourceTargetData in targetDataList:
        name = sourceTargetData.targetName
        if not cmds.objExists(f"{destinationBlendShape}.{name}"):
            _, newTargetIdx = add_target(destinationBlendShape, name)  # create new target and get data
        else:
            try:
                newTargetIdx = get_targetIndex(destinationBlendShape, name)
            except:
                continue
        newTargetData = TargetData(destinationBlendShape, newTargetIdx, sourceTargetData.inbetweenIdx, sourceTargetData.weight, sourceTargetData.postDeformersMode, name)
        if sourceTargetData.targetName not in sourceTargetDict.keys():
            sourceTargetDict[sourceTargetData.targetName] = [sourceTargetData]
        else:
            sourceTargetDict[sourceTargetData.targetName].append(sourceTargetData)

        if newTargetData.targetName not in transferTargetDict.keys():
            transferTargetDict[newTargetData.targetName] = [newTargetData]
        else:
            transferTargetDict[newTargetData.targetName].append(newTargetData)

    for name in transferTargetDict.keys():
        source = sourceTargetDict[name][-1]
        transfer = transferTargetDict[name][-1]

        sourceTargetAttr = f"{source.node}.inputTarget[0].inputTargetGroup[{source.targetIdx}]"
        newTargetAttr = f"{transfer.node}.inputTarget[0].inputTargetGroup[{transfer.targetIdx}]"

        # postDeformersMode
        cmds.setAttr(f"{newTargetAttr}.postDeformersMode", source.postDeformersMode)
        if source.postDeformersMode == 2:
            targetMatrix_sourceConnect = cmds.listConnections(f"{sourceTargetAttr}.targetMatrix", s=1, d=0) or []
            if targetMatrix_sourceConnect:
                cmds.connectAttr(targetMatrix_sourceConnect[0], f"{newTargetAttr}.targetMatrix")

        # disconnect bs weights to set value and bake weights
        bake_weight = cmds.getAttr(f"{source.node}.weight[{source.targetIdx}]")
        weight_sourceConnect = cmds.listConnections(f"{source.node}.weight[{source.targetIdx}]", p=1, s=1, d=0) or []
        if weight_sourceConnect:
            cmds.disconnectAttr(weight_sourceConnect[0], f"{source.node}.weight[{source.targetIdx}]")

        # transfer inbetween
        for i, _ in enumerate(transferTargetDict[name]):
            source_ib = sourceTargetDict[name][i]
            transfer_ib = transferTargetDict[name][i]

            cmds.setAttr(f"{source_ib.node}.weight[{source_ib.targetIdx}]", source_ib.weight)
            cmds.setAttr(f"{transfer_ib.node}.weight[{transfer_ib.targetIdx}]", transfer_ib.weight)
            print(f"Transfer: [{source_ib.targetName}] - {source_ib.node}.w[{source_ib.targetIdx}]-[{source_ib.inbetweenIdx}] to {transfer_ib.node}")
            add_sculptGeo(wrapMesh, transfer_ib, True)
            cmds.setAttr(f"{source_ib.node}.weight[{source_ib.targetIdx}]", 0)
            cmds.setAttr(f"{transfer_ib.node}.weight[{transfer_ib.targetIdx}]", 0)

        if weight_sourceConnect:
            cmds.connectAttr(weight_sourceConnect[0], f"{source.node}.weight[{source.targetIdx}]")
            cmds.connectAttr(weight_sourceConnect[0], f"{transfer.node}.weight[{transfer.targetIdx}]")
        if bake_weight:
            cmds.setAttr(f"{source.node}.weight[{source.targetIdx}]", bake_weight)
            cmds.setAttr(f"{transfer.node}.weight[{transfer.targetIdx}]", bake_weight)
    # delete wrap
    cmds.delete(wrapNode, wrapMesh, wrapBase)
