
import functools
from maya import cmds


def createAsset(name: str,
                assetType=None,
                public: bool = False,
                blackBox: bool = True,
                addNode: list = [],
                ** kwargs):
    """
    Create a container asset in Maya with optional parent and settings.

    Args:
        name (str): Name of the asset container to create.

        assetType (str): Name of the parent asset container.
        blackBox (bool): Whether the container should be a black box.
        icon (str): Icon name for the container.
        addNode (list): List of nodes to add to the container.

    Returns:
        str: The name of the created or existing asset container.
    """
    # Retrieve optional parameters
    icon = kwargs.get("icon", None)
    type = kwargs.get("type", "dagContainer")

    # Check if the asset already exists
    if cmds.objExists(name) and public:
        return name

    # Create parent asset if specified and not existing
    if assetType is not None:
        if not cmds.objExists(assetType):
            rig_asset = createAsset(name="RigAssets", assetType=None, blackBox=False, icon="character.svg", public=True, c=1)
            assetType = createAsset(name=assetType, assetType=rig_asset, blackBox=False, icon=icon, public=True, c=1)

    # Create the asset container
    asset = cmds.container(name=name, type=type)
    cmds.container(name=name, e=1, f=1, an=addNode)

    # Set container attributes
    cmds.setAttr(f"{asset}.blackBox", blackBox)
    cmds.setAttr(f"{asset}.viewMode", 0)
    if icon:
        cmds.setAttr(f"{asset}.iconName", icon, type="string")

    # Add the container to the parent container if specified
    if assetType:
        if cmds.objExists(assetType):
            cmds.container(assetType, e=1, addNode=asset, f=1, it=1, ish=1)

    return asset


def assetBindAttr(name: str, bind_attr: dict):
    for k, v in bind_attr.items():
        cmds.container(name, e=1, publishName=k)
        cmds.container(name, e=1, bindAttr=[v, k])


def get_bindAttrs(name: str):
    bindAttrList = cmds.container(name, q=1, ba=1)
    bindAttr = {}
    if bindAttrList:
        for i in range(0, len(bindAttrList), 2):
            bindAttr.update({bindAttrList[i+1]: bindAttrList[i]})
    return bindAttr


def create_asset(parentAsset=None, assetType="dagContainer", blackBox=True, icon=None):
    # 定义外部装饰器
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = "ds"
            asset = _createAsset(name=name, parentAsset=parentAsset, assetType=assetType, blackBox=blackBox, icon=icon)
            bindData = func(*args, **kwargs)
            if bindData:
                assetBindAttr(asset, bindData)
            return asset
        return wrapper
    return decorator


RIG_ASSET = "RigAsset"


def _createAsset(parentAsset=RIG_ASSET, assetType="dagContainer", blackBox=True, icon=None, name=None):
    if name == None:
        name = "temp_asset"

    # no rigAsset
    if not cmds.objExists(RIG_ASSET):
        rigAsset = cmds.container(name=RIG_ASSET, type="dagContainer", c=1)
        cmds.setAttr(f"{rigAsset}.iconName", "character.svg", type="string")
        cmds.setAttr(f"{rigAsset}.blackBox", False)

    # no parentAsset
    if not cmds.objExists(parentAsset):
        parentAsset = cmds.container(name=parentAsset, type=assetType, c=1)
        cmds.setAttr(f"{parentAsset}.blackBox", False)
    # create asset
    cmds.container(parentAsset, e=1, c=1)
    asset = cmds.container(name=name, type=assetType, c=1)

    if icon:
        cmds.setAttr(f"{asset}.iconName", icon, type="string")

    if blackBox:
        cmds.setAttr(f"{asset}.blackBox", blackBox)

    return asset


@create_asset(name="matrix", parentAsset="matrixConstraint")
def create(name="xxx"):
    cmds.createNode("multMatrix", name=name)


create("yes")
