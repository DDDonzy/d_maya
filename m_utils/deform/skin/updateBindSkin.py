from maya import cmds
from mutils.dag.getHistory import get_history


def updateBindSkin(node_skin):
    mult_index = cmds.getAttr(f"{node_skin}.matrix", mi=1)
    for i in mult_index:
        inf = cmds.listConnections(f"{node_skin}.matrix[{i}]", s=1, d=0)[0]
        inf_pre_matrix = cmds.getAttr(f"{inf}.worldInverseMatrix[0]")
        cmds.setAttr(f"{node_skin}.bindPreMatrix[{i}]", inf_pre_matrix, type="matrix")
    print(f"UPDATE BIND SKIN: {node_skin}")


def updateBindSkin_cmd(obj=None):
    if not obj:
        sel = cmds.ls(sl=1)
    for obj in sel:
        if cmds.objectType(obj) == "skinCluster":
            updateBindSkin(obj)
        else:
            skinCluster_list = get_history(obj, "skinCluster")
            for sk in skinCluster_list:
                updateBindSkin(sk)


if __name__ == "__main__":
    updateBindSkin_cmd()
