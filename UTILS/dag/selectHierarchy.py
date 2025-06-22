from UTILS.dag.iterHierarchy import IterHierarchy
from maya import cmds


def selectHierarchy_cmd():
    """
    Select all children of the selected object(s) in the Maya scene.
    """
    sel = cmds.ls(sl=1, type="transform")
    obj_list = []
    for x in sel:
        for name, dag in IterHierarchy(x, False):
            obj_list.append(name)

    cmds.select(obj_list)

if __name__ == "__main__":
    selectHierarchy_cmd()