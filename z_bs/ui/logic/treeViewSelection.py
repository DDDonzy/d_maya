from maya import cmds, mel
import z_bs.core.bsFunctions as fnBs
from typing import List


def get_lastSelection():
    return mel.eval("getShapeEditorTreeviewSelection 20")


def get_selectionBlendShape():
    return mel.eval("getShapeEditorTreeviewSelection 1")


def get_selectionTarget():
    return mel.eval("getShapeEditorTreeviewSelection 4")


def get_selectionInbetween():
    return mel.eval("getShapeEditorTreeviewSelection 6")


def get_lasterSelectedTargetData() -> List[fnBs.TargetData]:
    targetData: fnBs.TargetData = fnBs.TargetData()

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


def get_selectionTargetData(iterTargetInbetween=True) -> List[fnBs.TargetData]:
    """
    获取所有的选择项目，并且转换为 TargetData 列表。
    如果选择的是 blendshape 节点，则获取所有的目标数据。
    """
    target = get_selectionTarget()
    bs = get_selectionBlendShape()
    if not bs and not target:
        return []
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
        _targetList = fnBs.get_targetDataList(_bs)

        targetList = []
        if iterTargetInbetween:
            for i in _targetList:
                if i.targetIdx in idx_list:
                    targetList.append(i)
        else:
            _inbetween_dict = {}
            for i in _targetList:
                if (i.targetIdx in idx_list) and (i.inbetweenIdx > _inbetween_dict.get(i.targetIdx, [0])[0]):
                    _inbetween_dict.update({i.targetIdx: [i.inbetweenIdx, i]})
            for v in _inbetween_dict.values():
                targetList.append(v[1])

    if bs:
        bs = bs[0]
        targetList = fnBs.get_targetDataList(bs)

    return targetList


def get_selectionInbetweenData() -> List[str]:
    inbetween_list = get_selectionInbetween()
    targetData_list = []
    for inbetween in inbetween_list:
        node, target_idx, inbetween_idx = inbetween.split(".")
        inbetween_weight = fnBs.convertInbetweenIndexToValue(int(inbetween_idx))
        mode = cmds.getAttr(f"{node}.it[0].itg[{target_idx}].postDeformersMode")
        name = cmds.getAttr(f"{node}.inbetweenInfoGroup[{target_idx}].inbetweenInfo[{inbetween_idx}].inbetweenTargetName")
        targetData_list.append(fnBs.TargetData(node=node, targetIdx=int(target_idx), inbetweenIdx=int(inbetween_idx), weight=inbetween_weight, postDeformersMode=mode, targetName=name))
    return targetData_list
