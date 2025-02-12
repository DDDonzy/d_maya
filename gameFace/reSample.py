from UTILS.bSpline import CurveData
from gameFace.fit import get_fitJointByKeyWord, JointData
from UTILS.create.generateUniqueName import generateUniqueName
from UTILS import transform as t
from maya import cmds

from maya.api import OpenMaya as om

num = 4


def get_lid(*args):
    args1 = list(args)
    if "Upper" in args:
        args1.remove("Upper")
    if "Lower" in args:
        args1.remove("Lower")
    return get_fitJointByKeyWord(*args1, "Inner", "Sec", "Lid")\
        + get_fitJointByKeyWord(*args, "Sec", "Lid")\
        + get_fitJointByKeyWord(*args1, "Outer", "Sec", "Lid")


def get_brow(*args):
    brow = get_fitJointByKeyWord("Sec", "Brow")
    return get_fitJointByKeyWord(*args, iterList=brow)


def get_lip(*args):
    r_corner = get_fitJointByKeyWord("R_", "Corner", "Sec", "Lip")[0]
    m = get_fitJointByKeyWord("M_", "Sec", "Lip")
    l_corner = get_fitJointByKeyWord("L_", "Corner", "Sec", "Lip")[0]

    r = get_fitJointByKeyWord("R_", "Sec", "Lip")
    r.reverse()
    l = get_fitJointByKeyWord("L_", "Sec", "Lip")
    for x in [r_corner, m, l_corner]:
        if x in l:
            l.remove(x)
        if x in r:
            r.remove(x)
    return [r_corner] + get_fitJointByKeyWord(*args, iterList=r + m + l) + [l_corner]


def get_cheek(*args):
    brow = get_fitJointByKeyWord("Sec", "Cheek")
    return get_fitJointByKeyWord(*args, iterList=brow)


def get_eyeLine(*args):
    brow = get_fitJointByKeyWord("Sec", "EyeLine")
    return get_fitJointByKeyWord(*args, iterList=brow)


def reSample(baseFit: list, num: int) -> None:
    modify_str_list = baseFit[1:-1]
    modify_list = [JointData(x) for x in modify_str_list]

    cv = CurveData(controlPoints=[cmds.xform(x, q=1, t=1, ws=1) for x in baseFit],
                   degree=2)
    t_list = [cv.length()/(num+1) * (x) for x in range(num+2)][1:-1]
    newPos_ary = [cv.getPointAtParam(cv.findParamFromLength(x)) for x in t_list]

    if len(newPos_ary) > len(modify_list):
        modify_list.extend([modify_list[-1]] * (len(newPos_ary) - len(modify_list)))
    elif len(modify_list) > len(newPos_ary):
        modify_list = modify_list[:len(newPos_ary)]

    cmds.delete(modify_str_list)
    for i, pos in enumerate(newPos_ary):
        jntData = modify_list[i]
        jntData.name = generateUniqueName(jntData.name)
        trs = t.matrix_to_trs(om.MMatrix(jntData.worldMatrix))
        trs[0:3] = [pos[0], pos[1], pos[2]]
        jntData.worldMatrix = t.trs_to_matrix(trs)
        jntData.create()
