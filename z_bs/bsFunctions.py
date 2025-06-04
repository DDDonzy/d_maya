import maya.cmds as cmds
from dataclasses import dataclass
import z_bs.apiundo as apiundo

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


def sculptTarget(targetData: targetData = None, message=False):
    """ 
    Maya 自带bs 是有Invert逆矩阵的属性的 bs.it[0].deformMatrix
    需要 开启 bs.it[0].deformMatrixModified 才能刷新。
    it.[0].sculptInbetweenWeight 属性需要注意，这个属性代表 inbetween 的位置，和bs.w的权重无关
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


def add_target(bs: str, name: str):

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


def add_targetInbetween(bs: str, targetIdx, inbetweenIdx, name: str = "IB"):
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
