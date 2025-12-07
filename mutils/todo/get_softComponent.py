"""
================================================================================
Maya 软选择组件获取工具
================================================================================
选择模型、点、边或面后，获取软选择组件及其权重信息。
================================================================================
"""

from maya.api import OpenMaya as om
from collections import OrderedDict


def get_soft_selection_component(sortByWeights=False):


    mRichSel = om.MGlobal.getRichSelection()
    sel: om.MSelectionList = mRichSel.getSelection()

    data = {}
    for i in range(sel.length()):
        mDag, comp = sel.getComponent(i)

        softComponentDict = OrderedDict()
        if comp.apiType() == om.MFn.kMeshVertComponent:
            fnComp = om.MFnSingleIndexedComponent(comp)
            for i in range(fnComp.elementCount):
                softComponentDict[fnComp.element(i)] = fnComp.weight(i).influence if fnComp.hasWeights else 1.0
            if sortByWeights:
                softComponentDict = OrderedDict(sorted(softComponentDict.items(), key=lambda x: x[1], reverse=True))
        else:
            fnMesh: om.MFnMesh = om.MFnMesh(mDag)
            for i in range(fnMesh.numVertices):
                softComponentDict[i] = 1.0
        data[mDag.partialPathName()] = softComponentDict

    return data


if __name__ == "__main__":
    print(get_soft_selection_component(sortByWeights=True))
