from maya import cmds
from maya.api import OpenMaya as om


def get_obj(obj=None, dag=False, plug=False):
    """
    Get the partial path name of the specified object.

    Args:
        obj (str, optional): The name of the object. If None the active selection is used.

    Returns:
        str: The partial path name of the object.
    """

    if obj:
        mSel = om.MSelectionList()
        try:
            mSel.add(obj)
        except:
            raise ValueError(f"Object {obj} not found.")
    else:
        mSel = om.MGlobal.getActiveSelectionList()
        if mSel.isEmpty():
            raise ValueError(f"No object selected.")

    if plug:
        return mSel.getPlug(0)

    mDag = mSel.getDagPath(mSel.length() - 1)
    return mDag if dag else mDag.partialPathName()



def get_history(obj=None, type="node"):
    """
    Get the history of the specified object.
    Args:
        obj (str): The name of the object to get history for. If None, the active selection is used.
        type (str): The type of history nodes to filter by.
    Returns:
        list: A list of history nodes of the specified type.
    """

    obj = get_obj(obj)
    out_list = []

    history_list = cmds.listHistory(obj, pdo=1, il=1) or []

    for his in history_list:
        if cmds.objectType(his, isa=type):
            out_list.append(his)

    return out_list


def get_shape(obj=None):
    """
    Get the shape nodes of the specified transform object.
    Args:
        obj (str): The name of the transform object. If None, the active selection is used.
    Returns:
        list: A list of shape node names.
    """

    mDag = get_obj(obj, dag=True)
    shape_list = []

    num_shape = mDag.numberOfShapesDirectlyBelow()
    for i in range(num_shape):
        mDag.extendToShape(i)
        shape_list.append(mDag.partialPathName())

    return shape_list


def get_orig(obj=None):
    """
    Get the original shape node of the specified deformed object.
    Args:
        obj (str): The name of the deformed object. If None, the active selection is used.
    Returns:
        str: The name of the original shape node.
    """

    obj = get_obj(obj)
    all_orig = []

    all_history = cmds.listHistory(obj)
    for x in all_history:
        try:
            if cmds.getAttr(f"{x}.intermediateObject"):
                all_orig.append(x)
        except:
            pass
    return all_orig
