import functools
import inspect
import maya.api.OpenMaya as om
from maya import cmds

RIG_ASSET = "RigAsset"


def createContainer(name: str,
                    assetType: str = 'dagContainer',
                    addNode: list = [],
                    blackBox: bool = False,
                    icon: str = None,
                    publishAttrData: dict = None):

    container = cmds.createNode(assetType, name=name, ss=1)
    print(container)
    print(addNode)
    cmds.container(container, e=1, an=addNode)
    cmds.setAttr(f"{container}.blackBox", blackBox) if blackBox else None
    cmds.setAttr(f"{container}.iconName", icon) if icon else None
    cmds.setAttr(f"{container}.viewMode", 0)
    if publishAttrData:
        publishAssetAttr(name=container, publishAttrData=publishAttrData)


def publishAssetAttr(name: str = None, publishAttrData: dict = None):
    if publishAttrData and isinstance(publishAttrData, dict):
        for k, v in publishAttrData.items():
            cmds.container(name, e=1, publishAndBind=[v, k])


class AssetCallBack:
    callBack_instance = []

    def __init__(self,
                 name: str = "",
                 assetType: str = "container",
                 blackBox: bool = False,
                 icon: str = None):
        self.name = name
        self.addNode: list[str] = []

        self.assetType = assetType
        self.blackBox = blackBox
        self.icon = icon
        self.publishAttrData = None

        self.addCallBackID: int = 0
        self.removeCallBackID: int = 0

    def __repr__(self):
        return str(self.name)

    def __enter__(self):
        self.addCallBack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.removeNodeCallBack()
        createContainer(name=self.name,
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


def createAsset(parentAsset: str = "",
                assetType: str = "dagContainer"):  # 外部函数，接收装饰器参数

    def decorator(func):  # 内部函数，接收被装饰的函数

        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # 包装函数
            # 截取参数
            name = getNameFromFunctionParameter(*args, **kwargs)
            if not name:
                name = f"{parentAsset}1"
            else:
                name = f"{name}_{parentAsset}"
            
                
            # 运行函数前设置 call bask 用来截取这段时间内maya创建的节点
            with AssetCallBack(name=name, assetType=assetType) as asset:
                # 函数
                kwargs.update({"name": name})
                asset.publishAttrData = func(*args, **kwargs)  # 运行函数
                        
                        # 判断有无父级资产
            if not cmds.objExists(parentAsset):
                createContainer(name=parentAsset, assetType="dagContainer")
                if not cmds.objExists(RIG_ASSET):
                    createContainer(name=RIG_ASSET, assetType="dagContainer", addNode=parentAsset)
                    cmds.setAttr(f"{RIG_ASSET}.iconName", "character.svg", type="string")
                else:
                    cmds.container(RIG_ASSET, e=1, an=parentAsset)
            cmds.container(parentAsset, e=1, an=asset)
            return asset
        return wrapper
    return decorator


def hasKwargs(func):
    # 获取函数的签名
    signature = inspect.signature(func)

    # 遍历函数的参数，看是否包含 **kwargs
    for param in signature.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
    return False


def getNameFromFunctionParameter(*args, **kwargs):
    name = (kwargs.get("name")) or (kwargs.get("n")) or (args[-1] if args else None)
    if not name:
        sel = cmds.ls(sl=1)
        name = sel[-1] if sel else None
    return name
