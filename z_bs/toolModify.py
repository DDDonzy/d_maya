from maya.api import OpenMaya as om
import maya.cmds as cmds
from dataclasses import dataclass
import UTILS.apiundo as apiundo

from maya import cmds, mel


@dataclass
class ShapeLasterSelectedData:
    node: str = "None"
    targetIdx: int = -1
    inbetweenIdx: int = 6000
    weight: float = 0.0

    def __post_init__(self):
        bsNameData = mel.eval("getShapeEditorTreeviewSelection 11")
        targetData = mel.eval("getShapeEditorTreeviewSelection 14")
        inbetweenData = mel.eval("getShapeEditorTreeviewSelection 16")
        lastSelectedData = mel.eval("getShapeEditorTreeviewSelection 20")
        if lastSelectedData:
            lastSelectedData = lastSelectedData[0]

        if lastSelectedData in inbetweenData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            self.targetIdx = data[1]
            self.inbetweenIdx = data[-1]
            self.weight = cmds.getAttr(f"{self.node}.w[{self.targetIdx}]")
            return

        if lastSelectedData in targetData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            self.targetIdx = data[-1]
            self.weight = cmds.getAttr(f"{self.node}.w[{self.targetIdx}]")
            return
        if lastSelectedData in bsNameData:
            data = lastSelectedData.split(".")
            self.node = data[0]
            return

    @property
    def attr(self):
        return f"{self.node}.inputTarget[0].inputTargetGroup[{self.targetIdx}].inputTargetItem[{self.inbetweenIdx}]"


def get_blendshape_attr(panel_name="shapePanel1"):
    pass


def mayaInvertAddTarget():
    sel: om.MSelectionList = om.MGlobal.getActiveSelectionList()
    pos = om.MFnMesh(sel.getDagPath(0)).getPoints()

    currentItem: BlendShapeData = get_blendshape_attr("shapePanel1")
    bs_geo = cmds.blendShape(currentItem.node, q=1, g=1)[0]
    sel.clear()
    sel.add(bs_geo)
    fnMesh = om.MFnMesh(sel.getDagPath(0))
    basePos = fnMesh.getPoints()

    def doit(fnMesh=fnMesh, pos=pos):
        cmds.sculptTarget(currentItem.node, e=1,
                          target=currentItem.targetIdx,
                          ibw=(currentItem.inbetweenIdx-5000)/1000)
        fnMesh.setPoints(pos)
        cmds.sculptTarget(currentItem.node, e=1,
                          target=currentItem.targetIdx,
                          ibw=(currentItem.inbetweenIdx-5000)/1000)

    apiundo.commit(lambda *args, **kwargs: doit(fnMesh, basePos),
                   lambda *args, **kwargs: doit(fnMesh, pos),)
    doit(fnMesh, pos)


def flipTarget():
    currentItem: BlendShapeData = get_blendshape_attr("shapePanel1")
    if currentItem.targetIdx != -1:
        cmds.blendShape(currentItem.node, e=1, flipTarget=(0, currentItem.targetIdx), symmetryAxis="x", symmetrySpace=1)


if __name__ == "__main__":
    mayaInvertAddTarget()
    # flipTarget()
