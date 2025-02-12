from __future__ import print_function
from UTILS.mirrorEnv import MIRROR_CONFIG
from UTILS.other.choseFile import choseFile
from UTILS.ui.showMessage import showMessage
from UTILS.create.createBase import CreateNode
from UTILS.transform import get_worldMatrix, set_worldMatrix, flip_transform

from gameFace.data.config import *
from gameFace.hierarchyIter import hierarchyIter

import yaml

from maya import cmds
from maya.api import OpenMaya as om


class JointData(yaml.YAMLObject):
    """Joints data"""
    yaml_tag = 'JointData'

    def __init__(self, name):
        self.name = name
        self.parent = ""
        self.worldMatrix = []
        self.preferredAngle = []
        self.rotateOrder = 0
        self.radius = 1.0
        self.drawStyle = 0
        self.segmentScaleCompensate = True
        self.inheritsTransform = True
        self.visibility = True

        if cmds.objExists(self.name):
            self.getData(name=self.name)

    def getData(self, name):
        """Get joint data"""
        self.parent = (cmds.listRelatives(self.name, p=1) or ["kWorld"])[0]
        self.worldMatrix = list(get_worldMatrix(self.name))
        try:
            setattr(self, "preferredAngle", list(cmds.getAttr("{0}.preferredAngle".format(self.name))[0]))
        except:
            pass
        for attr in ["segmentScaleCompensate",
                     "rotateOrder",
                     "inheritsTransform",
                     "radius",
                     "drawStyle",
                     "visibility"]:
            try:
                setattr(self, attr, cmds.getAttr("{0}.{1}".format(self.name, attr)))
            except:
                pass

    def setData(self):
        """Set joint data by this class data"""
        if self.parent == "kWorld":
            pass
        else:
            try:
                cmds.parent(self.name, self.parent)
            except:
                pass
        set_worldMatrix(self.name, om.MMatrix(self.worldMatrix))
        try:
            cmds.setAttr("{0}.preferredAngle".format(self.name), *self.preferredAngle)
        except:
            pass
        for attr in ["segmentScaleCompensate",
                     "rotateOrder",
                     "inheritsTransform",
                     "radius",
                     "drawStyle",
                     "visibility"]:
            try:
                cmds.setAttr("{0}.{1}".format(self.name, attr), getattr(self, attr))
            except:
                pass
        if SET_SEGMENT_SCALE_COMPENSATE_FALSE_FORCE:
            cmds.setAttr("{0}.segmentScaleCompensate".format(self.name), False)

    def create(self):
        if cmds.objExists(self.name):
            self.setData()
            om.MGlobal.displayWarning("'{0}' exists!".format(self.name))
            return
        jnt = CreateNode("joint", name=self.name)
        self.setData()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


def exportFit(path=None):
    """Export joints data as yaml fils"""
    path = choseFile(path=path, dialogStyle=2, caption="Export joint", fileFilter="YAML file(*.yaml)", startingDirectory=DEFAULT_FIT_DIR)
    if path is None:
        return

    if not cmds.objExists(FIT_ROOT):
        raise RuntimeWarning("Can find {0}".format(FIT_ROOT))

    export_list = []
    for bone, boneDag in hierarchyIter(FIT_ROOT):
        if bone == FIT_ROOT:
            continue
        data = JointData(bone)
        if SET_SEGMENT_SCALE_COMPENSATE_FALSE_FORCE:
            data.segmentScaleCompensate = False
        export_list.append(data)

    with open(path, "w") as f:
        yaml.dump(export_list, f, indent=4, width=80)
    showMessage(" Export fit successful ")


def importFit(path=None):
    """Import joints data from yaml files"""
    path = choseFile(path=path, dialogStyle=2, caption="Import joint", fileFilter="YAML file(*.yaml)", fileMode=1, startingDirectory=DEFAULT_FIT_DIR)
    if path is None:
        return
    with open(path, "r") as f:
        data_list = yaml.load(f)

    if not cmds.objExists(FIT_ROOT):
        cmds.createNode("transform", name=FIT_ROOT, ss=1)
    for data in data_list:
        if cmds.objExists(data.name):
            cmds.delete(data.name)
        if SET_SEGMENT_SCALE_COMPENSATE_FALSE_FORCE:
            data.segmentScaleCompensate = False
        cmds.createNode("joint", name=data.name, ss=1)
        data.setData()
    cmds.select(FIT_ROOT)
    showMessage(" Import fit successful ")


def mirrorDuplicateTransform(obj):
    """Mirror and duplicate transform or joint"""
    mirror_rootName = cmds.duplicate(obj, rc=1, rr=1)[0]
    source_hierarchyIter = hierarchyIter(root_node=obj, skipShape=True)
    mirror_hierarchyIter = hierarchyIter(root_node=mirror_rootName, skipShape=True)

    for mirror_obj, mirror_dag in mirror_hierarchyIter:
        source, source_dag = source_hierarchyIter.next()
        mirror_obj = MIRROR_CONFIG.exchange(source)[0]
        if cmds.objExists(mirror_obj):
            cmds.delete(mirror_obj)
        cmds.rename(mirror_dag.partialPathName(), mirror_obj)
        flip_transform(source, mirror_obj)


def mirrorDuplicateTransform_cmd(all=False):
    """Command of mirror and duplicate transform or joint"""
    jointList = cmds.ls(sl=1)

    if jointList and all:
        for x in jointList:
            mirrorDuplicateTransform(x)
            return

    all_joint = get_allFitJoint()
    for x in all_joint:
        c = x.split("_")
        if MIRROR_CONFIG.l in c:
            if MIRROR_CONFIG.exchange(x)[0] != x:
                x_parent = (cmds.listRelatives(x, p=1) or ['None'])[0]
                if MIRROR_CONFIG.exchange(x_parent)[0] == x_parent:
                    mirrorDuplicateTransform(x)
    showMessage("Mirror All")


def autoCalClassPosition():
    """Auto cal class joints position"""
    for x, dag in hierarchyIter(FIT_ROOT):
        if "Class" in x:
            children = cmds.listRelatives(x, c=1) or []
            children_joint = []
            position = []
            for c in children:
                if cmds.objectType(c, isAType="transform"):
                    children_joint.append(c)
                    position.append(cmds.xform(c, q=1, t=1, ws=1))
            count = len(position)
            mean = [0, 0, 0]
            for i in range(3):
                s = 0
                for c in position:
                    s += c[i]
                mean[i] = s/count
            class_position = cmds.xform(x, q=1, t=1, ws=1)
            offset = om.MVector(mean) - om.MVector(class_position)
            cmds.move(offset[0], offset[1], offset[2], "{0}.scalePivot".format(x), "{0}.rotatePivot".format(x), r=1)


def isAverageTrue(bool_list):
    average = sum(bool_list) / (len(bool_list) or 1)
    return average >= 0.5


def hideClass():
    """ Hide class joints """
    boolList = []
    for x, dag in hierarchyIter(FIT_ROOT):
        if "Class" in x:
            if cmds.objExists("{0}.drawStyle".format(x)):
                boolList.append(cmds.getAttr("{0}.drawStyle".format(x)))

    for x, dag in hierarchyIter(FIT_ROOT):
        if "Class" in x:
            if cmds.objExists("{0}.drawStyle".format(x)):
                cmds.setAttr("{0}.drawStyle".format(x), 2 if not isAverageTrue(boolList) else 0)
    showMessage("Hide Class Controls")


def hidePart():
    """Hide part joints"""
    boolList = []
    for x, dag in hierarchyIter(FIT_ROOT):
        if "Part" in x:
            if cmds.objExists("{0}.drawStyle".format(x)):
                boolList.append(cmds.getAttr("{0}.drawStyle".format(x)))

    for x, dag in hierarchyIter(FIT_ROOT):
        if "Part" in x:
            if cmds.objExists("{0}.drawStyle".format(x)):
                cmds.setAttr("{0}.drawStyle".format(x), 2 if not isAverageTrue(boolList) else 0)
    showMessage("Hide Part Controls")


def get_allFitJoint():
    """Get all fit joints"""
    joint_list = []
    for x, _ in hierarchyIter(FIT_ROOT):
        isEnd = (END_LABEL in x)
        isRootGroup = (FIT_ROOT == x)
        notJoint = not cmds.objectType(x, isa="joint")
        if isEnd or isRootGroup or notJoint:
            continue
        joint_list.append(x)
    return joint_list


def get_fitJointByLabel(label):
    joint_list = []
    for x, _ in hierarchyIter(FIT_ROOT):
        isEnd = (END_LABEL in x)
        isRootGroup = (FIT_ROOT == x)
        notLabel = not (label in x)
        notJoint = not (cmds.objectType(x, isa="joint"))
        if isEnd or isRootGroup or notJoint or notLabel:
            continue
        joint_list.append(x)
    return joint_list


def get_fitJointByKeyWord(iterList=None, *args):
    if not iterList:
        iterList = get_allFitJoint()
    result_list = []
    for x in iterList:
        if all([arg in x for arg in args]):
            result_list.append(x)
    return result_list
