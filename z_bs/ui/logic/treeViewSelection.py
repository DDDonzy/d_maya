from maya import cmds, mel
from z_bs.core.bsFunctions import TargetData


def get_lastSelection():
    return mel.eval("getShapeEditorTreeviewSelection 20")


def get_selectionBlendShape():
    return mel.eval("getShapeEditorTreeviewSelection 11")


def get_selectionTarget():
    return mel.eval("getShapeEditorTreeviewSelection 14")


def get_selectionInbetween():
    return mel.eval("getShapeEditorTreeviewSelection 16")


def getDataFromShapeEditor():
    targetData: TargetData = TargetData()
    
    bsNameData = get_selectionBlendShape()
    targetData = get_selectionTarget()
    inbetweenData = get_selectionInbetween()
    lastSelectedData = get_lastSelection()
    if lastSelectedData:
        lastSelectedData = lastSelectedData[0]

    if lastSelectedData in inbetweenData:
        data = lastSelectedData.split(".")
        targetData.node = data[0]
        targetData.targetIdx = int(data[1])
        targetData.inbetweenIdx = int(data[-1])
        targetData.weight = round(cmds.getAttr(f"{targetData.node}.w[{targetData.targetIdx}]"), 3)

    if lastSelectedData in targetData:
        data = lastSelectedData.split(".")
        targetData.node = data[0]
        targetData.targetIdx = int(data[-1])
        targetData.weight = round(cmds.getAttr(f"{targetData.node}.w[{targetData.targetIdx}]"), 3)
        targetData.targetName = cmds.aliasAttr(f"{targetData.node}.w[{targetData.targetIdx}]", q=1)

    if lastSelectedData in bsNameData:
        data = lastSelectedData.split(".")
        targetData.node = data[0]

    if targetData.targetIdx >= 0:
        targetData.postDeformersMode = cmds.getAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].postDeformersMode")

    return targetData
