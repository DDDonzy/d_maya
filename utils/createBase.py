from maya.api import OpenMaya as om
from maya import cmds


def CreateNode(*args, **kwargs):
    kwargs.update({"skipSelect": True})
    return cmds.createNode(*args, **kwargs)


class AssetCallBack:
    callBack_instance = []

    def __init__(self,
                 name: str = "",
                 assetType: str = "container",
                 blackBox: bool = False,
                 icon: str = None,
                 publishAttrData: dict = {}):
        self.name = name
        self.addNode: list[str] = []

        self.assetType = assetType
        self.blackBox = blackBox
        self.icon = icon
        self.publishAttrData = publishAttrData

        self.addCallBackID: int = 0
        self.removeCallBackID: int = 0

    def __repr__(self):
        return str(self.name)

    def __enter__(self):
        self.addCallBack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.removeNodeCallBack()
        AssetCallBack.createContainer(name=self.name,
                                      assetType=self.assetType,
                                      addNode=self.addNode,
                                      blackBox=self.blackBox,
                                      publishAttrData=self.publishAttrData)

    def addCallBack(self):
        self.base_callBack_instance: list[AssetCallBack] = AssetCallBack.callBack_instance.copy()
        for baseCallback in AssetCallBack.callBack_instance:
            om.MMessage.removeCallback(baseCallback.addCallBackID)
            om.MMessage.removeCallback(baseCallback.removeCallBackID)

        self.addCallBackID = om.MDGMessage.addNodeAddedCallback(AssetCallBack.addNodeFunction, "dependNode", self)
        self.removeCallBackID = om.MDGMessage.addNodeRemovedCallback(AssetCallBack.removeNodeFunction, "dependNode", self)
        AssetCallBack.callBack_instance.append(self)

    def removeNodeCallBack(self):
        om.MMessage.removeCallback(self.addCallBackID)
        om.MMessage.removeCallback(self.removeCallBackID)
        AssetCallBack.callBack_instance.remove(self)

        for baseCallback in self.base_callBack_instance:
            baseCallback.addCallBackID = om.MDGMessage.addNodeAddedCallback(AssetCallBack.addNodeFunction, "dependNode", baseCallback)
            baseCallback.removeCallBackID = om.MDGMessage.addNodeRemovedCallback(AssetCallBack.removeNodeFunction, "dependNode", baseCallback)

    @staticmethod
    def addNodeFunction(mObj, thisClass):
        node = om.MFnDependencyNode(mObj)
        node_name = node.name()
        thisClass.addNode.append(node_name)

    @staticmethod
    def removeNodeFunction(mObj, thisClass):
        node = om.MFnDependencyNode(mObj)
        node_name = node.name()
        thisClass.addNode.remove(node_name)

    @staticmethod
    def createContainer(name: str,
                        assetType: str = 'dagContainer',
                        addNode: list = [],
                        blackBox: bool = False,
                        icon: str = None,
                        publishAttrData: dict = None):

        container = cmds.createNode(assetType, name=name, ss=1)
        cmds.container(container, e=1, an=addNode)
        cmds.setAttr(f"{container}.blackBox", blackBox) if blackBox else None
        cmds.setAttr(f"{container}.iconName", icon) if icon else None
        cmds.setAttr(f"{container}.viewMode", 0)
        if publishAttrData:
            AssetCallBack.publishAssetAttr(name=container, publishAttrData=publishAttrData)

    @staticmethod
    def publishAssetAttr(name: str = None, publishAttrData: dict = None):
        if publishAttrData and isinstance(publishAttrData, dict):
            for k, v in publishAttrData.items():
                cmds.container(name, e=1, publishAndBind=[v, k])


class CreatorBase():
    creatorType: str = "RigAsset"
    isDagAsset: bool = True
    blackBox: bool = False
    icon: str = None
    publishAttrData: dict = {}

    def __init__(self, name='noName'):
        self._pre_init()

        self.name: str = name
        self.__assetType: str = ("container", "dagContainer")[self.isDagAsset]

        self.__build()
        self._post_init()

    def _pre_init(self):
        pass

    def _post_init(self):
        pass

    def __build(self):

        with AssetCallBack(name=self.name,
                           assetType=self.__assetType,
                           blackBox=self.blackBox,
                           icon=self.icon,
                           publishAttrData=self.publishAttrData) as self.asset:
            self.create()

    def create(self):
        raise NotImplementedError("Subclass must implement this method")


class b(CreatorBase):
    creatorType: str = "base"
    isDagAsset: bool = True
    blackBox: bool = False
    icon: str = None

    def create(self):
        CreateNode("transform")


b_ = b("testName")
