from .createControls import buildControl
from .hierarchyIter import hierarchyIter
from .fit import get_allFitJoint, mirrorDuplicateTransform_cmd, addPartJoint
from ._config import *
from UTILS.create.createBase import CreateBase
from UTILS.control import cvShape

from maya import cmds
from maya.api import OpenMaya as om


class build(CreateBase):
    thisAssetName = "FaceSystem"
    isBlackBox = False

    def _pre_create(self):
        addPartJoint()
        if MIRROR_BUILD:
            mirrorDuplicateTransform_cmd()

    def create(self):

        build.buildControls()
        cvShape.import_cvData(FACE_SHAPES_FILE)

    def _post_create(self):
        cmds.setAttr(f"{FIT_ROOT}.v", 0)

    ############################

    @staticmethod
    def buildControls():
        all_joint = get_allFitJoint()
        for x in all_joint:
            buildControl(x)

        build.removeUnSkinJoints()

    @staticmethod
    def removeUnSkinJoints():
        for x, x_dag in hierarchyIter(JOINT_ROOT):
            if x == JOINT_ROOT:
                continue
            for label in UN_SKIN_LABEL:
                if label in x.lower():
                    parent = cmds.listRelatives(x, p=1)[0]
                    children_dag = [om.MDagPath.getAPathTo(x_dag.child(x)) for x in range(x_dag.childCount())]
                    children = [x.partialPathName() for x in children_dag]
                    if children and parent:
                        cmds.parent(children, parent)
                    cmds.delete(x)
                    break
