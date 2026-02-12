from maya import cmds
from maya.api import OpenMaya as om

import log
from m_utils.dag.getHistory import get_history
from m_utils.transform import set_worldMatrix


def go_to_bind_pose(sel: list = None):
    if not sel:
        sel = cmds.ls(sl=1)

    if not sel:
        log.error("Please input selection list or selected some objects.")
        return

    for x in sel:
        skin_node = get_history(x, type="skinCluster")
        if not skin_node:
            continue
        skin_node = skin_node[0]
        indices = cmds.getAttr(f"{skin_node}.matrix", mi=1)
        for i in indices:
            bones = cmds.listConnections(f"{skin_node}.matrix[{i}]", s=1, d=0)[0]
            matrix: om.MMatrix = om.MMatrix(cmds.getAttr(f"{skin_node}.bindPreMatrix[{i}]"))
            set_worldMatrix(bones, matrix.inverse())
        log.success(f"'{x}' Go to bind pose!")


if __name__ == "__main__":
    go_to_bind_pose()
