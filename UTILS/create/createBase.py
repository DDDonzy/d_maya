from maya.api import OpenMaya as om
from maya import cmds
# from UTILS.create.assetCallback import AssetCallback
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


class AssetCallback:
    asset_stack = []

    def __enter__(self):
        self.lastContainer = AssetCallback.asset_stack[-1] if AssetCallback.asset_stack else None
        self.currentContainer = AssetCallback.createContainer(name=self.name,
                                                              isDagAsset=self.isDagAsset,
                                                              isBlackBox=self.blackBox,
                                                              icon=self.icon,
                                                              force=self.force)
        self.name = self.currentContainer
        cmds.container(self.currentContainer, e=1, c=True)
        AssetCallback.asset_stack.append(self)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.lastContainer:
            cmds.container(self.lastContainer, e=1, c=True)
        else:
            cmds.container(self.currentContainer, e=1, c=False)
            if self.parent:
                cmds.container(self.parent, e=1, an=[self])

        if self.isDagAsset:
            nodeList = cmds.container(self.currentContainer, q=1, nodeList=1) or []
            for x in nodeList:
                if cmds.objectType(x, isAType="dagNode"):
                    if (cmds.listRelatives(x, p=1) or ["world"])[0] not in nodeList:
                        cmds.parent(x, self.currentContainer)

        AssetCallback.asset_stack.pop()

    def __init__(self,
                 name: str,
                 parent: str = None,
                 isDagAsset: bool = True,
                 isBlackBox: bool = False,
                 icon: str = None,
                 force: bool = True):
        self.parent = parent
        self.currentContainer = None
        self.lastContainer = None
        self.name = name
        self.force = force
        self.icon = icon
        self.blackBox = isBlackBox
        self.isDagAsset = isDagAsset

    def __repr__(self):
        return str(self.currentContainer)

    def __str__(self):
        return str(self.currentContainer)

    @staticmethod
    def createContainer(name: str,
                        isDagAsset: bool = True,
                        isBlackBox: bool = False,
                        icon: str = None,
                        force: bool = True):
        if not force and cmds.objExists(name):
            return name
        assetType = ("container", "dagContainer")[isDagAsset]
        container = CreateNode(assetType, name=name)
        cmds.container(container, e=1, addNode=[])
        cmds.setAttr(f"{container}.blackBox", isBlackBox) if isBlackBox else None
        cmds.setAttr(f"{container}.iconName", icon, type="string") if icon else None
        cmds.setAttr(f"{container}.viewMode", 0)
        return container

    @staticmethod
    def publishAssetData(name: str,
                         isPublishAssetAttr: bool = False,
                         publishAttrData: dict = None,
                         isPublishNode: bool = False,
                         publishNodeList: list = []):

        if publishAttrData and isPublishAssetAttr:
            if publishAttrData and isinstance(publishAttrData, dict):
                for k, v in publishAttrData.items():
                    cmds.container(name, e=1, publishAndBind=[v, k])
        if publishNodeList and isPublishNode:
            if publishNodeList and isinstance(publishNodeList, list):
                for x in publishNodeList:
                    cmds.containerPublish(name, publishNode=[x, ""])
                    cmds.containerPublish(name, bindNode=[x, x])


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
            with AssetCallback(name=RIG_ASSET_NAME, force=False, icon="character.svg"):
                pass
            with AssetCallback(name=self.thisAssetName,
                               force=True,
                               icon=self.icon,
                               parent=RIG_ASSET_NAME,
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
