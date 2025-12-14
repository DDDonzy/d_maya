from typing import List
from functools import partial
from dataclasses import dataclass

from maya import cmds
from maya.api import OpenMaya as om

import m_utils.apiundo as apiundo

import log as log
from m_utils.mirrorEnv import MIRROR_BASE

@dataclass
class TargetData:
    node: str = None
    targetIdx: int = -1
    inbetweenIdx: int = 6000
    weight: float = 0.0
    postDeformersMode: int = 0
    targetName: str = ""

    @property
    def attr(self):
        return f"{self.node}.inputTarget[0].inputTargetGroup[{self.targetIdx}].inputTargetItem[{self.inbetweenIdx}]"

    @property
    def baseMesh(self):
        if not self.node:
            return None
        if cmds.objExists(self.node):
            geos = cmds.blendShape(self.node, q=1, g=1)
            if geos:
                return geos[0]
        else:
            return None

    @property
    def isNodeExists(self):
        return cmds.objExists(self.node)

    @property
    def isTargetExists(self):
        try:
            multiIndices = cmds.getAttr(f"{self.node}.inputTarget[0].inputTargetGroup", mi=1)
            if self.targetIdx in multiIndices:
                return True
        except Exception:
            return False
        return False

    @property
    def isInbetweenExists(self):
        try:
            multiIndices = cmds.getAttr(f"{self.node}.inputTarget[0].inputTargetGroup[{self.targetIdx}].inputTargetItem", mi=1)
            if self.inbetweenIdx in multiIndices:
                return True
        except Exception:
            return False
        return False


def get_targetDataList(blendShapeNode):
    """
    Get blendShape node data (updated version)

    Args:
        blendShapeNode (str): BlendShape node name

    Returns:
        list: List of TargetData objects
    """
    targetNameList = cmds.listAttr(f"{blendShapeNode}.weight", m=True) or []
    targetIndexList = cmds.getAttr(f"{blendShapeNode}.weight", mi=True) or []
    data_list = []
    for targetIdx in targetIndexList:
        item_list = cmds.getAttr(f"{blendShapeNode}.it[0].itg[{targetIdx}].iti", mi=1) or []
        postDeformersMode = cmds.getAttr(f"{blendShapeNode}.it[0].itg[{targetIdx}].postDeformersMode")
        for item in item_list:
            data = TargetData(blendShapeNode, targetIdx, item, (item - 5000) / 1000, postDeformersMode, cmds.aliasAttr(f"{blendShapeNode}.w[{targetIdx}]", q=1))
            data_list.append(data)
    return data_list


def get_bsBaseGeometry(bsNode):
    """
    Get the base geometry of blendShape node

    Args:
        bsNode (str): BlendShape node name

    Returns:
        tuple: (geometry transform, geometry shape)
    """
    geometryShape = cmds.blendShape(bsNode, q=1, g=1)[0]
    geometry = cmds.listRelatives(geometryShape, p=1)[0]
    return geometry, geometryShape


def create_blendShapeNode(objectName, name="New_Blendshapes"):
    """
    Create a new blendShape node

    Args:
        objectName (str): Target object name
        name (str): BlendShape node name

    Returns:
        str: Created blendShape node name
    """
    bsNode = cmds.blendShape(objectName, foc=1, name=name)[0]
    return bsNode


def sculptTarget(targetData: TargetData, message=False):
    """
    # Turn on/off the target sculpt mode.

    When you turn it on:
        - bsNode.it[0].sculptTargetTweaks.vertex[0] -> baseMesh.tweakLocation
        - bsNode.it[0].sculptTargetIndex = targetIdx  (-1 = off)
        - bsNode.it[0].sculptInbetweenWeight = inbetweenValue  (0.0 to 1.0)
        - bsNode.it[0].deformMatrixModified = True (to update bs.it[0].deformMatrix)

    When you turn it off:
        - bsNode.it[0].sculptTargetTweaks.vertex[0] // baseMesh.tweakLocation
        - bsNode.it[0].sculptTargetIndex = -1
        - bsNode.it[0].deformMatrixModified = False
        - bsNode.it[0].sculptInbetweenWeight = 1

    Args:
        targetData (targetData): Data about the blendShape node, target index, inbetween index, etc.
        message (bool, optional): If True, show a message in Maya UI when mode is turned on or off. Default is False.

    Maya Notes:
        - The blendShape node has a 'deformMatrix' attribute for each target.
        - You must set 'deformMatrixModified' to True to update the sculpt target.
        - 'sculptInbetweenWeight' is the inbetween position, not the blendShape weight.

    Example:
        sculptTarget(targetData_instance, message=True)
    """

    tweak = f"{targetData.baseMesh}.tweakLocation"
    inputTarget = f"{targetData.node}.inputTarget[0]"
    sculptTargetIndex = f"{inputTarget}.sculptTargetIndex"
    sculptTargetTweaks = f"{inputTarget}.sculptTargetTweaks.vertex[0]"
    sculptInbetweenWeight = f"{inputTarget}.sculptInbetweenWeight"

    if cmds.getAttr(sculptTargetIndex) != -1:
        cmds.setAttr(sculptTargetIndex, -1)
        for _ in cmds.listConnections(sculptTargetTweaks, d=1, p=1) or []:
            cmds.disconnectAttr(sculptTargetTweaks, _)
        cmds.setAttr(f"{targetData.node}.it[0].deformMatrixModified", False)
        cmds.setAttr(sculptInbetweenWeight, 1)
        if message:
            log.info("Sculpt target mode disabled.")
        return
    if targetData.isInbetweenExists:
        cmds.connectAttr(sculptTargetTweaks, tweak, f=1)
        cmds.setAttr(sculptTargetIndex, targetData.targetIdx)

        cmds.setAttr(sculptInbetweenWeight, round((targetData.inbetweenIdx - 5000) / 1000, 3))
        cmds.setAttr(f"{targetData.node}.it[0].deformMatrixModified", True)
        if message:
            log.info("Sculpt target mode enabled.")
    else:
        raise RuntimeError(f"Can not find {targetData.attr}!")


def resetInbetweenDelta(targetData: TargetData = None, removeInbetween=True):
    if not targetData.isInbetweenExists:
        raise RuntimeError(f"{targetData.attr} does not exist.")
    if removeInbetween and targetData.inbetweenIdx != 6000:
        cmds.removeMultiInstance(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{targetData.inbetweenIdx}]")
    else:
        cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{targetData.inbetweenIdx}].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
        cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{targetData.inbetweenIdx}].ict", *[1, "vtx[0]"], type="componentList")


def resetTargetDelta(targetData: TargetData = None, removeInbetween=True):
    if not targetData.isInbetweenExists:
        raise RuntimeError(f"{targetData.attr} does not exist.")

    if removeInbetween:
        inbetweenIdx = cmds.getAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti", mi=1)
        for idx in inbetweenIdx:
            cmds.removeMultiInstance(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{idx}]")
    cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[6000].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[6000].ict", *[1, "vtx[0]"], type="componentList")


def add_target(bs: str, name: str) -> str:
    """
    # Add a new target to the blendShape
    Args:
        bs (str): The name of the blendShape node.
        name (str): The name of the new target to be added.
    Returns:
        str: The full attribute path of the new target. eg: "blendShape1.w[0]"
    """

    w_mi = cmds.getAttr(f"{bs}.w", mi=1)
    i = w_mi[-1] + 1 if w_mi else 0
    cmds.setAttr(f"{bs}.w[{i}]", 0)
    if cmds.objExists(f"{bs}.{name}"):
        num = 0
        base_name = name
        while cmds.objExists(f"{bs}.{name}"):
            name = f"{base_name}{num}"
            num += 1
    cmds.aliasAttr(name, f"{bs}.w[{i}]")
    cmds.setAttr(f"{bs}.it[0].itg[{i}].iti[6000].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{bs}.it[0].itg[{i}].iti[6000].ict", *[1, "vtx[0]"], type="componentList")
    return f"{bs}.{name}", i


def add_targetInbetween(bs: str, targetIdx: int, inbetweenIdx: int, name: str = "IB") -> str:
    """
    # Add inbetween to the blendShape's target
    Args:
        bs (str): The name of the blendShape node.
        targetIdx (int): The index of the target to which the inbetween will be added.
        inbetweenIdx (int): The index of the inbetween to be added, should be between 0 and 1000.
        name (str): The name of the inbetween. Defaults to "IB".

    Returns:
        str: The full attribute path of the inbetween target. eg: "blendShape1.it[0].itg[0].iti[6000]"
    """
    if float(inbetweenIdx) < 1.0:
        targetIdx = int(1000 * round(inbetweenIdx, 3) + 5000)
    else:
        inbetweenIdx = int(inbetweenIdx)
    cmds.setAttr(f"{bs}.it[0].itg[{targetIdx}].iti[{inbetweenIdx}].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{bs}.it[0].itg[{targetIdx}].iti[{inbetweenIdx}].ict", *[1, "vtx[0]"], type="componentList")
    return f"{bs}.it[0].itg[{targetIdx}].iti[{targetIdx}]"


def add_sculptGeo(sculptGeo, targetData: TargetData = None, addInbetween=True):
    if not cmds.objExists(sculptGeo):
        raise RuntimeError(f"Object {sculptGeo} does not exist.")
    if not targetData.isTargetExists:
        raise RuntimeError(f"{targetData.node}.{targetData.targetName} does not exist.")
    if not cmds.objExists(targetData.baseMesh):
        raise RuntimeError(f"Base mesh {targetData.baseMesh} does not exist.")

    mSel = om.MGlobal.getSelectionListByName(sculptGeo)
    sculptFnMesh = om.MFnMesh(mSel.getDagPath(0))
    mSel = om.MGlobal.getSelectionListByName(targetData.baseMesh)
    baseFnMesh = om.MFnMesh(mSel.getDagPath(0))

    sculptPoints = sculptFnMesh.getPoints(om.MSpace.kObject)

    if addInbetween:
        inbetweenIdx = int(round(targetData.weight * 1000 + 5000, 3))
        targetData.inbetweenIdx = inbetweenIdx
        add_targetInbetween(targetData.node, targetData.targetIdx, targetData.inbetweenIdx)
    else:
        inbetweenIdx = 6000
        targetData.inbetweenIdx = inbetweenIdx

    baseData = copy_delta(targetData)

    def doit():
        try:
            cmds.undoInfo(stateWithoutFlush=False)
            sculptTarget(targetData, message=False)
            baseFnMesh.setPoints(sculptPoints)
            sculptTarget(targetData, message=False)
        finally:
            cmds.undoInfo(stateWithoutFlush=True)

    def undo():
        pasted_delta(targetData, baseData)

    apiundo.commit(undo, doit)
    doit()


def copy_delta(targetData: TargetData):
    iti = targetData.attr

    sel = om.MSelectionList()
    sel.add(iti)
    iti_plug: om.MPlug = sel.getPlug(0)

    return iti_plug.asMObject()


def pasted_delta(targetData: TargetData, data):
    iti = targetData.attr
    sel = om.MSelectionList()
    sel.add(iti)
    iti_plug: om.MPlug = sel.getPlug(0)
    baseData = iti_plug.asMObject()

    def doit():
        iti_plug.setMObject(data)

    def undo():
        iti_plug.setMObject(baseData)

    apiundo.commit(undo, doit)
    doit()


def flip_bsTarget(targetData: TargetData, axis="x", space=1):
    if not cmds.objExists(targetData.node):
        raise RuntimeError(f"Flip error: Can not find {targetData.node}.")
    cmds.blendShape(targetData.node, e=1, flipTarget=(0, targetData.targetIdx), symmetryAxis=axis, symmetrySpace=space)
    cmds.symmetricModelling(e=True, r=1)


# mirrorDirection = 0    +X   --->   -X
# mirrorDirection = 1    -X   --->   +X
def mirror_bsTarget(targetData: TargetData, axis="x", mirrorDirection=0, space=1):
    if not cmds.objExists(targetData.node):
        raise RuntimeError(f"Mirror error: Can not find {targetData.node}.")
    cmds.blendShape(targetData.node, e=1, mirrorTarget=(0, targetData.targetIdx), symmetryAxis=axis, mirrorDirection=mirrorDirection, symmetrySpace=space)
    cmds.symmetricModelling(e=True, r=1)


def flipCopy_targetData(sourceTargetData: TargetData, destinationTargetData: TargetData, axis="x", space=1):
    sourceTargetData.node
    sourceTargetData.targetIdx
    resetTargetDelta(destinationTargetData, removeInbetween=True)
    inbetweenIdx = cmds.getAttr(f"{sourceTargetData.node}.it[0].itg[{sourceTargetData.targetIdx}].iti", mi=1)
    # print(f"----Flip - {sourceTargetData.targetName}")
    for idx in inbetweenIdx:
        sourceTargetData.inbetweenIdx = idx
        destinationTargetData.inbetweenIdx = idx
        data = copy_delta(sourceTargetData)
        pasted_delta(destinationTargetData, data)
    flip_bsTarget(destinationTargetData, axis, space)


def autoFlipCopy(blendShapeName, targetList=[], replaceStr=("L", "R"), axis="x", direction="+", mirror=False):
    mirrorFunction = partial(mirror_bsTarget, axis=axis, mirrorDirection=direction, space=1)
    flipFunction = partial(flipCopy_targetData, axis=axis, space=1)

    bs_targetList: List[TargetData] = get_targetDataList(blendShapeName)
    bs_targetDict = {}
    for x in bs_targetList:
        bs_targetDict.update({x.targetName: x})
    bs_targetNames = list(bs_targetDict.keys())

    if not targetList:
        targetList: List[TargetData] = bs_targetList

    targetDict = {}
    for x in targetList:
        targetDict.update({x.targetName: x})
    targetList = list(targetDict.keys())

    mirrorBase = MIRROR_BASE()
    mirrorBase.MIRROR_PAIRS = [replaceStr]
    mirrorList = mirrorBase.exchange(targetList)
    doneList = []
    for i, x in enumerate(targetList):
        if x in doneList:
            continue
        doneList.append(targetList[i])
        doneList.append(mirrorList[i])
        if targetList[i] == mirrorList[i]:
            if mirror:
                print(f"{'Mirror:':<10} {x:<30}")
                mirrorFunction(targetDict[x])
            else:
                print(f"{'Continue:':<10} {x:<30}")
                continue
        else:
            print(f"{'FlipCopy:':<10} {x:-<30} >>> {mirrorList[i]:<30}")
            if mirrorList[i] in bs_targetNames:
                flipFunction(targetDict[x], bs_targetDict[mirrorList[i]])
            else:
                print(f"Warning: {mirrorList[i]} not found in targetDict, skipping flip copy.")
                continue


def get_targetIndex(node, name):
    nameList = cmds.listAttr(f"{node}.weight", m=True) or []
    indexList = cmds.getAttr(f"{node}.weight", mi=True) or []
    idx = indexList[nameList.index(name)]
    return idx


def get_targetInbetween(node, targetIdx):
    """
    Get the inbetween index for a given target index.
    """
    if not cmds.objExists(node):
        raise RuntimeError(f"Node {node} does not exist.")
    inbetween = cmds.getAttr(f"{node}.it[0].itg[{targetIdx}].iti", mi=True) or []
    return [TargetData(node, targetIdx, x) for x in inbetween]


def convertInbetweenIndexToValue(inbetweenIdx: int):
    """
    Convert inbetween index to value.
    Inbetween index is between 5000 and 6000, where 6000 is the default inbetween.
    """
    if not isinstance(inbetweenIdx, int):
        raise TypeError("Inbetween index must be an integer.")
    if inbetweenIdx < 5000 or inbetweenIdx > 6000:
        raise ValueError("Inbetween index must be between 5000 and 6000.")
    return (inbetweenIdx - 5000) / 1000.0


if __name__ == "__main__":
    autoFlipCopy("blendShape1")
