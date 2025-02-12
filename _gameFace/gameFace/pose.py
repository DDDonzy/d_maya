from __future__ import print_function
import numpy as np
from UTILS import apiundo
from UTILS.getHistory import get_history
from UTILS.mirrorEnv import MIRROR_CONFIG
from UTILS.other.choseFile import choseFile
from UTILS.ui.showMessage import showMessage
from UTILS.transform import uvPin, reset_transformObjectValue
from UTILS.bs.blendShapePsdTool.blendShapePsdTool import del_bsTargetData
from UTILS.bs.bs_flip_mirror import flip_bsTarget, copy_bsTargetData, get_bsData

from gameFace.data.config import *
from gameFace.control import ControlData

from maya import cmds
from maya.api import OpenMaya as om

import os
import yaml


class SDKData(yaml.YAMLObject):
    yaml_tag = 'SDKData'

    def __init__(self, name, driverAttr=None, min=0, max=1):
        self.name = name
        self.driverAttr = driverAttr
        self.min = min
        self.max = max

    def __str__(self):
        return self.name


def exportSDK(data, path=None):

    path = choseFile(path, dialogStyle=2, caption="Export SDK", fileFilter="SDK YAML file(*.yaml)", startingDirectory=DEFAULT_SDK_DIR)
    if not path:
        return

    with open(path, "w") as f:
        yaml.dump(data, f, indent=4, width=80)

    showMessage("Export SDK.")


def importSDK(path=None):

    path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="SDK YAML file(*.yaml)", fileMode=1, startingDirectory=DEFAULT_SDK_DIR)
    if not path:
        return

    with open(path, "r") as f:
        data = yaml.load(f)

    showMessage("Import SDK.")
    return data


def setPoseBase(obj, bs, targetIndex, pose_position=None):
    if not pose_position:
        uvPin_data = yaml.load(cmds.getAttr("{0}.notes".format(obj)))
        driven_list = [ControlData(x["driven"]) for x in uvPin_data]
        control_list = [x.ctl for x in driven_list]

        data_fnMesh, data = uvPin.create_planeByObjectList(targetList=control_list, buildInMaya=False)
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


def flipPose(source_name):
    target_name = MIRROR_CONFIG.exchange(source_name)[0]
    if source_name == target_name:
        return
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        blendShapeNode = get_history(obj, type="blendShape")[0]
        copy_bsTargetData(blendShapeNode, source_name, target_name)
        flip_bsTarget(blendShapeNode, target_name)


def mirrorPose(targetName,
               axis="x",
               mirrorDirection=0):

    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        blendShapeNode = get_history(obj, type="blendShape")[0]
        targetData = get_bsData(blendShapeNode)
        cmds.blendShape(blendShapeNode, e=1, mirrorTarget=(0, targetData[targetName].index),
                        symmetryAxis=axis, mirrorDirection=mirrorDirection, symmetrySpace=1)
        cmds.symmetricModelling(e=True, r=1)


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
    path = choseFile(path=path, dialogStyle=2, caption="Export pose", fileFilter="YAML file(*.yaml)", startingDirectory=POSE_DIR)
    if not path:
        return
    dir = os.path.dirname(path)
    name = os.path.basename(path)
    os.path.splitext(path)

    data = []
    uvPin_list = yaml.load(cmds.getAttr("{0}.notes".format(FACE_ROOT)))["uvPin"]
    for obj in uvPin_list:
        obj_file_name = "{0}_{1}_poseData".format(name, obj)
        obj_path = os.path.join(dir, obj_file_name)
        bs = get_history(obj, type="blendShape")[0]
        cmds.blendShape(bs, e=1, ep=obj_path)
        data.append({
            "mesh": obj,
            "blendShapeName": bs,
            "path": obj_file_name
        })

    with open(path, "wb") as f:
        yaml.dump(data, f, indent=4, width=80)


def importPose(path=None):
    path = choseFile(path=path, fileMode=1, dialogStyle=2, caption="Import pose", fileFilter="YAML file(*.yaml)", startingDirectory=POSE_DIR)
    if not path:
        return
    dir = os.path.dirname(path)

    with open(path, "r") as f:
        data = yaml.load(f)
    for x in data:
        dataFileName = x["path"]
        dataPath = os.path.join(dir, dataFileName)
        cmds.blendShape(x["blendShapeName"], e=1, ip=dataPath)
