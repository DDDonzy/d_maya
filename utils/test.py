# import maya.standalone
# maya.standalone.initialize()

from maya import cmds
from maya.api import OpenMaya as om


class AssetCallBack:
    currentInstance = None
    instanceAll = []
    addCallbackID = 0
    removeCallbackID = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.delete()
        print(self.addNode)

    def __init__(self, name):

        if AssetCallBack.currentInstance:
            AssetCallBack.currentInstance.stop()
        self.lasterCallBack = AssetCallBack.currentInstance

        AssetCallBack.currentInstance = self
        AssetCallBack.instanceAll.append(self)

        self.name = name
        self.status = False
        self.addNode: list[str] = []
        self.start()

    def start(self):
        AssetCallBack.addCallbackID = om.MDGMessage.addNodeAddedCallback(AssetCallBack.addNodeFunction, "dependNode", self)
        AssetCallBack.removeCallbackID = om.MDGMessage.addNodeRemovedCallback(AssetCallBack.removeNodeFunction, "dependNode", self)
        self.status = True

    def stop(self):
        if AssetCallBack.addCallbackID:
            om.MMessage.removeCallback(AssetCallBack.addCallbackID)
            AssetCallBack.addCallbackID = 0
        if AssetCallBack.removeCallbackID:
            om.MMessage.removeCallback(AssetCallBack.removeCallbackID)
            AssetCallBack.removeCallbackID = 0
        self.status = False

    def delete(self):
        self.stop()
        AssetCallBack.instanceAll.remove(self)
        AssetCallBack.currentInstance = self.lasterCallBack
        if AssetCallBack.currentInstance:
            self.lasterCallBack.start()

    @staticmethod
    def deleteAll():
        for x in AssetCallBack.instanceAll:
            x.delete()

    @staticmethod
    def addNodeFunction(mObj, thisClass):
        node = om.MFnDependencyNode(mObj)
        node_name = node.name()
        thisClass.addNode.append(node_name)
        print(thisClass.name, node_name)

    @staticmethod
    def removeNodeFunction(mObj, thisClass):
        node = om.MFnDependencyNode(mObj)
        node_name = node.name()
        if node_name in thisClass.addNode:
            thisClass.addNode.remove(node_name)
        print(thisClass.name, node_name)


# with AssetCallBack("A:") as call:
#     cmds.polyCube()
