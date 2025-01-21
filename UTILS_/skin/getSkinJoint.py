from maya import cmds
from UTILS_.getHistory import get_history


def get_skinJoint(obj_list=None):
    if type(obj_list) is str:
        obj_list = [obj_list]
    skin_joint_list = []
    for obj in obj_list:
        if not cmds.objExists(obj):
            continue

        history_list = get_history(obj, 'skinCluster')
        if not history_list:
            skin_joint_list.extend([])
            continue

        for his in history_list:
            skin_joint_list.extend(cmds.skinCluster(his, q=1, inf=1))
    seen = set()
    skin_joint_list = [x for x in skin_joint_list if not (x in seen or seen.add(x))]
    return skin_joint_list


def get_skinJoint_cmd(createSet=False):
    obj_list = cmds.ls(sl=1)
    skin_joint_list = get_skinJoint(obj_list)
    if createSet and skin_joint_list:
        cmds.sets(skin_joint_list, n='skinJointSet')
    cmds.select(skin_joint_list)
    return skin_joint_list


# get_skinJoint_cmd(True)
