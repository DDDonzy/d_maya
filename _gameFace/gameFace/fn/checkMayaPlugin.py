import maya.cmds as cmds


def checkPlugin():
    pluginList = ["matrixNodes", "quatNodes"]
    for plugin in pluginList:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            cmds.loadPlugin(plugin)
