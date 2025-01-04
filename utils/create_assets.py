from maya import cmds


def create_assets(name: str,
                  parent_assets: str = None):
    if cmds.objExists(name):
        return name
    assets = cmds.container(name=name)
    cmds.setAttr(f"{assets}.blackBox", 1)
    if parent_assets:
        if cmds.objExists(parent_assets):
            cmds.container(parent_assets, e=1, addNode=assets)
    return assets
