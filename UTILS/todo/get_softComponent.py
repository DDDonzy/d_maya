from maya.api import OpenMaya as om
from collections import OrderedDict


def get_soft_selection_component(sortByWeights=False):
    """Get the soft selected component and its weights.

    Returns:
        Dict: List of tuples containing component index and its weight.
    """
    softComponentDict = OrderedDict()

    mRichSel = om.MGlobal.getRichSelection()
    sel = mRichSel.getSelection()

    _, comp = sel.getComponent(0)

    fnComp = om.MFnSingleIndexedComponent(comp)
    if fnComp.hasWeights is False:
        raise RuntimeError("Component has no weights, Please use soft selection.")

    for i in range(fnComp.elementCount):
        softComponentDict[fnComp.element(i)] = fnComp.weight(i).influence

    if sortByWeights:
        return OrderedDict(sorted(softComponentDict.items(), key=lambda x: x[1], reverse=True))
    else:
        return softComponentDict


def get_selection_component():
    """
    Get the selected component.
    Returns:
        MIntArray: List of component index.
    """

    selection = om.MGlobal.getActiveSelectionList()
    _, comp = selection.getComponent(0)
    fnComp: om.MFnSingleIndexedComponent = om.MFnSingleIndexedComponent(comp)
    return fnComp.getElements()


if __name__ == "__main__":
    print(get_soft_selection_component(True))
    print(get_selection_component())
