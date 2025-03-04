from face.fn import apiundo
from face.fn.getHistory import get_history, get_obj, get_orig
from face.fn.mirrorEnv import MIRROR_CONFIG
from face.fn.choseFile import choseFile
from face.fn.showMessage import showMessage
from face.fn.transform import uvPin, reset_transformObjectValue
from face.fn.bsData import del_bsTargetData
from face.fn.bsFn import flip_bsTarget, copy_bsTargetData, get_bsData

from face.data.config import *
from face.control import ControlData

from maya import cmds
from maya.api import OpenMaya as om

import os
import yaml

import numpy as np
from functools import partial


def move_uvPin_orig(uvPin):
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(uvPin)))

    tempDict = {}
    for x in uvPin_list:
        tempDict.update({x["driven"]: x["meshComponent"]})
    outValueDict = {}
    for k, v in tempDict.items():
        obj_o = MIRROR_CONFIG.exchange(k)[0]
        outValueDict.update({k: list(set(tempDict[k]+tempDict[obj_o]))})

    orig = get_orig(uvPin)[0]
    dag = get_obj(orig, dag=1)

    fnMesh = om.MFnMesh(dag)
    posBase = fnMesh.getPoints()
    pos = np.array(posBase)
    value = 0
    for k, v in outValueDict.items():
        pos[v, 2] += value
        value += 1
    
    apiundo.commit(undo=partial(fnMesh.setPoints, posBase),
                redo=partial(fnMesh.setPoints, om.MPointArray(pos)))
    fnMesh.setPoints(om.MPointArray(pos))
    return partial(fnMesh.setPoints, posBase)