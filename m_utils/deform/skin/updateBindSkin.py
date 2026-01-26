from maya import cmds
from m_utils.dag.getHistory import get_history
from m_utils.apiundo import commit

import log


def updateBindSkin(node_skin):
    mult_index = cmds.getAttr(f"{node_skin}.matrix", mi=1)
    old_pre_matrix = {}
    new_pre_matrix = {}

    for i in mult_index:
        inf = cmds.listConnections(f"{node_skin}.matrix[{i}]", s=1, d=0)[0]
        new_pre_matrix.update({i: cmds.getAttr(f"{inf}.worldInverseMatrix[0]")})
        old_pre_matrix.update({i: cmds.getAttr(f"{node_skin}.bindPreMatrix[{i}]")})

    def _undo():
        for i, inf_pre_matrix in old_pre_matrix.items():
            cmds.setAttr(f"{node_skin}.bindPreMatrix[{i}]", inf_pre_matrix, type="matrix")
            log.trace(f"UNDO BIND SKIN: {node_skin}.bindPreMatrix[{i}] ---> {inf_pre_matrix}")

    def _doit():
        for i, inf_pre_matrix in new_pre_matrix.items():
            cmds.setAttr(f"{node_skin}.bindPreMatrix[{i}]", inf_pre_matrix, type="matrix")
            log.trace(f"UPDATE BIND SKIN: {node_skin}.bindPreMatrix[{i}] ---> {inf_pre_matrix}")

    commit(_undo, _doit)
    _doit()
    log.success(f"UPDATE BIND SKIN: {node_skin}")


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
