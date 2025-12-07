from maya.api import OpenMaya as om
from maya import cmds


def getInputTargetGeometry(select=True):
    objList = []
    bsNode = cmds.ls(sl=1)
    if not bsNode:
        return
    bsNode = bsNode[0]
    bsTargetList = cmds.channelBox("mainChannelBox", q=1, sha=1) or []

    for x in bsTargetList:
        mSel = om.MSelectionList()
        mSel.add(f"{bsNode}.{x}")
        mPlug = mSel.getPlug(0)
        logicalIndex = mPlug.logicalIndex()
        inputTargetAttr = f"{bsNode}.inputTarget[0].inputTargetGroup[{logicalIndex}].inputTargetItem[6000].inputGeomTarget"
        objList.extend(cmds.listConnections(inputTargetAttr, s=1, d=0))
    if select:
        cmds.select(objList)


if __name__ == "__main__":
    getInputTargetGeometry()
