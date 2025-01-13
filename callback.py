import maya.api.OpenMaya as om
from maya import cmds
from functools import partial
partial(printObject(self))


class D_CallBack():
    callBack_instance = []

    def __init__(self):
        print("create!")

        self.addObject = []
        self.addID = 0
        self.removeID = 0

        self.base_callBack_instance = D_CallBack.callBack_instance.copy()
        for callback in D_CallBack.callBack_instance:
            om.MMessage.removeCallback(callback.addID)
            om.MMessage.removeCallback(callback.removeID)
            D_CallBack.callBack_instance.remove(callback)

        self.addID = om.MDGMessage.addNodeAddedCallback(partial(printObject, extra_param=self), "dependNode")

        self.removeID = om.MDGMessage.addNodeRemovedCallback(removePrintObject, "dependNode")
        # D_CallBack.callBack_instance.append(self)

    def __del__(self):
        print("del")
        self.removeNodeCallBack()

    def removeNodeCallBack(self):
        print("delete!")
        om.MMessage.removeCallback(self.addID)
        om.MMessage.removeCallback(self.removeID)
        # D_CallBack.callBack_instance.remove(self)
        for callback in self.base_callBack_instance:
            callback.addID = om.MDGMessage.addNodeAddedCallback(printObject, "dependNode")
            callback.removeID = om.MDGMessage.addNodeRemovedCallback(removePrintObject, "dependNode")
            D_CallBack.callBack_instance.append(callback)


def printObject(mObj, clientData):
    node = om.MFnDependencyNode(mObj)
    node_name = node.name()
    print("CREATE:", node_name)


def removePrintObject(mObj, clientData):
    node = om.MFnDependencyNode(mObj)
    node_name = node.name()
    print("REMOVE:", node_name)
