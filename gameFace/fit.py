import yaml
from dataclasses import dataclass, field

from UTILS.transform import get_worldMatrix, set_worldMatrix
from UTILS.ui.showMessage import showMessage
from UTILS.transform import flip_transform
from UTILS.mirrorEnv import MIRROR_CONFIG

from ._config import *
from .hierarchyIter import hierarchyIter


from maya import cmds
from maya.api import OpenMaya as om


@dataclass
class JointData(yaml.YAMLObject):
    yaml_tag = 'JointData'
    name: str
    parent: str = ""
    worldMatrix: list = field(default_factory=list)
    preferredAngle: list = field(default_factory=list)

    rotateOrder: int = 0
    radius: float = 1.0
    drawStyle: int = 0
    segmentScaleCompensate: bool = True
    inheritsTransform: bool = True
    visibility: bool = True

    def __post_init__(self):
        self.getData(name=self.name)

    def getData(self, name):
        self.parent = (cmds.listRelatives(self.name, p=1) or ["kWorld"])[0]
        self.worldMatrix = list(get_worldMatrix(self.name))
        try:
            setattr(self, "preferredAngle", list(cmds.getAttr(f"{self.name}.preferredAngle")[0]))
        except:
            pass
        for attr in ["segmentScaleCompensate",
                     "rotateOrder",
                     "inheritsTransform",
                     "radius",
                     "drawStyle",
                     "visibility"]:
            try:
                setattr(self, attr, cmds.getAttr(f"{self.name}.{attr}"))
            except:
                pass

    def setData(self):
        if self.parent == "kWorld":
            pass
        else:
            try:
                cmds.parent(self.name, self.parent)
            except:
                pass
        set_worldMatrix(self.name, om.MMatrix(self.worldMatrix))
        try:
            cmds.setAttr(f"{self.name}.preferredAngle", *self.preferredAngle)
        except:
            pass
        for attr in ["segmentScaleCompensate",
                     "rotateOrder",
                     "inheritsTransform",
                     "radius",
                     "drawStyle",
                     "visibility"]:
            try:
                cmds.setAttr(f"{self.name}.{attr}", getattr(self, attr))
            except:
                pass


def exportFit(path=None):
    if not path:
        path = (cmds.fileDialog2(dialogStyle=2, caption="Export joint", fileFilter="YAML file(*.yaml)") or [None])[0]
    if not path:
        return

    if not cmds.objExists(FIT_ROOT):
        raise RuntimeWarning(f"Can find {FIT_ROOT}")

    export_list = []
    for bone, boneDag in hierarchyIter(FIT_ROOT):
        if bone == FIT_ROOT:
            continue
        export_list.append(JointData(bone))

    with open(path, "w") as f:
        yaml.dump(export_list, f, sort_keys=False, indent=4, width=80)
    showMessage(" Export successful ")


def importFit(path=None):
    if not path:
        path = (cmds.fileDialog2(dialogStyle=2, caption="Import joint", fileFilter="YAML file(*.yaml)", fileMode=1) or [None])[0]
    if not path:
        return

    with open(path, "r") as f:
        data_list = yaml.unsafe_load(f)

    if not cmds.objExists(FIT_ROOT):
        cmds.createNode("transform", name=FIT_ROOT, ss=1)
    for bone in data_list:
        if cmds.objExists(bone.name):
            cmds.delete(bone.name)
        cmds.createNode("joint", name=bone.name, ss=1)
        bone.setData()
    cmds.select(FIT_ROOT)


def get_allFitJoint():
    joint_list = []
    for x, _ in hierarchyIter(FIT_ROOT):
        isEnd = (END_LABEL in x)
        isRootGroup = (FIT_ROOT == x)
        notJoint = ("joint" != cmds.objectType(x))
        if isEnd or isRootGroup or notJoint:
            continue
        joint_list.append(x)
    return joint_list


def mirrorDuplicateTransform(obj):
    mirror_rootName = cmds.duplicate(obj, rc=1, rr=1)[0]
    source_hierarchyIter = hierarchyIter(root_node=obj, skipShape=True)
    mirror_hierarchyIter = hierarchyIter(root_node=mirror_rootName, skipShape=True)

    for mirror_obj, mirror_dag in mirror_hierarchyIter:
        source, source_dag = source_hierarchyIter.__next__()
        mirror_obj = MIRROR_CONFIG.exchange(source)[0]
        if cmds.objExists(mirror_obj):
            cmds.delete(mirror_obj)
        cmds.rename(mirror_dag.partialPathName(), mirror_obj)
        flip_transform(source, mirror_obj)


def mirrorDuplicateTransform_cmd(all=False):
    jointList = cmds.ls(sl=1)

    if jointList and all:
        for x in jointList:
            mirrorDuplicateTransform(x)
            return

    all_joint = get_allFitJoint()
    for x in all_joint:
        if MIRROR_CONFIG.l in x:
            if MIRROR_CONFIG.exchange(x)[0] != x:
                x_parent = (cmds.listRelatives(x, p=1) or ['None'])[0]
                if MIRROR_CONFIG.exchange(x_parent)[0] == x_parent:
                    mirrorDuplicateTransform(x)


def autoCalClassPosition():
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
            cmds.move(*offset, f"{x}.scalePivot", f"{x}.rotatePivot", r=1)


def isAverageTrue(bool_list):
    average = sum(bool_list) / (len(bool_list) or 1)
    return average >= 0.5


def hideClass():
    boolList = []
    for x, dag in hierarchyIter(FIT_ROOT):
        if "Class" in x:
            if cmds.objExists(f"{x}.drawStyle"):
                boolList.append(cmds.getAttr(f"{x}.drawStyle"))

    for x, dag in hierarchyIter(FIT_ROOT):
        if "Class" in x:
            if cmds.objExists(f"{x}.drawStyle"):
                cmds.setAttr(f"{x}.drawStyle", 2 if not isAverageTrue(boolList) else 0)


def hidePart():
    boolList = []
    for x, dag in hierarchyIter(FIT_ROOT):
        if "Part" in x:
            if cmds.objExists(f"{x}.drawStyle"):
                boolList.append(cmds.getAttr(f"{x}.drawStyle"))

    for x, dag in hierarchyIter(FIT_ROOT):
        if "Part" in x:
            if cmds.objExists(f"{x}.drawStyle"):
                cmds.setAttr(f"{x}.drawStyle", 2 if not isAverageTrue(boolList) else 0)


def addPartJoint(force=False):
    for part, ref in PART_JOINT.items():
        if cmds.objExists(part):
            if force:
                cmds.delete(part)
            continue

        cmds.createNode("joint", name=part, ss=1)
        ref_data = JointData(ref)
        part_data = ref_data
        part_data.name = part
        part_data.radius *= 2
        part_data.setData()
