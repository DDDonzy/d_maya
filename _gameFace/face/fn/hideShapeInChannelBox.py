from maya import cmds
from maya.api import OpenMaya as om
from face.fn.createBase import CreateBase


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


def hideShapeInChannelBox(objectList):
    if isinstance(objectList, basestring):
        objectList = [objectList]
    for obj in objectList:
        if cmds.objectType(obj, isAType="transform"):
            for shape in get_shape(obj):
                cmds.setAttr("{}.isHistoricallyInteresting".format(shape), 0)
        if cmds.objectType(obj, isAType="shape"):
            cmds.setAttr("{}.isHistoricallyInteresting".format(obj), 0)


class hideShapeContainer(CreateBase):
    thisAssetName = "HideShapeContainer"
    isDagAsset = True
    isBlackBox = True

    def __init__(self, *args, **kwargs):
        if not args:
            raise RuntimeError("No object to hide shape. Please input object to hide shape.")
        args = list(args)
        self.obj = args.pop(0)
        if isinstance(self.obj, basestring):
            self.obj = [self.obj]

        super(hideShapeContainer, self).__init__(*args, **kwargs)

    def create(self):
        for x in self.obj:
            if cmds.objectType(x, isAType="transform"):
                for shape in get_shape(x):
                    cmds.container(self.name, an=[shape])
            if cmds.objectType(x, isAType="shape"):
                cmds.container(self.name, an=[x])


if __name__ == "__main__":
    hideShapeInChannelBox(cmds.ls(sl=1))
