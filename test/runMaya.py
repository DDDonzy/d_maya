

from maya import cmds
# import maya.standalone
# maya.standalone.initialize()


RIG_ASSET = "RigAssets"


def _createAsset(name: str, assetType="dagContainer", parentAsset=None, public=False, blackBox=True, icon=None):
    if (parentAsset is not None) and (not cmds.objExists(parentAsset)) and (name != RIG_ASSET):
        _createAsset(name=parentAsset, assetType="dagContainer", parentAsset=RIG_ASSET)

    asset = cmds.container(name=name, type=assetType, c=1)

    if icon:
        cmds.setAttr(f"{asset}.iconName", icon, type="string")
    if blackBox:
        cmds.setAttr(f"{asset}.blackBox", blackBox)

    return asset


_createAsset("xx", "container", "matrixConstraint")
_createAsset("xx1", "container", "matrixConstraint")
