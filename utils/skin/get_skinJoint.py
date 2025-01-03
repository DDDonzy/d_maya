from maya import cmds


def get_history(obj, type=None):
    out_list = []
    if not cmds.objExists(obj):
        return out_list
    history_list = cmds.listHistory(obj, pdo=1, il=1)
    if not history_list:
        return out_list

    if type:
        for his in history_list:
            if cmds.objectType(his, i=type):
                out_list.append(his)
    return out_list


def get_skin_joint(obj_list=None):
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


def get_skin_joint_cmd(createSet=False):
    obj_list = cmds.ls(sl=1)
    skin_joint_list = get_skin_joint(obj_list)
    if createSet and skin_joint_list:
        cmds.sets(skin_joint_list, n='skinJointSet')
    cmds.select(skin_joint_list)
    return skin_joint_list


# get_skin_joint_cmd(True)
