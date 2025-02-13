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
