from gameFace.fn.bSpline import CurveData
from gameFace.fn.generateUniqueName import generateUniqueName
from gameFace.fn import transform as t

from gameFace.fit import get_fitJointByKeyWord, JointData

from maya import cmds
from maya.api import OpenMaya as om


def reSample(baseFit, num):
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
