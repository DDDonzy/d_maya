from maya import cmds
from maya.api import OpenMaya as om

def get_shape(transform_object):
    if not cmds.objExists(transform_object):
        raise RuntimeError("'{}'is not exists".format(transform_object))
    shape_list = []
    mSel = om.MSelectionList()
    mSel.add(transform_object)
    mDag = mSel.getDagPath(0)
    num_shape = mDag.numberOfShapesDirectlyBelow()
    for i in range(num_shape):
        mDag = mSel.getDagPath(0)
        mDag.extendToShape(i)
        shape_list.append(mDag.partialPathName())
    return shape_list

def hideShapeInChannelBox(objectList: list):
    if type(objectList) is str:
        objectList = [objectList]
    for obj in objectList:
        for shape in get_shape(obj):
            cmds.setAttr("{}.isHistoricallyInteresting".format(shape),0)

if __name__ == "__main__":
    hideShapeInChannelBox(cmds.ls(sl=1))