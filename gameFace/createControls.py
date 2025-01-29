
from UTILS.create.createBase import CreateNode
from UTILS.transform import get_worldMatrix, set_worldMatrix, get_localMatrix, set_localMatrix, matrixConstraint, alignTransform
from UTILS.create.generateUniqueName import generateUniqueName

from .fit import get_allFacialJoint, JointData

from maya import cmds, mel

CONTROL_LABEL_LIST = ["controls", "ctrl", "ctl"]

CTL_LABEL = "CTL"
SDK_LABEL = "SDK"
GRP_LABEL = "GRP"
LOC_LABEL = "LOC"
JOINT_LABEL = "SK"

CONTROL_ROOT = "Controls_GRP"
JOINT_ROOT = "SkinJoint_GRP"


def addDefaultShape(obj):
    shape = CreateNode("nurbsCurve", name=f"{obj}Shape", parent=obj)
    shapeCmd = f'setAttr "{shape}.create" -type "nurbsCurve" 1 7 0 no 3 8 0 1 2 3 4 5 6 7 8 -0.5 0 0 0.5 0 0 0 0 0 0 0 0.5 0 0 -0.5 0 0 0 0 0.5 0 0 -0.5 0;'
    cmds.setAttr(f"{shape}.overrideColor", 31)
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.lineWidth", 3)
    mel.eval(shapeCmd)


def addParentTransform(obj, name=None):
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
    for x in hierarchyList:
        if replace:
            name = obj.replace(replace, x)
        else:
            name = f"{obj}_{x}"
        transform = addParentTransform(obj, name=name)
        if x.lower() in CONTROL_LABEL_LIST:
            addDefaultShape(transform)


def buildControl(obj, hierarchyList=[GRP_LABEL, SDK_LABEL, CTL_LABEL]):
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
    if not cmds.objExists(JOINT_ROOT):
        CreateNode("transform", name=JOINT_ROOT)
    parent = f"{(cmds.listRelatives(obj, p=1) or ['None'])[0]}_{JOINT_LABEL}"
    if not cmds.objExists(parent):
        parent = JOINT_ROOT
    joint = CreateNode("joint", name=f"{obj}_{JOINT_LABEL}")

    joint_data = JointData(joint)
    fit_joint_data = JointData(obj)
    fit_joint_data.name = joint_data.name
    fit_joint_data.parent = parent
    fit_joint_data.setData()
    matrixConstraint(loc, joint)
