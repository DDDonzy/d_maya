import functools
import maya.api.OpenMaya as om
from maya import cmds
from maya import OpenMaya as om1


class D_CallBack:
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

    def __enter__(self):
        print("enter")
        self.addCallBack()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")
        self.removeNodeCallBack()
        self.createAsset()

    def addCallBack(self):
        self.base_callBack_instance: list[D_CallBack] = D_CallBack.callBack_instance.copy()
        for baseCallback in D_CallBack.callBack_instance:
            om.MMessage.removeCallback(baseCallback.addCallBackID)
            om.MMessage.removeCallback(baseCallback.removeCallBackID)

        self.addCallBackID = om.MDGMessage.addNodeAddedCallback(D_CallBack.addNodeFunction, "dependNode", self)
        self.removeCallBackID = om.MDGMessage.addNodeRemovedCallback(D_CallBack.removeNodeFunction, "dependNode", self)
        D_CallBack.callBack_instance.append(self)

    def removeNodeCallBack(self):
        om.MMessage.removeCallback(self.addCallBackID)
        om.MMessage.removeCallback(self.removeCallBackID)
        D_CallBack.callBack_instance.remove(self)

        for baseCallback in self.base_callBack_instance:
            baseCallback.addCallBackID = om.MDGMessage.addNodeAddedCallback(D_CallBack.addNodeFunction, "dependNode", baseCallback)
            baseCallback.removeCallBackID = om.MDGMessage.addNodeRemovedCallback(D_CallBack.removeNodeFunction, "dependNode", baseCallback)

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


RIG_ASSET = "RigAsset"


def create_asset(parentAsset: str = "",
                 assetType: str = "dagContainer"):  # 外部函数，接收装饰器参数
    def decorator(func):  # 内部函数，接收被装饰的函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # 包装函数
            # 截取参数
            name = kwargs.get("name") or kwargs.get("n") or args[-1] if args else "NoName"
            name = f"{name}_{parentAsset}"
            # 运行函数前设置 call bask 用来截取这段时间内maya创建的节点
            with D_CallBack(name=name, assetType=assetType) as asset_class:
                # 运行函数
                func(*args, **kwargs)
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


@create_asset("matrixConstraint",assetType="container")
def c():
    cmds.polyCube()
c()
