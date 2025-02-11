from UTILS.control import cvShape
from UTILS import transform as t
from UTILS.skin import fnSkin as sk
from UTILS.ui.showMessage import muteMessage, showMessage
from UTILS.create.createBase import CreateBase, CreateNode


from gameFace.data.config import *
from gameFace.pose import importSDK
from gameFace.hierarchyIter import hierarchyIter
from gameFace.fit import get_allFitJoint, mirrorDuplicateTransform_cmd
from gameFace.control import ControlData, ControlPanel, buildControl, get_allControls, get_controlsByLabel

from maya import cmds
from maya.api import OpenMaya as om

import yaml


class build(CreateBase):
    thisAssetName = FACE_ROOT
    isBlackBox = False

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
        cvShape.import_cvData(DEFAULT_SHAPES_FILE)
        # create uvPin
        build.buildUvPin()
        # class controls constraint
        build.buildClassConstraint()
        # Controls panel
        build.buildControlsPanelAndSDK()

    def _post_create(self):
        cmds.setAttr(f"{FIT_ROOT}.v", 0)
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

        jaw_list = [ControlData("M_Jaw"), ControlData("M_JawUpper")]
        jaw_grp = [ctl.grp for ctl in jaw_list]

        sec_list = get_controlsByLabel(SEC_LABEL)
        sec_grp = [ctl.grp for ctl in sec_list]
        sec_grp.sort()

        part_grp = list(set(all_grp) - set(head_grp+jaw_grp+sec_grp))
        part_grp.sort()

        head_pin = t.uvPin(head_grp, name='Head')

        t.matrixConstraint(CONTROL_ROOT, head_pin.mesh)
        cmds.setAttr(f"{head_pin.thisAssetName}.inheritsTransform", False)

        jaw_pin = t.uvPin(jaw_grp, name='Jaw')
        cmds.setAttr(f"{jaw_pin.thisAssetName}.inheritsTransform", False)

        sec_pin = t.uvPin(sec_grp, name="Sec")
        cmds.setAttr(f"{sec_pin.thisAssetName}.inheritsTransform", False)

        part_pin = t.uvPin(part_grp, name="part")
        cmds.setAttr(f"{part_pin.thisAssetName}.inheritsTransform", False)

        sk.importWeights(sec_pin.mesh, SEC_WEIGHT_FILE)
        sk.importWeights(part_pin.mesh, PART_WEIGHT_FILE)
        sk.importWeights(jaw_pin.mesh, JAW_WEIGHT_FILE)

        # # pose uv pin
        # mesh, _ = uvPin.create_planeByObjectList(targetList=head_grp+jaw_grp+sec_grp+part_grp, name="uvPinPose")
        # cmds.setAttr(f"{mesh}.inheritsTransform", False)
        # # to max uv pin
        # all_skin = get_allSkinJoint()
        # mesh, _ = uvPin.create_planeByObjectList(targetList=all_skin, name="uvPinToMax")
        # cmds.setAttr(f"{mesh}.inheritsTransform", False)
        # # weights
        # data = yaml.unsafe_load(cmds.getAttr(f"{mesh}.notes"))
        # w_nAry = np.zeros((len(data), len(data)*5), dtype=float)
        # for i, x in enumerate(data):
        #     w_nAry[i, x["meshComponent"]] = 1.0
        # w_nAry = w_nAry.T.reshape(-1)
        # w_data = sk.weightsData(mesh=mesh, component=[], influenceIndex=[], influenceName=all_skin, weights=w_nAry, blendWeights=[])
        # sk.importWeights(obj=mesh, data=w_data)

        try:
            cmds.addAttr(FACE_ROOT, ln="notes", dt="string")
        except:
            pass
        info = {"uvPin": [head_pin.mesh, jaw_pin.mesh, part_pin.mesh, sec_pin.mesh]}
        infoStr = yaml.dump(info, indent=4)
        cmds.setAttr(f"{FACE_ROOT}.notes", infoStr, type="string")

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
                    relatives = t.relativesMatrix(name=f'{ctl.grp}_RM')
                    cmds.connectAttr(f"{ctl.grp}.worldMatrix[0]", relatives.inputMatrix)
                    cmds.connectAttr(f"{x.grp}.worldMatrix[0]", relatives.inputRelativeMatrix)
                    mult = CreateNode("multMatrix", name=f'{x.grp}_Addon')
                    cmds.connectAttr(relatives.outputMatrix, f"{mult}.matrixIn[0]")
                    cmds.connectAttr(f"{x.loc}.worldMatrix[0]", f"{mult}.matrixIn[1]")
                    decom = t.decomMatrix(ctl.sdk, name=ctl.sdk, scale=False)
                    cmds.connectAttr(f"{mult}.matrixSum", decom.inputMatrix)

    @staticmethod
    def buildControlsPanelAndSDK():
        panel = ControlPanel()
        # set control panel position
        cmds.refresh()
        boundingBox = cmds.exactWorldBoundingBox(CONTROL_ROOT)
        pos = (om.MVector(boundingBox[3]-boundingBox[0], boundingBox[1], boundingBox[5]))
        cmds.setAttr(f"{CONTROLS_PANEL_ROOT}.t", *pos)
        cmds.parent(CONTROLS_PANEL_ROOT, CONTROL_ROOT)
        # import pose data
        data = importSDK(DEFAULT_SDK_FILE)
        meshStr = cmds.getAttr(f"{FACE_ROOT}.notes")
        mesh = yaml.unsafe_load(meshStr)["uvPin"]
        panel.setSDK(data=data, mesh=mesh)
