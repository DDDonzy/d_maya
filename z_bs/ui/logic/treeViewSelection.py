from maya import cmds, mel
from z_bs.core.bsFunctions import TargetData, get_targetDataList
from typing import List


def get_lastSelection():
    return mel.eval("getShapeEditorTreeviewSelection 20")


def get_selectionBlendShape():
    return mel.eval("getShapeEditorTreeviewSelection 11")


def get_selectionTarget():
    return mel.eval("getShapeEditorTreeviewSelection 14")


def get_selectionInbetween():
    return mel.eval("getShapeEditorTreeviewSelection 16")


def get_lasterSelectedData() -> List[TargetData]:
    targetData: TargetData = TargetData()

    bsNameSelected = get_selectionBlendShape()
    targetSelected = get_selectionTarget()
    inbetweenSelected = get_selectionInbetween()
    lastSelectedSelected = get_lastSelection()
    if lastSelectedSelected:
        lastSelectedSelected = lastSelectedSelected[0]

    if lastSelectedSelected in inbetweenSelected:
        data = lastSelectedSelected.split(".")
        targetData.node = data[0]
        targetData.targetIdx = int(data[1])
        targetData.inbetweenIdx = int(data[-1])
        targetData.weight = round(cmds.getAttr(f"{targetData.node}.w[{targetData.targetIdx}]"), 3)

    if lastSelectedSelected in targetSelected:
        data = lastSelectedSelected.split(".")
        targetData.node = data[0]
        targetData.targetIdx = int(data[-1])
        targetData.weight = round(cmds.getAttr(f"{targetData.node}.w[{targetData.targetIdx}]"), 3)
        targetData.targetName = cmds.aliasAttr(f"{targetData.node}.w[{targetData.targetIdx}]", q=1)

    if lastSelectedSelected in bsNameSelected:
        data = lastSelectedSelected.split(".")
        targetData.node = data[0]

    if targetData.targetIdx >= 0:
        targetData.postDeformersMode = cmds.getAttr(f"{targetData.node}.it[0].itg[{targetData.targetIdx}].postDeformersMode")

    return targetData


def get_selectionConvertToTargetData():
    target = get_selectionTarget()
    bs = get_selectionBlendShape()
    if not bs and not target:
        raise RuntimeError("Please select blendshape or targets in shapeEdit.")
    if target and bs:
        raise RuntimeError("Please select blendshape or targets in shapeEdit not both.")
    if len(bs) > 1:
        raise RuntimeError("Please select only one blendshape node in shapeEdit.")

    if target:
        _bs = target[0].split(".")[0]
        idx_list = []
        for i in target:
            i_bs, idx = i.split(".")
            idx_list.append(int(idx))
            if i_bs != _bs:
                raise RuntimeError("Please select targets from the same blendShape node")
        _targetList = get_targetDataList(_bs)
        targetList = []
        for i in _targetList:
            if i.targetIdx in idx_list:
                targetList.append(i)
    if bs:
        bs = bs[0]
        targetList = get_targetDataList(bs)

    return targetList
