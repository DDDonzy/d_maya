import maya.cmds as cmds


cmds.listRelatives("pSphere1", children=True)
cmds.ls(selection=True, long=True)
