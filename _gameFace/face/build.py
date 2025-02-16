from __future__ import print_function
from face.fn import cvFn
from face.fn import transform as t
from face.fn.choseFile import choseFile
from face.fn import skinFn as sk
from face.fn.calWeights import CalWeights
from face.fn.showMessage import muteMessage, showMessage
from face.fn.createBase import CreateBase, CreateNode
from face.fn.hideShapeInChannelBox import HideShapeContainer

from face.data.config import *
from face.fn.getHistory import get_history
from face.fn.hierarchyIter import hierarchyIter
from face.fit import get_allFitJoint, mirrorDuplicateTransform_cmd, get_fitJointByKeyWord
from face.control import ControlData, ControlPanel, buildControl, get_allControls, get_controlsByLabel, get_brow, get_eyeLine, get_lid, get_lip, get_cheek
from face.toMax import buildMaxJoint

from maya import cmds
from maya.api import OpenMaya as om

import yaml


class build(CreateBase):
    thisAssetName = FACE_ROOT
    isBlackBox = True

    def _pre_create(self):
        """
        Pre create.
        mirror joints.
        """
        muteMessage(True)

        if MIRROR_BUILD:
            mirrorDuplicateTransform_cmd()

    def create(self):
        """Build face logic."""
        # build face controls
        build.buildControls()
        cvFn.import_cvData(DEFAULT_SHAPES_FILE)
        # create uvPin
        build.buildUvPin()
        # class controls constraint
        build.buildClassConstraint()
        # Controls panel
        build.buildControlsPanelAndSDK()

    def _post_create(self):
        # hide fit
        cmds.setAttr("{}.v".format(FIT_ROOT), 0)
        # parent to world
        cmds.parent(CONTROL_ROOT, w=1)
        cmds.parent(SKIN_JOINT_ROOT, w=1)

        cmds.parent(UN_SKIN_JOINT_ROOT, w=1)
        cmds.setAttr(UN_SKIN_JOINT_ROOT+".v", 0)
        # hide shape
        shape_list = [x for x, _ in hierarchyIter('Controls_GRP') if cmds.objectType(x, isAType="shape")]
        HideShapeContainer(shape_list)
        # build max joints
        buildMaxJoint("MaxJoints")

        muteMessage(False)
        showMessage("Build !")

    ############################

    @staticmethod
    def buildControls():
        all_joint = get_allFitJoint()
        for x in all_joint:
            buildControl(x)

        if not cmds.objExists(UN_SKIN_JOINT_ROOT):
            CreateNode("transform", name=UN_SKIN_JOINT_ROOT)

        for x, x_dag in hierarchyIter(SKIN_JOINT_ROOT):
            if x == SKIN_JOINT_ROOT:
                continue
            for label in UN_SKIN_LABEL:
                if label in x:
                    parent = cmds.listRelatives(x, p=1)[0]
                    children_dag = [om.MDagPath.getAPathTo(x_dag.child(c)) for c in range(x_dag.childCount())]
                    children = [c.partialPathName() for c in children_dag]
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

        jaw_list = [ControlData("M_Jaw"), ControlData("M_JawUpper")]
        jaw_grp = [ctl.grp for ctl in jaw_list]

        part_list = get_controlsByLabel(PART_LABEL)
        part_grp = [ctl.grp for ctl in part_list]

        sec_list = get_controlsByLabel(SEC_LABEL)
        sec_grp = [ctl.grp for ctl in sec_list]
        sec_grp.sort()
        tongue_removeUvPin = [ControlData(x).grp for x in get_fitJointByKeyWord("Tongue")[1:]]
        class_part_grp = list((set(all_grp) - set(head_grp+jaw_grp+sec_grp)) - set(tongue_removeUvPin))
        class_part_grp.sort()

        head_pin = t.uvPin(head_grp, name='Head', size=UV_PIN_SIZE)
        jaw_pin = t.uvPin(jaw_grp, name='Jaw', size=UV_PIN_SIZE)
        part_pin = t.uvPin(class_part_grp, name="part", size=UV_PIN_SIZE)
        sec_pin = t.uvPin(sec_grp, name="Sec", size=UV_PIN_SIZE)

        t.matrixConstraint(CONTROL_ROOT, head_pin.mesh)

        for x in [head_pin.mesh, jaw_pin.mesh, part_pin.mesh, sec_pin.mesh]:
            cmds.setAttr("{}.inheritsTransform".format(x), False)
            cmds.setAttr("{}.v".format(x), False)

        jaw_sk = cmds.skinCluster(head_list[1].sk, jaw_pin.mesh, rui=0, tsb=1, name=jaw_pin.mesh+"_skinCluster")[0]

        part_sk = cmds.skinCluster([x.sk for x in head_list + jaw_list], part_pin.mesh, rui=0, tsb=1, name=part_pin.mesh+"_skinCluster")[0]

        sec_sk = cmds.skinCluster([x.sk for x in head_list + jaw_list + part_list], sec_pin.mesh, rui=0, tsb=1, name=sec_pin.mesh+"_skinCluster")[0]

        importUVPinWeights(DEFAULT_WEIGHT_FILE)

        try:
            cmds.addAttr(FACE_ROOT, ln="notes", dt="string")
        except:
            pass
        info = {"uvPin": [head_pin.mesh, jaw_pin.mesh, part_pin.mesh, sec_pin.mesh]}
        infoStr = yaml.dump(info, indent=4)
        cmds.setAttr("{}.notes".format(FACE_ROOT), infoStr, type="string")

        data = yaml.load(cmds.getAttr("{}.notes".format(sec_pin.mesh)))
        _calWeights([x.grp for x in get_lid("L_", "Upper")],
                    ['L_LidInnerPart_SK', 'L_LidUpperPart_SK', 'L_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)
        _calWeights([x.grp for x in get_lid("R_", "Upper")],
                    ['R_LidInnerPart_SK', 'R_LidUpperPart_SK', 'R_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)
        _calWeights([x.grp for x in get_lid("L_", "Lower")],
                    ['L_LidInnerPart_SK', 'L_LidLowerPart_SK', 'L_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)
        _calWeights([x.grp for x in get_lid("R_", "Lower")],
                    ['R_LidInnerPart_SK', 'R_LidLowerPart_SK', 'R_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)

        _calWeights([x.grp for x in get_brow("L_")],
                    ['L_BrowPart1_SK', 'L_BrowPart2_SK', 'L_BrowPart3_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    5,
                    data)

        _calWeights([x.grp for x in get_brow("R_")],
                    ['R_BrowPart1_SK', 'R_BrowPart2_SK', 'R_BrowPart3_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    5,
                    data)

        _calWeights([x.grp for x in get_cheek("L_")],
                    ['L_CheekUpperPart1_SK', 'L_CheekUpperPart2_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)
        _calWeights([x.grp for x in get_cheek("R_")],
                    ['R_CheekUpperPart1_SK', 'R_CheekUpperPart2_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    2,
                    data)

        _calWeights([x.grp for x in get_lip("Upper")],
                    ['R_LipCornerPart_SK', 'M_LipUpperPart_SK', "L_LipCornerPart_SK"],
                    sec_sk,
                    [0, 1, 0],
                    5,
                    data)
        _calWeights([x.grp for x in get_lip("Lower")],
                    ['R_LipCornerPart_SK', 'M_LipLowerPart_SK', "L_LipCornerPart_SK"],
                    sec_sk,
                    [0, 1, 0],
                    5,
                    data)

        _calWeights(list(set([x.grp for x in get_cheek("L_", "")]) ^ set([x.grp for x in get_cheek("L_")])),
                    ['L_LipCornerPart_SK', 'L_CheekUpperPart2_SK'],
                    sec_sk,
                    0.5,
                    1,
                    data)
        _calWeights(list(set([x.grp for x in get_cheek("R_", "")]) ^ set([x.grp for x in get_cheek("R_")])),
                    ['R_LipCornerPart_SK', 'R_CheekUpperPart2_SK'],
                    sec_sk,
                    0.5,
                    1,
                    data)
        _calWeights([x.grp for x in get_eyeLine("L")],
                    ['L_LidInnerPart_SK', 'L_LidUpperPart_SK', 'L_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    5,
                    data)
        _calWeights([x.grp for x in get_eyeLine("R")],
                    ['R_LidInnerPart_SK', 'R_LidUpperPart_SK', 'R_LidOuterPart_SK'],
                    sec_sk,
                    [0, 0.2, 0],
                    5,
                    data)

        t._uvPin.normalizedWeights(sec_pin.mesh, sec_sk)

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
                    relatives = t.relativesMatrix(name='{}_RM'.format(ctl.grp))
                    cmds.connectAttr("{}.worldMatrix[0]".format(ctl.grp), relatives.inputMatrix)
                    cmds.connectAttr("{}.worldMatrix[0]".format(x.grp), relatives.inputRelativeMatrix)
                    mult = CreateNode("multMatrix", name='{}_Addon'.format(x.grp))
                    cmds.connectAttr(relatives.outputMatrix, "{}.matrixIn[0]".format(mult))
                    cmds.connectAttr("{}.worldMatrix[0]".format(x.loc), "{}.matrixIn[1]".format(mult))
                    decom = t.decomMatrix(ctl.sdk, name=ctl.sdk, scale=False)
                    cmds.connectAttr("{}.matrixSum".format(mult), decom.inputMatrix)

    @staticmethod
    def buildControlsPanelAndSDK():
        ControlPanel()
        # set control panel position
        cmds.refresh()
        boundingBox = cmds.exactWorldBoundingBox(CONTROL_ROOT)
        pos = (om.MVector(boundingBox[3]-boundingBox[0], boundingBox[1], boundingBox[5]))
        cmds.setAttr("{}.t".format(CONTROLS_PANEL_ROOT), *pos)
        cmds.parent(CONTROLS_PANEL_ROOT, CONTROL_ROOT)


def exportUVPinWeights(path=None):
    path = choseFile(path, dialogStyle=2, caption="Export UVPin Weights", fileFilter="Weights YAML file(*.w)", startingDirectory=DEFAULT_WEIGHT_DIR)
    if path is None:
        return

    meshStr = cmds.getAttr("{}.notes".format(FACE_ROOT))
    mesh = yaml.load(meshStr)["uvPin"]
    data = {}
    for x in mesh:
        sk_node = get_history(x, "skinCluster")
        if sk_node:
            sk_node = sk_node[0]
            fnSkin = sk.D_FnSkin(sk_node)
            weights = fnSkin.auto_getWeights()
            data.update({x: weights})

    with open(path, "w") as f:
        yaml.dump(data, f, indent=4)
    om.MGlobal.displayInfo("Export UVPin Weights to {}".format(path))


def importUVPinWeights(path=None):
    path = choseFile(path, dialogStyle=2, fileMode=1, caption="Import UVPin Weights", fileFilter="Weights YAML file(*.w)", startingDirectory=DEFAULT_WEIGHT_DIR)
    if path is None:
        return

    with open(path, "r") as f:
        data_yaml = yaml.load(f)

    for mesh in data_yaml:
        sk_node = get_history(mesh, "skinCluster")

        noFindJoint = []
        for x in data_yaml[mesh].influenceName:
            if not cmds.objExists(x):
                noFindJoint.append(x)
        if noFindJoint:
            raise RuntimeError("Can not find '{}'.".format(noFindJoint))

        try:
            mesh = cmds.skinCluster(data_yaml[mesh].influenceName, mesh, tsb=1, rui=0, name='{}_skinCluster'.format(x))[0]
        except:
            pass

        fnSkin = sk.D_FnSkin(mesh)
        fnSkin.auto_setWeights(data_yaml[mesh])


def _calWeights(sec, inf, sk, parameter, degree, data):
    component_list = []
    for x in data:
        if x["driven"] in sec:
            component_list.extend(x["meshComponent"])

    calCore = CalWeights(sk)
    calCore.setVertex(component_list)
    calCore.setInfluence(inf)
    calCore.calWeights(degree, parameter)
