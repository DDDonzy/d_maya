import maya.cmds as cmds

from mutils.transform import align_transform, reset_transform

import log


def align_transform_cmd():
    """Align selected objects to the first selected object"""
    selected_objects = cmds.ls(sl=True)
    if len(selected_objects) < 2:
        log.error("Please select at least two objects.")
        return
    source = selected_objects[0]
    for target in selected_objects[1:]:
        align_transform(source, target)
    log.success("Align Complete.")


def reset_transform_cmd(transform=True, userDefined=False):
    for obj in cmds.ls(sl=1):
        reset_transform(obj, transform, userDefined)
    log.success("Reset value(all)." if userDefined else "Reset value.")
