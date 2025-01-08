from maya import cmds


def createAssets(name: str,
                 **kwargs):
    """
    Create a container asset in Maya with optional parent and settings.

    Args:
        name (str): Name of the asset container to create.

        **kwargs: Optional keyword arguments:
            parent_assets (str): Name of the parent asset container.
            black_box (bool): Whether the container should be a black box.
            icon (str): Icon name for the container.
            add_node (list): List of nodes to add to the container.

    Returns:
        str: The name of the created or existing asset container.
    """
    # Retrieve optional parameters
    parent_assets = kwargs.get("parent_assets", None)
    black_box = kwargs.get("black_box", True)
    icon = kwargs.get("icon", None)
    add_node = kwargs.get("add_node", [])
    public = bool(kwargs.get("public", False))

    # Check if the asset already exists
    if cmds.objExists(name) and public:
        print("xx")
        return name

    # Create parent assets if specified and not existing
    if parent_assets is not None:
        if not cmds.objExists(parent_assets):
            rig_assets = createAssets(name="RigAssets", parent_assets=None, black_box=False, icon="character.svg", public=True)
            parent_assets = createAssets(name=parent_assets, parent_assets=rig_assets, black_box=False, icon=icon, public=True)

    # Create the asset container
    assets = cmds.container(name=name, an=add_node)

    # Set container attributes
    cmds.setAttr(f"{assets}.blackBox", black_box)
    if icon:
        cmds.setAttr(f"{assets}.iconName", icon, type="string")

    # Add the container to the parent container if specified
    if parent_assets:
        if cmds.objExists(parent_assets):
            cmds.container(parent_assets, e=1, addNode=assets)

    return assets


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
