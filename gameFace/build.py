
from UTILS.create.createBase import CreateBase, CreateNode
from UTILS.control import cvShape
import UTILS.transform as t

from .createControls import buildControl, get_allControls, ControlData, get_controlsByLabel
from .hierarchyIter import hierarchyIter
from .fit import get_allFitJoint, mirrorDuplicateTransform_cmd, addPartJoint
from .config import *
from . import fnSkin as sk
from .calWeights import calWeights

from maya import cmds
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

import numpy as np
import json


if cmds.about(api=1) >= 2020_0000:
    uvPin = t.uvPin
else:
    uvPin = t.follicle


class build(CreateBase):
    thisAssetName = "FaceSystem"
    isBlackBox = False

    def _pre_create(self):
        """
        Pre create.
        mirror joints.
        """
        # addPartJoint()  # may be delete this functions.

        if MIRROR_BUILD:
            mirrorDuplicateTransform_cmd()

    def create(self):
        """Build face logic."""
        # build face controls
        build.buildControls()

        cvShape.import_cvData(DEFAULT_SHAPES_FILE)
        # create uvPin
        build.buildUvPin()

        build.buildClassConstraint()

    def _post_create(self):
        cmds.setAttr(f"{FIT_ROOT}.v", 0)

    ############################

    @staticmethod
    def buildControls():
        all_joint = get_allFitJoint()
        for x in all_joint:
            buildControl(x)

        # for x in get_allControls():
        #     if (cmds.listRelatives(x.grp, p=1) or [None])[0] != CONTROL_ROOT:
        #         cmds.parent(x.grp, CONTROL_ROOT)
        # for x, _ in hierarchyIter(SKIN_JOINT_ROOT):
        #     if x == SKIN_JOINT_ROOT:
        #         continue
        #     if (cmds.listRelatives(x, p=1) or [None])[0] != SKIN_JOINT_ROOT:
        #         cmds.parent(x, SKIN_JOINT_ROOT)

        build.removeUnSkinJoints()

    @staticmethod
    def removeUnSkinJoints():
        if not cmds.objExists(UN_SKIN_JOINT_ROOT):
            CreateNode("transform", name=UN_SKIN_JOINT_ROOT)

        for x, x_dag in hierarchyIter(SKIN_JOINT_ROOT):
            if x == SKIN_JOINT_ROOT:
                continue
            for label in UN_SKIN_LABEL:
                if label in x:
                    parent = cmds.listRelatives(x, p=1)[0]
                    children_dag = [om.MDagPath.getAPathTo(x_dag.child(x)) for x in range(x_dag.childCount())]
                    children = [x.partialPathName() for x in children_dag]
                    if children and parent:
                        cmds.parent(children, parent)
                    cmds.parent(x, UN_SKIN_JOINT_ROOT)
                    break

    @staticmethod
    def buildUvPin():
        if not cmds.objExists(LOCAL_JOINT_ROOT):
            CreateNode("transform", name=LOCAL_JOINT_ROOT)

        all_list = get_allControls()
        all_grp = [ctl.grp for ctl in all_list]

        head_list = [ControlData("M_HeadUpper"), ControlData("M_HeadLower")]
        head_grp = [ctl.grp for ctl in head_list]
        head_pin = uvPin(head_grp, name='Head')
        t.matrixConstraint(CONTROL_ROOT, head_pin.mesh)
        cmds.setAttr(f"{head_pin.thisAssetName}.inheritsTransform",False)

        jaw_list = [ControlData("M_Jaw"), ControlData("M_JawUpper")]
        jaw_grp = [ctl.grp for ctl in jaw_list]
        jaw_pin = uvPin(jaw_grp, name='Jaw')
        cmds.skinCluster(ControlData("M_HeadLower").sk, jaw_pin.mesh, tsb=1, rui=0)
        cmds.setAttr(f"{jaw_pin.thisAssetName}.inheritsTransform",False)

        sec_list = get_controlsByLabel(SEC_LABEL)
        sec_grp = [ctl.grp for ctl in sec_list]
        sec_pin = uvPin(sec_grp, name="Sec")
        inf = [x.sk for x in get_controlsByLabel(PART_LABEL)]
        cmds.skinCluster(inf, sec_pin.mesh, tsb=1, rui=0)
        cmds.setAttr(f"{sec_pin.thisAssetName}.inheritsTransform",False)

        part_grp = list(set(all_grp) - set(head_grp+jaw_grp+sec_grp))
        part_pin = uvPin(part_grp, name="part")
        inf = [x.sk for x in (head_list+jaw_list)]
        cmds.skinCluster(inf, part_pin.mesh, tsb=1, rui=0)
        cmds.setAttr(f"{part_pin.thisAssetName}.inheritsTransform",False)

        sk.importWeights(sec_pin.mesh, SEC_WEIGHT_FILE)
        sk.importWeights(part_pin.mesh, PART_WEIGHT_FILE)

    @staticmethod
    def buildClassConstraint():
        sec_list = get_controlsByLabel(SEC_LABEL)
        sec_loc = [x.loc for x in sec_list]
        class_list = get_controlsByLabel(CLASS_LABEL)
        for x in class_list:
            children = cmds.listRelatives(x.ctl, c=1)
            for c in children:
                if cmds.objectType(c) != "transform":
                    continue
                ctl = ControlData(c)
                if ctl.loc in sec_loc:
                    continue
                if ctl.loc != x.loc:
                    print(ctl, x)
                    relatives = t.relativesMatrix(name=f'{ctl.grp}_RM')
                    cmds.connectAttr(f"{ctl.grp}.worldMatrix[0]", relatives.inputMatrix)
                    cmds.connectAttr(f"{x.grp}.worldMatrix[0]", relatives.inputRelativeMatrix)
                    mult = CreateNode("multMatrix", name=f'{x.grp}_Addon')
                    cmds.connectAttr(relatives.outputMatrix, f"{mult}.matrixIn[0]")
                    cmds.connectAttr(f"{x.loc}.worldMatrix[0]", f"{mult}.matrixIn[1]")
                    decom = t.decomMatrix(ctl.sdk, name=ctl.sdk)
                    cmds.connectAttr(f"{mult}.matrixSum", decom.inputMatrix)
