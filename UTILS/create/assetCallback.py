from maya import cmds


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
                    if (cmds.listRelatives(x, p=1) or ["world"])[0] not in nodeList+[self.currentContainer]:
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
        container = cmds.createNode(assetType, name=name, skipSelect=True)
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
