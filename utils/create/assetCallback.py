# import maya.standalone
# maya.standalone.initialize()

from maya.api import OpenMaya as om


class AssetCallback:
    currentInstance = None
    instanceAll = []
    addCallbackID = 0
    removeCallbackID = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.delete()
        for mObj in self.addNodeMObj:
            fnDep = om.MFnDependencyNode(mObj)
            self.addNode.append(fnDep.name())

    def __init__(self, name):

        if AssetCallback.currentInstance:
            AssetCallback.currentInstance.stop()
        self.lasterCallBack = AssetCallback.currentInstance

        AssetCallback.currentInstance = self
        AssetCallback.instanceAll.append(self)

        self.name = name
        self.status = False
        self.addNodeMObj: list[str] = []
        self.addNode: list[str] = []
        self.start()

    def start(self):
        AssetCallback.addCallbackID = om.MDGMessage.addNodeAddedCallback(AssetCallback.addNodeFunction, "dependNode", self)
        AssetCallback.removeCallbackID = om.MDGMessage.addNodeRemovedCallback(AssetCallback.removeNodeFunction, "dependNode", self)
        self.status = True

    def stop(self):
        if AssetCallback.addCallbackID:
            om.MMessage.removeCallback(AssetCallback.addCallbackID)
            AssetCallback.addCallbackID = 0
        if AssetCallback.removeCallbackID:
            om.MMessage.removeCallback(AssetCallback.removeCallbackID)
            AssetCallback.removeCallbackID = 0
        self.status = False

    def delete(self):
        self.stop()
        AssetCallback.instanceAll.remove(self)
        AssetCallback.currentInstance = self.lasterCallBack
        if AssetCallback.currentInstance:
            self.lasterCallBack.start()

    @staticmethod
    def deleteAll():
        for x in AssetCallback.instanceAll:
            x.delete()

    @staticmethod
    def addNodeFunction(mObj, thisClass):
        if mObj.apiTypeStr != "kHyperLayout":
            thisClass.addNodeMObj.append(mObj)

    @staticmethod
    def removeNodeFunction(mObj, thisClass):
        if mObj in thisClass.addNodeMObj:
            thisClass.addNodeMObj.remove(mObj)


# with AssetCallBack("A:") as call:
#     cmds.polyCube()
