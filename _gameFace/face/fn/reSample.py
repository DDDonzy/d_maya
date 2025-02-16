from face.fn.bSpline import CurveData
from face.fn.generateUniqueName import generateUniqueName
from face.fn import transform as t

from face.fit import get_fitJointByKeyWord, JointData

from maya import cmds
from maya.api import OpenMaya as om


def reSample(baseFit, num, name=""):
    if len(baseFit) > 2:
        degree = 1
    else:
        degree = 2

    CP_pos = [cmds.xform(x, q=1, t=1, ws=1) for x in baseFit]

    cv = CurveData(controlPoints=CP_pos, degree=degree)
    t_list = [cv.length()/(num-1) * (x) for x in range(num)]
    newPos_ary = [cv.getPointAtParam(cv.findParamFromLength(x)) for x in t_list]

    jntData = JointData("x")
    jntData.parent = JointData(baseFit[0]).parent
    for i, pos in enumerate(newPos_ary):
        jntData.name = generateUniqueName(name)
        trs = t.matrix_to_trs(om.MMatrix())
        trs[0:3] = [pos[0], pos[1], pos[2]]
        jntData.worldMatrix = t.trs_to_matrix(trs)
        jntData.create()


def reSampleBrow(num):
    cmds.delete(get_fitJointByKeyWord("Brow", "Sec"))
    reSample(cmds.ls("L_BrowPart*"), num, name="L_BrowSec")
    reSample(cmds.ls("R_BrowPart*"), num, name="R_BrowSec")


def reSampleEye(num):
    cmds.delete(get_fitJointByKeyWord("Lid", "Sec", "Upper"))
    cmds.delete(get_fitJointByKeyWord("Lid", "Sec", "Lower"))
    reSample(["L_LidOuterPart"]+cmds.ls("L_LidUpperPart*")+["L_LidOuterPart"], num, name="L_LidUpperSec")
    reSample(cmds.ls("R_BrowPart*"), num, name="R_BrowSec")
