from maya import cmds

def createAssets(name, assetsType=None, public=False, blackBox=True, addNode=[], **kwargs):
    """
    Create a container asset in Maya with optional parent and settings.

    Args:
        name (str): Name of the asset container to create.
        assetsType (str): Name of the parent asset container.
        blackBox (bool): Whether the container should be a black box.
        icon (str): Icon name for the container.
        addNode (list): List of nodes to add to the container.

    Returns:
        str: The name of the created or existing asset container.
    """
    # Retrieve optional parameters
    icon = kwargs.get("icon", None)
    type = kwargs.get("type", "container")

    # Check if the asset already exists
    if cmds.objExists(name) and public:
        return name

    # Create parent assets if specified and not existing
    if assetsType is not None:
        if not cmds.objExists(assetsType):
            rig_assets = createAssets(name="RigAssets", assetsType=None, blackBox=False, icon="character.svg", public=True, type="dagContainer")
            assetsType = createAssets(name=assetsType, assetsType=rig_assets, blackBox=False, icon=icon, public=True)

    # Create the asset container
    assets = cmds.container(name=name, type=type)
    for x in addNode:
        cmds.container(name=name, e=1, f=1, an=x)

    # Set container attributes
    cmds.setAttr("{}.blackBox".format(assets), blackBox)
    cmds.setAttr("{}.viewMode".format(assets), 0)
    if icon:
        cmds.setAttr("{}.iconName".format(assets), icon, type="string")

    # Add the container to the parent container if specified
    if assetsType:
        if cmds.objExists(assetsType):
            cmds.container(assetsType, e=1, addNode=assets, f=1, it=1, ish=1)

    return assets


def assetBindAttr(name, bind_attr):
    for k, v in bind_attr.items():
        cmds.container(name, e=1, publishName=k)
        cmds.container(name, e=1, bindAttr=[v, k])


def get_bindAttrs(name):
    bindAttrList = cmds.container(name, q=1, ba=1)
    bindAttr = {}
    if bindAttrList:
        for i in range(0, len(bindAttrList), 2):
            bindAttr.update({bindAttrList[i+1]: bindAttrList[i]})
    return bindAttr
