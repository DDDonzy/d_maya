import functools
import inspect
import maya.api.OpenMaya as om
from maya import cmds

RIG_ASSET = "RigAsset"


class AssetCallBack:
    callBack_instance = []

    def __init__(self,
                 name: str = "",
                 assetType: str = "container",
                 blackBox: bool = False,
                 icon: str = None):
        print("init")
        self.addNode: list[str] = []
        self.addCallBackID: int = 0
        self.removeCallBackID: int = 0
        self.name = name
        self.assetType = assetType
        self.blackBox = blackBox
        self.icon = icon
        self.publishAttr = {}

    def __enter__(self):
        print("enter")
        self.addCallBack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        self.removeNodeCallBack()
        self.createAsset()

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

    def createAsset(self):
        asset = cmds.container(name=self.name,
                               type=self.assetType,
                               an=self.addNode,
                               f=1)
        cmds.setAttr(f"{asset}.blackBox", self.blackBox) if self.blackBox else None
        cmds.setAttr(f"{asset}.iconName", self.icon) if self.icon else None
        self.asset = asset

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


def create_asset(parentAsset: str = "",
                 assetType: str = "dagContainer"):  # 外部函数，接收装饰器参数
    def decorator(func):  # 内部函数，接收被装饰的函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # 包装函数
            # 截取参数
            name = f"{getName(*args, **kwargs)}_{parentAsset}"
            # 运行函数前设置 call bask 用来截取这段时间内maya创建的节点
            with AssetCallBack(name=name, assetType=assetType) as asset_class:
                # 如果函数定义了 **kwargs 参数,把assetData 传递进函数，以便于publish属性
                if has_kwargs(func):
                    kwargs.update({"assetData": asset_class})
                # 函数
                func(*args, **kwargs)  # 运行函数
                # 如果函数内部设置了 publishAttr,执行publish 方法
                if asset_class.publishAttr:
                    print("publishAttr", asset_class.publishAttr)
            # publish 属性
            # 判断有无父级资产
            if not cmds.objExists(parentAsset):
                cmds.container(name=parentAsset, type="dagContainer")
                if not cmds.objExists(RIG_ASSET):
                    cmds.container(name=RIG_ASSET, type="dagContainer", an=parentAsset)
                    cmds.setAttr(f"{RIG_ASSET}.iconName", "character.svg", type="string")
            cmds.container(parentAsset, e=1, an=asset_class.asset)
            return asset_class.asset
        return wrapper
    return decorator


def has_kwargs(func):
    # 获取函数的签名
    signature = inspect.signature(func)

    # 遍历函数的参数，看是否包含 **kwargs
    for param in signature.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
    return False


def getName(*args, **kwargs):
    name = (kwargs.get("name")) or (kwargs.get("n")) or (args[-1] if args else None)
    if not name:
        sel = cmds.ls(sl=1)
        name = sel[-1] if sel else "NoName"
    return name

def updatePublishAttrData(**kwargs):
    assetData = kwargs.get("assetData",None)
    if assetData:
        assetData.publishAttr = 

# @create_asset("matrixConstraint", assetType="container")
# def c(**kwargs):
#     cmds.polyCube()

#     assetData = kwargs.get("assetData",None)
#     if assetData:
#         assetData.publishAttr = {"a":"b"}
#     print(assetData,assetData.publishAttr)


# c()



import inspect

def has_kwargs(func):
    # 获取函数的签名
    signature = inspect.signature(func)

    # 遍历函数的参数，看是否包含 **kwargs
    for param in signature.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
    return False

def caller_function():
    # 获取当前帧和上一层帧的信息
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back  # 获取上一层栈帧
    caller_locals = caller_frame.f_locals
    
    
    
def calling_function(*args):
    caller_function()

calling_function()