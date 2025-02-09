from dataclasses import dataclass
from UTILS.create.createBase import CreateNode
from UTILS.transform import matrixConstraint, alignTransform

from gameFace.fit import JointData
from gameFace.data.config import *
from gameFace.hierarchyIter import *


from maya import cmds, mel


@dataclass
class ControlData():
    name: str

    def __post_init__(self):
        self.update()

    def update(self):
        split_list = self.name.split("_")
        for x in SUFFIX_LIST:
            if x in split_list:
                split_list.remove(x)
        self.name = "_".join(split_list)

    @property
    def sk(self):
        return self.getObject(SKIN_JOINT_LABEL)

    @property
    def fit(self):
        return self.name

    @property
    def grp(self):
        return self.getObject(GRP_LABEL)

    @property
    def sdk(self):
        return self.getObject(SDK_LABEL)

    @property
    def ctl(self):
        return self.getObject(CTL_LABEL)

    @property
    def loc(self):
        return self.getObject(LOC_LABEL)

    def getObject(self, label):
        obj = f"{self.name}_{label}"
        if cmds.objExists(obj):
            return obj
        else:
            return None


def addDefaultShape(obj):
    """Add a shape"""
    shape = CreateNode("nurbsCurve", name=f"{obj}Shape", parent=obj)
    shapeCmd = f'setAttr "{shape}.create" -type "nurbsCurve" 1 7 0 no 3 8 0 1 2 3 4 5 6 7 8 -0.5 0 0 0.5 0 0 0 0 0 0 0 0.5 0 0 -0.5 0 0 0 0 0.5 0 0 -0.5 0;'
    cmds.setAttr(f"{shape}.overrideColor", 31)
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.lineWidth", 3)
    mel.eval(shapeCmd)


def addParentTransform(obj, name=None):
    """Add controls parent group"""
    if not name:
        name = f"{obj}_add"
    transform = CreateNode("transform", name=name)
    parent = (cmds.listRelatives(obj, parent=1) or ["kWorld"])[0]
    if cmds.objExists(parent):
        cmds.parent(transform, parent)
    alignTransform(obj, transform)
    cmds.parent(obj, transform)
    return transform


def addControlHierarchy(obj, hierarchyList=[], replace=""):
    """Add controls hierarchy"""
    for x in hierarchyList:
        if replace:
            name = obj.replace(replace, x)
        else:
            name = f"{obj}_{x}"
        transform = addParentTransform(obj, name=name)
        # if controls add a shapes
        if x == CTL_LABEL:
            addDefaultShape(transform)


def buildControl(obj, hierarchyList=CONTROL_HIERARCHY_LIST):
    """Build controls"""
    # controls
    if not cmds.objExists(CONTROL_ROOT):
        CreateNode("transform", name=CONTROL_ROOT)
    parent = f"{(cmds.listRelatives(obj, p=1) or ['None'])[0]}_{CTL_LABEL}"
    if not cmds.objExists(parent):
        parent = CONTROL_ROOT
    loc = CreateNode("transform", name=f"{obj}_{LOC_LABEL}", parent=parent)
    alignTransform(obj, loc)
    addControlHierarchy(loc, hierarchyList=hierarchyList, replace=LOC_LABEL)

    # joint
    if not cmds.objExists(SKIN_JOINT_ROOT):
        CreateNode("transform", name=SKIN_JOINT_ROOT)
    parent = f"{(cmds.listRelatives(obj, p=1) or ['None'])[0]}_{SKIN_JOINT_LABEL}"
    if not cmds.objExists(parent):
        parent = SKIN_JOINT_ROOT
    joint = CreateNode("joint", name=f"{obj}_{SKIN_JOINT_LABEL}")

    joint_data = JointData(joint)
    fit_joint_data = JointData(obj)
    fit_joint_data.name = joint_data.name
    fit_joint_data.parent = parent
    fit_joint_data.setData()
    matrixConstraint(loc, joint)


def get_allSkinJoint():
    """Get all skin joints"""
    joint_list = []
    for x, _ in hierarchyIter(SKIN_JOINT_ROOT):
        isEnd = (END_LABEL in x)
        isRootGroup = (SKIN_JOINT_ROOT == x)
        notJoint = not cmds.objectType(x, isa="joint")
        if isEnd or isRootGroup or notJoint:
            continue
        joint_list.append(x)
    return joint_list


def get_allControls():
    """Get all controls"""
    controls_list = []
    for x, _ in hierarchyIter(CONTROL_ROOT):
        isRootGroup = (CONTROL_ROOT == x)
        notLoc = (LOC_LABEL not in x)
        notTransform = not cmds.objectType(x, isa="transform")
        if notLoc or isRootGroup or notTransform:
            continue
        controls_list.append(ControlData(x))
    return controls_list


def get_controlsByLabel(label):
    """Get all controls from label str"""
    controls_list = []
    for x, _ in hierarchyIter(CONTROL_ROOT):
        isRootGroup = (CONTROL_ROOT == x)
        notLabel = (label not in x)
        notLoc = (LOC_LABEL not in x)
        notTransform = not cmds.objectType(x, isa="transform")
        if notLabel or isRootGroup or notTransform or notLoc:
            continue
        controls_list.append(ControlData(x))
    return controls_list
