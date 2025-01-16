from maya.api import OpenMaya as om
from maya import cmds
from utils.test import AssetCallBack
RIG_ASSET_NAME = "RigAsset"

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
    return container


def publishAssetAttr(name: str = None, publishAttrData: dict = None):
    if publishAttrData and isinstance(publishAttrData, dict):
        for k, v in publishAttrData.items():
            cmds.container(name, e=1, publishAndBind=[v, k])


class CreatorBase():
    creatorType: str = "base"   # example: matrixConstraint, IkFkSystem, spileSystem,parentSpace,as name prefix
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
        # run create funcation logic  example create assets
        
        # start new callback and do create function
        self._pre_create()
        with AssetCallBack(self.name) as thisCallback:
            self.create()

        # create this asset
        thisAsset = createContainer(name=f"{self.name}_{self.creatorType}1",
                                    addNode=thisCallback.addNode,
                                    assetType=self.__assetType,
                                    blackBox=self.blackBox,
                                    icon=self.icon)

        # stop callback
        AssetCallBack.currentInstance.stop()
        
        # if not creatorType'asset, create and parent it to RigAsset. else return this creatorType assets'name.
        if not cmds.objExists(self.creatorType):
            thisTypeAsset = createContainer(name=self.creatorType, addNode=[thisAsset])
        else:
            thisTypeAsset = self.creatorType
            cmds.container(thisTypeAsset, e=1 ,an=[thisAsset])

        # if not RigAsset creat it. else return this RigAsset's name.
        if not cmds.objExists(RIG_ASSET_NAME):
            rigAsset = createContainer(name=RIG_ASSET_NAME, addNode=[thisTypeAsset], icon = "character.svg")
        else:
            rigAsset = RIG_ASSET_NAME
            cmds.container(rigAsset, e=1, an=[thisTypeAsset])

        # restore callback
        AssetCallBack.currentInstance.start()

        

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
