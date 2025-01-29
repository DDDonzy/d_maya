from .createControls import buildControl, JOINT_ROOT
from .hierarchyIter import hierarchyIter
from .fit import get_allFacialJoint

from maya import cmds
from maya.api import OpenMaya as om

UN_SKIN_LABEL = ["class", "end", "part"]


def build():
    all_joint = get_allFacialJoint()
    for x in all_joint:
        buildControl(x)

    removeUnSkinJoints()


def removeUnSkinJoints():
    for x, x_dag in hierarchyIter(JOINT_ROOT):
        if x == JOINT_ROOT:
            continue
        for label in UN_SKIN_LABEL:
            if label in x.lower():
                parent = cmds.listRelatives(x, p=1)[0]
                children_dag = [om.MDagPath.getAPathTo(x_dag.child(x)) for x in range(x_dag.childCount())]
                children = [x.partialPathName() for x in children_dag]
                cmds.parent(children, parent)
                cmds.delete(x)
                break
