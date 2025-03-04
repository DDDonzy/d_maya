from face.data.config import *

from face.fn.getHistory import get_history
from face.fn.choseFile import choseFile
from face.fn.showMessage import showMessage
from face.fn.createBase import CreateNode, CreateBase
from face.fn.transform import matrixConstraint, alignTransform
from face.fn.bsData import add_bsTarget

from face.fit import JointData, get_fitJointByKeyWord
from face.fn.hierarchyIter import hierarchyIter

from maya import cmds, mel
import yaml


class BridgeData(yaml.YAMLObject):
    yaml_tag = 'BridgeData'

    def __init__(self, name, driverAttr=None, min=0, max=1):
        self.name = name
        self.driverAttr = driverAttr
        self.min = min
        self.max = max

    def __str__(self):
        return self.name


class ControlData(object):
    def __init__(self, name):
        self.name = name
        self.update()

    def update(self):
        split_list = self.name.split("_")
        if split_list[-1] in ALL_LABEL:
            self.name = "_".join(split_list[0:-1])
        else:
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
        obj = "{}_{}".format(self.name, label)
        if cmds.objExists(obj):
            return obj
        else:
            return None


def addDefaultShape(obj):
    """Add a shape"""
    shape = CreateNode("nurbsCurve", name="{}Shape".format(obj), parent=obj)
    shapeCmd = 'setAttr "{}.create" -type "nurbsCurve" 1 7 0 no 3 8 0 1 2 3 4 5 6 7 8 -0.5 0 0 0.5 0 0 0 0 0 0 0 0.5 0 0 -0.5 0 0 0 0 0.5 0 0 -0.5 0;'.format(
        shape)
    cmds.setAttr("{}.overrideColor".format(shape), 31)
    cmds.setAttr("{}.overrideEnabled".format(shape), 1)
    cmds.setAttr("{}.lineWidth".format(shape), 3)
    mel.eval(shapeCmd)


def addParentTransform(obj, name=None):
    """Add controls parent group"""
    if not name:
        name = "{}_add".format(obj)
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
            name = "{}_{}".format(obj, x)
        transform = addParentTransform(obj, name=name)
        # if controls add a shapes
        if x == CTL_LABEL:
            addDefaultShape(transform)


def buildControl(obj, hierarchyList=CONTROL_HIERARCHY_LIST):
    """Build controls"""
    # controls
    if not cmds.objExists(CONTROL_ROOT):
        CreateNode("transform", name=CONTROL_ROOT)
    parent = "{}_{}".format((cmds.listRelatives(obj, p=1) or ['None'])[0], CTL_LABEL)
    if not cmds.objExists(parent):
        parent = CONTROL_ROOT
    loc = CreateNode("transform", name="{}_{}".format(obj, LOC_LABEL), parent=parent)
    alignTransform(obj, loc)
    addControlHierarchy(loc, hierarchyList=hierarchyList, replace=LOC_LABEL)

    # joint
    if not cmds.objExists(SKIN_JOINT_ROOT):
        CreateNode("transform", name=SKIN_JOINT_ROOT)
    parent = "{}_{}".format((cmds.listRelatives(obj, p=1) or ['None'])[0], SKIN_JOINT_LABEL)
    if not cmds.objExists(parent):
        parent = SKIN_JOINT_ROOT
    joint = CreateNode("joint", name="{}_{}".format(obj, SKIN_JOINT_LABEL))

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


class ControlPanel(CreateBase):
    isDagAsset = False
    isBlackBox = False

    @staticmethod
    def exportBridgeData(data, path=None):
        path = choseFile(path, dialogStyle=2, caption="Export SDK", fileFilter="SDK YAML file(*.sdk)", startingDirectory=DEFAULT_SDK_DIR)
        if not path:
            return
        with open(path, "w") as f:
            yaml.dump(data, f, indent=4, width=80)
        showMessage("Export SDK.")

    @staticmethod
    def importBridgeData(path=None):
        path = choseFile(path, dialogStyle=2, caption="Import weights", fileFilter="SDK YAML file(*.sdk)", fileMode=1, startingDirectory=DEFAULT_SDK_DIR)
        if not path:
            return
        with open(path, "r") as f:
            data = yaml.load(f)
        showMessage("Import SDK.")
        return data

    def _pre_create(self):
        self.thisAssetName = BRIDGE
        if cmds.objExists(BRIDGE):
            cmds.delete(BRIDGE)

    def create(self):
        with open(CONTROLS_PANEL_FILE, "r") as f:
            mel.eval(f.read())
        # import pose data
        data = ControlPanel.importBridgeData(DEFAULT_SDK_FILE)
        meshStr = cmds.getAttr("{}.notes".format(FACE_ROOT))
        mesh = yaml.load(meshStr)["uvPin"]
        self.setSDK(data=data, mesh=mesh)

    def setSDK(self, data, mesh):
        self.data = data
        if isinstance(mesh, str):
            mesh = [mesh]
        self.mesh = mesh

        bridge_list = []
        for x in self.data:
            cmds.addAttr(self.thisAssetName, ln=x.name, at="double", dv=0, k=1)
            attr_name = "{}.{}".format(self.thisAssetName, x.name)
            bridge_list.append(attr_name)

            if not x.driverAttr:
                continue
            if not cmds.objExists(x.driverAttr):
                continue

            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.min, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setDrivenKeyframe(attr_name, cd=x.driverAttr, dv=x.max, v=1, inTangentType="linear", outTangentType="linear")

        for _mesh in self.mesh:
            check_bs = get_history(_mesh, "blendShape")
            if check_bs:
                cmds.delete(check_bs)

            bsNode = cmds.blendShape(_mesh, name="{}_bs".format(_mesh), foc=1, tc=0)[0]
            for i, x in enumerate(self.data):
                bs_attr = add_bsTarget(bsNode, x.name)

                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=0, v=0, inTangentType="linear", outTangentType="linear")
                cmds.setDrivenKeyframe(bs_attr, cd=bridge_list[i], dv=1, v=1, inTangentType="linear", outTangentType="linear")
        try:
            cmds.addAttr(BRIDGE, ln="notes", dt="string")
        except:
            pass
        info = self.data
        infoStr = yaml.dump(info, indent=4, width=80)
        cmds.setAttr("{}.notes".format(BRIDGE), infoStr, type="string")


def get_lid(lr="L_", ud="Upper"):
    return [ControlData(x) for x in get_fitJointByKeyWord(lr, "Lid", "Inner", "Sec") + get_fitJointByKeyWord(lr, "Lid", ud, "Sec") + get_fitJointByKeyWord(lr, "Lid", "Outer", "Sec")]


def get_lip(ud="Upper"):
    r = get_fitJointByKeyWord("R_", "Lip", ud, "Sec")
    r.reverse()
    return [ControlData(x) for x in get_fitJointByKeyWord("R_", "Lip", "Corner", "Sec") + r + get_fitJointByKeyWord("M_", "Lip", ud, "Sec") + get_fitJointByKeyWord("L_", "Lip", ud, "Sec") + get_fitJointByKeyWord("L_", "Lip", "Corner", "Sec")]


def get_cheek(lr="L_", ud="Upper"):
    return [ControlData(x) for x in get_fitJointByKeyWord(lr, "Cheek", "Sec", ud)]


def get_brow(lr="L_"):
    return [ControlData(x) for x in get_fitJointByKeyWord(lr, "Brow", "Sec")]


def get_eyeLine(lr="L_"):
    return [ControlData(x) for x in get_fitJointByKeyWord(lr, "EyeLine", "Sec")]
