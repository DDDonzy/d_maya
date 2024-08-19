import maya.cmds as cmds


def mirrorSelected():
    baseSelected = cmds.ls(sl=1)
    targetSelected = [get_oppositeString(x) for x in baseSelected]
    cmds.select(targetSelected)


mirrorSelected()
