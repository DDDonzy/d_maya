from pymel.core import *


def mirrorTransform(obj=None, duplicateMode=True):
    sl = selected()
    for x in sl:
        if type(obj) == list:
            x = PyNode(x)
        loc = spaceLocator(name='temp')
        delete(parentConstraint(x, loc))
        t = xform(loc, q=1, t=1, ws=1)
        r = xform(loc, q=1, ro=1, ws=1)
        oppositeT = [-t[0], t[1], t[2]]
        oppositeR = [-r[0], -r[1] - 180, -r[2]]
        delete(loc)
        oppositeOBJ = get_oppositeString(x.name())
        if duplicateMode == False:
            if oppositeOBJ != x:
                xform(oppositeOBJ, t=oppositeT, ws=1)
                xform(oppositeOBJ, ro=oppositeR, ws=1)
            else:
                pass
        else:
            oppositeOBJ = duplicate(x, name=oppositeOBJ)[0]
            xform(oppositeOBJ, t=oppositeT, ws=1)
            xform(oppositeOBJ, ro=oppositeR, ws=1)
    select(sl)


mirrorTransform(obj=None, duplicateMode=False)
