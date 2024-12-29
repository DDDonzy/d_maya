from maya import cmds


def create_controller_tag(transform):
    if type(transform) != list:
        transform = [transform]
    # clear controller in scene
    old_controller_tag = cmds.ls(type="controller")
    if old_controller_tag:
        cmds.delete(old_controller_tag)

    for obj in transform:
        tag = cmds.createNode("controller", name=f'{obj}_tag', ss=1)
        cmds.connectAttr(f"{obj}.message",
                         f"{tag}.controllerObject")

# create_controller_tag(cmds.ls(sl=1))
