from maya.api import OpenMaya as om
import maya.cmds as cmds
from dataclasses import dataclass
import z_bs.utils.apiundo as apiundo



@dataclass
class BlendShapeData:
    node: str
    targetIdx: int = -1
    inbetweenIdx: int = 6000
    attr: str = ""

    def __post_init__(self):
        self.attr = f"{self.node}.inputTarget[0].inputTargetGroup[{self.targetIdx}].inputTargetItem[{self.inbetweenIdx}]"


def get_blendshape_attr(panel_name="shapePanel1"):
    """获取Shape Editor当前选中项的BlendShape属性路径"""
    try:
        str_info = cmds.shapeEditor(panel_name, q=True, ls=True)
        if not str_info:
            return None
        info_list = str_info.replace("/", "").split(".")
        node = info_list[0]
        if len(info_list) == 1:
            return BlendShapeData(node)
        elif len(info_list) == 2:
            return BlendShapeData(node, int(info_list[1]))
        else:
            return BlendShapeData(node, int(info_list[1]), int(info_list[2]))

    except:
        return None


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