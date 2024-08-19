# Author:   Donzy.xu
# CreateTime:   2022/6/22 - 2:42
# FileName:  mirror_curve
from pymel.core import *


def symmetryCV(obj=None):
    obj = selected()
    for x in obj:
        x = PyNode(x)
        shapes = x.getShapes()
        for z in shapes:
            opposite = PyNode(get_oppositeString(z.name()))
            transformList = z.numCVs()
            for i in range(transformList):
                pos = z.getCV(i, space='world')
                xform(opposite.cv[i], t=[-pos[0], pos[1], pos[2]], ws=1)


symmetryCV(obj=None)
