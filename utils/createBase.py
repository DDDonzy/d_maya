from maya.api import OpenMaya as om
from maya import cmds
from utils.assetCallback import AssetCallback
RIG_ASSET_NAME = "RigAsset"


def getNameFromFunctionParameter(*args, **kwargs):
    name = (kwargs.get("name")) or (kwargs.get("n")) or (args[-1] if args else None)
    if not name:
        sel = cmds.ls(sl=1)
        name = sel[-1] if sel else None
    return name


def CreateNode(*args, **kwargs):
    kwargs.update({"skipSelect": True})
    return cmds.createNode(*args, **kwargs)


def createContainer(name: str,
                    assetType: str = 'dagContainer',
                    addNode: list = [],
                    blackBox: bool = False,
                    icon: str = None,
                    publishAssetAttr: bool = False,
                    publishAttrData: dict = None):

    container = cmds.createNode(assetType, name=name, ss=1)
    cmds.container(container, e=1, an=addNode, f=1)
    cmds.setAttr(f"{container}.blackBox", blackBox) if blackBox else None
    cmds.setAttr(f"{container}.iconName", icon, type="string") if icon else None
    cmds.setAttr(f"{container}.viewMode", 0)
    if publishAttrData and publishAssetAttr:
        if publishAttrData and isinstance(publishAttrData, dict):
            for k, v in publishAttrData.items():
                cmds.container(name, e=1, publishAndBind=[v, k])
    return container


class CreatorBase():
    isBuildAsset: bool = False
    isDagAsset: bool = True
    isBlackBox: bool = True
    isPublishAssetAttr: bool = True
    icon: str = None

    def __init__(self, *args, **kwargs):

        self._pre_init(*args, **kwargs)

        self.name: str = getNameFromFunctionParameter(*args, **kwargs)
        self.thisType = self.__class__.__name__
        self.__publishAttrData: dict = {}

        if not self.name:
            raise RuntimeError("Please input name or select objects")

        self.isQuery = kwargs.get("q") or kwargs.get("query") or False
        self.isEdit = kwargs.get("e") or kwargs.get("edit") or False

        self._post_init(*args, **kwargs)

        if self.isQuery:
            self.query()

        elif self.isEdit:
            self.edit()

        else:
            self.__create()

    def _pre_init(self, *args, **kwargs):
        pass

    def _post_init(self, *args, **kwargs):
        pass

    def __create(self):
        # run create function logic, example create assets
        self._pre_create()

        if self.isBuildAsset:
            # start new callback and do create function
            with AssetCallback(self.name) as thisCallback:
                self.create()
            # create this asset
            self.thisAsset = createContainer(name=f"{self.name}_{self.thisType}1",
                                             addNode=thisCallback.addNode,
                                             assetType=("container", "dagContainer")[self.isDagAsset],
                                             blackBox=self.isBlackBox,
                                             icon=self.icon,
                                             publishAssetAttr=self.isPublishAssetAttr,
                                             publishAttrData=self.__publishAttrData)
            # use with AssetCallback to excluding rigAsset and typeAssets
            with AssetCallback("STOP"):
                # if not creatorType'asset, create and parent it to RigAsset. else return this creatorType assets'name.
                if not cmds.objExists(self.thisType):
                    thisTypeAsset = createContainer(name=self.thisType, addNode=[self.thisAsset])
                else:
                    thisTypeAsset = self.thisType
                    cmds.container(thisTypeAsset, e=1, an=[self.thisAsset])
                # if not RigAsset create it. else return this RigAsset's name.
                if not cmds.objExists(RIG_ASSET_NAME):
                    rigAsset = createContainer(name=RIG_ASSET_NAME, addNode=[thisTypeAsset], icon="character.svg")
                else:
                    rigAsset = RIG_ASSET_NAME
                    cmds.container(rigAsset, e=1, an=[thisTypeAsset])

        else:
            self.create()

        self._post_create()

    def _pre_create(self):
        pass

    def _post_create(self):
        pass

    def create(self):
        raise NotImplementedError("Subclass must implement this method")

    def query(self):
        pass

    def edit(self):
        pass

    def publishAttr(self, data):
        self.__publishAttrData.update(data)
        self.__dict__.update(self.__publishAttrData)

    def createName(self, keyword):
        return "_".join([self.name, keyword, self.thisType]) + "1"

    def __repr__(self):
        if self.thisAsset:
            return f"{self.__class__.__name__}(name: {self.thisAsset})"
        else:
            return f"{self.__class__.__name__}(name: {self.name})"

    def __str__(self):
        if self.thisAsset:
            return self.thisAsset
        else:
            return self.name
