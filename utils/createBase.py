from maya.api import OpenMaya as om
from maya import cmds
from utils.test import AssetCallBack


def CreateNode(*args, **kwargs):
    kwargs.update({"skipSelect": True})
    return cmds.createNode(*args, **kwargs)


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


def publishAssetAttr(name: str = None, publishAttrData: dict = None):
    if publishAttrData and isinstance(publishAttrData, dict):
        for k, v in publishAttrData.items():
            cmds.container(name, e=1, publishAndBind=[v, k])


class CreatorBase():
    creatorType: str = "RigAsset"   # example: matrixConstraint, IkFkSystem, spileSystem
    isDagAsset: bool = True
    blackBox: bool = False
    icon: str = None
    publishAttrData: dict = {}

    def __init__(self, name='noName'):
        self._pre_init()

        self.name: str = name
        self.__assetType: str = ("container", "dagContainer")[self.isDagAsset]
        self._post_init()

        self.__create()

    def _pre_init(self):
        pass

    def _post_init(self):
        pass

    def __create(self):
        self._pre_create()
        with AssetCallBack(self.name) as selfCallback:
            self.create()
        self._post_create()

    def _pre_create(self):
        pass

    def _post_create(self):
        pass

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
