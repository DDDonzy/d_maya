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
                if cmds.objectType(x, isAType="transform"):
                    if (cmds.listRelatives(x, p=1) or ["world"])[0] not in nodeList+[self.currentContainer]:
                        cmds.parent(x, self.currentContainer)

        AssetCallback.asset_stack.pop()

    def __init__(self,
                 name,
                 parent=None,
                 isDagAsset=True,
                 isBlackBox=False,
                 icon=None,
                 force=True):
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
    def createContainer(name,
                        isDagAsset=True,
                        isBlackBox=False,
                        icon=None,
                        force=True):
        if not force and cmds.objExists(name):
            return name
        assetType = ("container", "dagContainer")[isDagAsset]
        container = CreateNode(assetType, name=name)
        cmds.container(container, e=1, addNode=[])
        if isBlackBox:
            cmds.setAttr("{}.blackBox".format(container), isBlackBox)
        if icon:
            cmds.setAttr("{}.iconName".format(container), icon, type="string")
        cmds.setAttr("{}.viewMode".format(container), 0)
        return container

    @staticmethod
    def publishAssetData(name,
                         isPublishAssetAttr=False,
                         publishAttrData=None,
                         isPublishNode=False,
                         publishNodeList=[]):

        if publishAttrData and isPublishAssetAttr:
            if publishAttrData and isinstance(publishAttrData, dict):
                for k, v in publishAttrData.items():
                    cmds.container(name, e=1, publishAndBind=[v, k])
        if publishNodeList and isPublishNode:
            if publishNodeList and isinstance(publishNodeList, list):
                for x in publishNodeList:
                    cmds.containerPublish(name, publishNode=[x, ""])
                    cmds.containerPublish(name, bindNode=[x, x])


class CreateBase(object):
    isBuildAsset = IS_BUILD_ASSETS
    isDagAsset = True
    isBlackBox = True
    isPublishAssetAttr = True
    isPublishAssetNode = True
    icon = None
    thisAssetName = None

    def __init__(self, *args, **kwargs):
        self.thisType = self.__class__.__name__

        self.name = getNameFromFunctionParameter(*args, **kwargs)
        if not self.thisAssetName:
            self.thisAssetName = "{}_{}1".format(self.name, self.thisType)

        self.isQuery = kwargs.get("q") or kwargs.get("query") or False
        self.isEdit = kwargs.get("e") or kwargs.get("edit") or False

        self.__publishAttrData = {}
        self.__publishNodeData = []

        if not self.name:
            raise RuntimeError("Please input name or select objects")

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
            return "{}(name: {})".format(self.__class__.__name__, self.thisAssetName)
        else:
            return "{}(name: {})".format(self.__class__.__name__, self.name)

    def __str__(self):
        if self.thisAssetName:
            return self.thisAssetName
        else:
            return self.name
