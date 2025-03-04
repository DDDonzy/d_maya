# -*- coding: utf-8 -*-
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


def move_uvPin_orig():
    """
    避免骨骼重叠的时候，镜像翻转bs的时候，出现问题
    大概原理，根据对称控制器修改对应的uvPin的位置，每对控制器保持对称
    且其他控制器不会和对称控制器重叠，然后进行bs的翻转和镜像
    
    由于API不可以撤销，所以这里使用了apiundo模块
    并且返回一个函数列表，用于镜像翻转之后进行orig的还原
    
    """
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    returnFunctionList = []
    for uvPin in uvPin_list:
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
        returnFunctionList.append(partial(fnMesh.setPoints, posBase))
    return returnFunctionList


def setPoseBase(obj, bs, targetIndex, pose_position=None):
    if not pose_position:
        uvPin_data = yaml.load(cmds.getAttr("{0}.notes".format(obj)))
        driven_list = [ControlData(x["driven"]) for x in uvPin_data]
        control_list = [x.ctl for x in driven_list]

        data_fnMesh, data = uvPin.create_planeByObjectList(targetList=control_list, buildInMaya=False, size=UV_PIN_SIZE)
        pose_position = data_fnMesh.getPoints(om.MSpace.kObject)

    obj_fnMesh = om.MFnMesh(om.MSelectionList().add(obj).getDagPath(0))
    base_pos = obj_fnMesh.getPoints(om.MSpace.kObject)

    def _doit():
        cmds.sculptTarget(bs, e=1, target=targetIndex)
        obj_fnMesh.setPoints(pose_position, om.MSpace.kObject)
        cmds.sculptTarget(bs, e=1, target=-1)
        for x in control_list:
            reset_transformObjectValue(x, True, False)

    def _undo():
        cmds.sculptTarget(bs, e=1, target=targetIndex)
        obj_fnMesh.setPoints(base_pos, om.MSpace.kObject)
        cmds.sculptTarget(bs, e=1, target=-1)

    _doit()
    apiundo.commit(undo=_undo, redo=_doit)


def setPose(targetIndex, pose_position=None):
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        bs = get_history(obj, type="blendShape")[0]
        setPoseBase(obj=obj, bs=bs, targetIndex=targetIndex)


def delPoseData(targetIndex):
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        bs = get_history(obj, type="blendShape")[0]
        del_bsTargetData(bs, targetIndex)


def prePose(targetIndex):
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]


def flipPose(source_name):
    resetList = move_uvPin_orig()
    target_name = MIRROR_CONFIG.exchange(source_name)[0]
    if source_name == target_name:
        return
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        blendShapeNode = get_history(obj, type="blendShape")[0]
        copy_bsTargetData(blendShapeNode, source_name, target_name)
        flip_bsTarget(blendShapeNode, target_name)
    for x in resetList:
        x()


def mirrorPose(targetName,
               axis="x",
               mirrorDirection=0):
    restList = move_uvPin_orig()
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        blendShapeNode = get_history(obj, type="blendShape")[0]
        targetData = get_bsData(blendShapeNode)

        cmds.blendShape(blendShapeNode, e=1, mirrorTarget=(0, targetData[targetName].index),
                        symmetryAxis=axis, mirrorDirection=mirrorDirection, symmetrySpace=1)
        cmds.symmetricModelling(e=True, r=1)
    for x in restList:
        x()


def auto_mirror_flip_pose(source_name):
    target_name = MIRROR_CONFIG.exchange(source_name)[0]
    if target_name == source_name:
        mirrorPose(target_name)
    else:
        flipPose(source_name=source_name, target_name=target_name)


def pose_scale(index, value=1.1):
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        blendShapeNode = get_history(obj, type="blendShape")[0]
        nAry = np.array(cmds.getAttr("{0}.it[0].itg[{1}].iti[6000].ipt".format(blendShapeNode, index)))
        nAry[:, :3] *= value
        cmds.setAttr("{0}.it[0].itg[{1}].iti[6000].ipt".format(blendShapeNode, index), len(nAry), *nAry, type="pointArray")


def exportPose(path=None):
    path = choseFile(path=path, dialogStyle=2, caption="Export pose", fileFilter="Pose YAML file(*.pose)", startingDirectory=POSE_DIR)
    if not path:
        return
    dir = os.path.dirname(path)
    name = os.path.basename(path)
    _name = os.path.splitext(name)[0]

    data = []
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        obj_file_name = "{0}.{1}".format(_name, obj)
        obj_path = os.path.join(dir, obj_file_name)
        bs = get_history(obj, type="blendShape")[0]
        cmds.blendShape(bs, e=1, ep=obj_path)
        data.append({"meshName": obj,
                     "blendShapeName": bs,
                     "path": obj_file_name})

    with open(path, "wb") as f:
        yaml.dump(data, f, indent=4, width=80)
    om.MGlobal.displayInfo("Export pose : {}".format(path))


def importPose(path=None):
    path = choseFile(path=path, fileMode=1, dialogStyle=2, caption="Import pose", fileFilter="Pose YAML file(*.pose)", startingDirectory=POSE_DIR)
    if not path:
        return
    dir = os.path.dirname(path)

    with open(path, "r") as f:
        data = yaml.load(f)
    for x in data:
        dataFileName = x["path"]
        dataPath = os.path.join(dir, dataFileName)
        cmds.blendShape(x["blendShapeName"], e=1, ip=dataPath)
