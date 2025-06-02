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
        if cmds.objExists(self.node):
            geos = cmds.blendShape(self.node, q=1, g=1)
            if geos:
                return geos[0]
        else:
            return None


def sculptTarget(targetData: targetData = None, message=True):
    tweak = f"{targetData.baseMesh}.tweakLocation"
    inputTarget = f"{targetData.node}.inputTarget[0]"
    sculptTargetIndex = f"{inputTarget}.sculptTargetIndex"
    sculptTargetTweaks = f"{inputTarget}.sculptTargetTweaks.vertex[0]"
    sculptInbetweenWeight = f"{inputTarget}.sculptInbetweenWeight"
    cmds.sculptTarget(targetData.node, e=1, target=targetData.targetIdx, ibw=(targetData.inbetweenIdx-5000)/1000)

    """
    有bug，先用系统自带的，多个bs开启情况效果不对
    用系统自带的挺好，就是没办法隐藏 inViewMessage 如果可以隐藏，就不需要后面自己再写方法了。
    
    if cmds.getAttr(sculptTargetIndex) != -1:
        cmds.setAttr(sculptTargetIndex, -1)
        for _ in cmds.listConnections(sculptTargetTweaks, d=1, p=1) or []:
            cmds.disconnectAttr(sculptTargetTweaks, _)
        if message:
            showMessage("Sculpt target mode disabled.")
    else:
        cmds.connectAttr(sculptTargetTweaks, tweak, f=1)
        cmds.setAttr(sculptTargetIndex, targetData.targetIdx)
        cmds.setAttr(sculptInbetweenWeight, (targetData.inbetweenIdx-5000)/1000)
        if message:
            showMessage("Sculpt target mode enabled.")
    """


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
        raise RuntimeError(f"Object {sculptGeo} does not exist.")
    if not cmds.objExists(targetData.attr):
        raise RuntimeError(f"{targetData.attr} does not exist.")
    if not cmds.objExists(targetData.baseMesh):
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
    else:
        cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{targetData.inbetweenIdx}].ipt", *[1, (0, 0, 0, 1)], type="pointArray")
        cmds.setAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].iti[{targetData.inbetweenIdx}].ict", *[1, "vtx[0]"], type="componentList")

    sculptTarget(targetData, message=False)
    baseFnMesh.setPoints(sculptPoints)
    sculptTarget(targetData, message=False)


if __name__ == "__main__":
    add_sculptGeo(cmds.ls(sl=1)[0], targetData())
