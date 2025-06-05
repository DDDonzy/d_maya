import maya.cmds as cmds
from dataclasses import dataclass
import z_bs.utils.apiundo as apiundo

from maya import cmds, mel
from maya.api import OpenMaya as om

from z_bs.showMessage import showMessage


@dataclass
class targetData:
    node: str = None
    targetIdx: int = -1
    inbetweenIdx: int = 6000
    weight: float = 0.0

    def __post_init__(self):
        if self.node and self.targetIdx >= 0:
            return
        self.getDataFromShapeEditor()

    def getDataFromShapeEditor(self):
        bsNameData = mel.eval("getShapeEditorTreeviewSelection 11")
        targetData = mel.eval("getShapeEditorTreeviewSelection 14")
        inbetweenData = mel.eval("getShapeEditorTreeviewSelection 16")
        lastSelectedData = mel.eval("getShapeEditorTreeviewSelection 20")
        if lastSelectedData:
            lastSelectedData = lastSelectedData[0]

        if lastSelectedData in inbetweenData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            self.targetIdx = int(data[1])
            self.inbetweenIdx = int(data[-1])
            self.weight = round(cmds.getAttr(f"{self.node}.w[{self.targetIdx}]"), 3)
            return

        if lastSelectedData in targetData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            self.targetIdx = int(data[-1])
            self.weight = round(cmds.getAttr(f"{self.node}.w[{self.targetIdx}]"), 3)
            return
        if lastSelectedData in bsNameData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            return

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


def sculptTarget(targetData: targetData, message=False):
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
            showMessage("Sculpt target mode disabled.")
    else:
        cmds.connectAttr(sculptTargetTweaks, tweak, f=1)
        cmds.setAttr(sculptTargetIndex, targetData.targetIdx)

        cmds.setAttr(sculptInbetweenWeight, round((targetData.inbetweenIdx-5000)/1000, 3))
        cmds.setAttr(f"{targetData.node}.it[0].deformMatrixModified", True)
        if message:
            showMessage("Sculpt target mode enabled.")


def resetTargetDelta(targetData: targetData = None):
    if not cmds.objExists(targetData.attr):
        raise RuntimeError(f"{targetData.attr} does not exist.")
    cmds.blendShape(targetData.node, e=1, rtd=[0, targetData.targetIdx], ibi=targetData.inbetweenIdx)


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
    i = w_mi[-1]+1 if w_mi else 0
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
    return f"{bs}.{name}"


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
        targetIdx = int(1000 * round(inbetweenIdx, 3)+5000)
    else:
        inbetweenIdx = int(inbetweenIdx)
    cmds.setAttr(f"{bs}.it[0].itg[{targetIdx}].iti[{inbetweenIdx}].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
    cmds.setAttr(f"{bs}.it[0].itg[{targetIdx}].iti[{inbetweenIdx}].ict", *[1, "vtx[0]"], type="componentList")
    return f"{bs}.it[0].itg[{targetIdx}].iti[{targetIdx}]"


def add_sculptGeo(sculptGeo, targetData: targetData = None, addInbetween=True):
    if not cmds.objExists(sculptGeo):
        showMessage("Please select a sculpt geometry.")
        raise RuntimeError(f"Object {sculptGeo} does not exist.")
    if not cmds.objExists(targetData.attr):
        showMessage("Please select a blendShape target in the Shape Editor.")
        raise RuntimeError(f"{targetData.attr} does not exist.")
    if not cmds.objExists(targetData.baseMesh):
        showMessage("Please select a blendShape target in the Shape Editor.")
        raise RuntimeError(f"Base mesh {targetData.baseMesh} does not exist.")

    mSel = om.MGlobal.getSelectionListByName(sculptGeo)
    sculptFnMesh = om.MFnMesh(mSel.getDagPath(0))
    mSel = om.MGlobal.getSelectionListByName(targetData.baseMesh)
    baseFnMesh = om.MFnMesh(mSel.getDagPath(0))

    bakeSourcePoints = baseFnMesh.getPoints(om.MSpace.kObject)
    sculptPoints = sculptFnMesh.getPoints(om.MSpace.kObject)

    if addInbetween:
        inbetweenIdx = round(targetData.weight * 1000 + 5000, 3)
        inbetweenAttr = add_targetInbetween(targetData.node, targetData.targetIdx, inbetweenIdx)
        targetData.inbetweenIdx = inbetweenIdx

    sculptTarget(targetData, message=False)
    baseFnMesh.setPoints(sculptPoints)
    sculptTarget(targetData, message=False)


if __name__ == "__main__":
    add_sculptGeo(cmds.ls(sl=1)[0], targetData(), 0)
