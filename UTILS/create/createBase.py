from maya.api import OpenMaya as om
from maya import cmds
from UTILS.create.assetCallback import AssetCallback

RIG_ASSET_NAME = "RigAsset"
IS_BUILD_ASSETS = True

def getNameFromFunctionParameter(*args, **kwargs):
    name = (kwargs.get("name")) or (kwargs.get("n")) or (args[-1] if args else None)
    if not name:
        sel = cmds.ls(sl=1)
        name = sel[-1] if sel else None
    return name


def CreateNode(*args, **kwargs):
    kwargs.update({"skipSelect": True})
    return cmds.createNode(*args, **kwargs)


class CreateBase():
    """Create rig asset base class"""
    isBuildAsset: bool = IS_BUILD_ASSETS
    isDagAsset: bool = True
    isBlackBox: bool = True
    isPublishAssetAttr: bool = True
    isPublishAssetNode: bool = True
    icon: str = None
    thisAssetName: str = None

    def __init__(self, *args, **kwargs):
        """
        Initialize the base creator class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                name (str): The name of the asset. If not provided, it will be derived from the function parameters or selection list.
                query (bool): Alias for q. Default is False.
                edit (bool): Alias for e. Default is False.
        """
        # init parameter
        self.thisType = self.__class__.__name__

        self.name: str = getNameFromFunctionParameter(*args, **kwargs)
        if not self.thisAssetName:
            self.thisAssetName = f"{self.name}_{self.thisType}1"

        self.isQuery = kwargs.get("q") or kwargs.get("query") or False
        self.isEdit = kwargs.get("e") or kwargs.get("edit") or False

        self.__publishAttrData: dict = {}
        self.__publishNodeData: list = []

        if not self.name:
            raise RuntimeError("Please input name or select objects")

        # do
        if self.isQuery:
            self.query()
        elif self.isEdit:
            self.edit()
        else:
            self.__create()

    def __create(self):
        self._pre_create()

        if self.isBuildAsset:
            with AssetCallback(name=self.thisAssetName,
                               force=True,
                               icon=self.icon,
                               isBlackBox=self.isBlackBox,
                               isDagAsset=self.isDagAsset) as self.thisAssetName:
                self.create()
                AssetCallback.publishAssetData(name=self.thisAssetName,
                                               isPublishAssetAttr=self.isPublishAssetAttr,
                                               isPublishNode=self.isPublishAssetNode,
                                               publishAttrData=self.__publishAttrData,
                                               publishNodeList=self.__publishNodeData)
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

    def publishNode(self, nodeList):
        if not isinstance(nodeList, list):
            nodeList = [nodeList]
        self.__publishNodeData.extend(nodeList)

    def createName(self, keyword):
        return "_".join([self.name, keyword, self.thisType]) + "1"

    def __repr__(self):
        if self.thisAssetName:
            return f"{self.__class__.__name__}(name: {self.thisAssetName})"
        else:
            return f"{self.__class__.__name__}(name: {self.name})"

    def __str__(self):
        if self.thisAssetName:
            return self.thisAssetName
        else:
            return self.name
