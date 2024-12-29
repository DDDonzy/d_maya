from maya import cmds


def get_history_by_type(obj, his_type):
    if type(his_type) is str:
        his_type = [his_type]

    history_list = cmds.listHistory(obj, pdo=1, il=1)
    if not history_list:
        raise RuntimeError(f"{obj} do not have history !")

    out_list = []
    for his in history_list:
        if cmds.objectType(his) in his_type:
            out_list.append(his)

    return out_list


def update_bind_skin(node_skin):
    mult_index = cmds.getAttr(f"{node_skin}.matrix", mi=1)
    for i in mult_index:
        inf = cmds.listConnections(f"{node_skin}.matrix[{i}]", s=1, d=0)[0]
        inf_pre_matrix = cmds.getAttr(f"{inf}.worldInverseMatrix[0]")
        cmds.setAttr(f"{node_skin}.bindPreMatrix[{i}]", inf_pre_matrix, type="matrix")
    print(f"UPDATE BIND SKIN: {node_skin}")


def update_bind_skin_cmd(obj=None):
    if not obj:
        sel = cmds.ls(sl=1)
    for obj in sel:
        if cmds.objectType(obj) == "skinCluster":
            update_bind_skin(obj)
        else:
            skinCluster_list = get_history_by_type(obj, "skinCluster")
            for sk in skinCluster_list:
                update_bind_skin(sk)


update_bind_skin_cmd()
