import maya.api.OpenMaya as om
from maya import cmds
obj_list = []


def printObject(mObj, clientData):
    node = om.MFnDependencyNode(mObj)
    node_name = node.name()
    print("CREATE:", node_name)
    obj_list.append(node_name)


def removeprintObject(mObj, clientData):
    node = om.MFnDependencyNode(mObj)
    node_name = node.name()
    print("REMOVE:", node_name)
    obj_list.remove(node_name)


addCallbackID = om.MDGMessage.addNodeAddedCallback(printObject, "dependNode")
removeCallbackID = om.MDGMessage.addNodeRemovedCallback(removeprintObject, "dependNode")

try:
    cmds.createNode("transform", name="yes")
finally:
    om.MMessage.removeCallback(addCallbackID)
    om.MMessage.removeCallback(removeCallbackID)
