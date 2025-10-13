from maya import cmds


def find_animated_controls():
    """
    查找场景中所有有关键帧动画的控制器
    """
    animated_controls = []

    try:
        keyframe_objects = cmds.ls(type="transform")

        for obj in keyframe_objects:
            # 检查对象是否有关键帧
            if cmds.keyframe(obj, query=True, keyframeCount=True) > 0:
                animated_controls.append(obj)

    except Exception:
        raise

    return animated_controls


def find_animated_attrs():
    """
    查找场景中所有有关键帧动画的控制器
    """
    animated_attrs = []

    animCurveNode = cmds.ls(type="animCurveTL") + cmds.ls(type="animCurveTU") + cmds.ls(type="animCurveTA") + cmds.ls(type="animCurveTT")

    for cv in animCurveNode:
        animated_attrs += cmds.listConnections(f"{cv}.output", s=0, d=1, p=1)

    return animated_attrs


def find_animCurveNode():
    animCurveNode = cmds.ls(type="animCurveTL") + cmds.ls(type="animCurveTU") + cmds.ls(type="animCurveTA") + cmds.ls(type="animCurveTT")

    return animCurveNode


def bake_and_merge_animation_layers(objects_to_bake, destination_layer=None, time_range=None):
    """
    Bakes and merges animation layers for specified objects.

    Args:
        objects_to_bake (list): A list of objects (e.g., 'pSphere1', 'nurbsSphere1')
                                whose animation layers will be baked.
        destination_layer (str, optional): The name of the animation layer to bake to.
                                           If None, bakes to the base animation curves.
        time_range (tuple, optional): A tuple (start_frame, end_frame) specifying the
                                      time range for baking. If None, uses the current
                                      time slider range.
    """
    if not objects_to_bake:
        cmds.warning("No objects provided for baking.")
        return

    # Ensure objects are selected for bakeResults to operate on them
    cmds.select(objects_to_bake, replace=True)

    bake_args = {
        'simulation': True,  # Essential for correct baking with layers
        'bakeOnOverrideLayer': False, # Set to True if baking to an override layer
        'removeBakedAnimFromLayer': True, # Removes baked anim from original layers
        'removeBakedAttributeFromLayer': True, # Removes baked attributes from original layers
        'sparseAnimCurveBake': False, # Set to True for fewer keys, if desired
    }

    if destination_layer:
        bake_args['destinationLayer'] = destination_layer
    else:
        # If no destination layer, bake to base animation curves
        bake_args['resolveWithoutLayer'] = 'baseAnimation'

    if time_range:
        bake_args['time'] = time_range
    else:
        # Use current time slider range if no specific range is provided
        min_time = cmds.playbackOptions(query=True, minTime=True)
        max_time = cmds.playbackOptions(query=True, maxTime=True)
        bake_args['time'] = (min_time, max_time)

    try:
        cmds.bakeResults(objects_to_bake, **bake_args)
        cmds.warning(f"Successfully baked and merged animation layers for: {', '.join(objects_to_bake)}")
    except RuntimeError as e:
        cmds.error(f"Error during baking: {e}")

def merge_animLayers():
    """
    合并所有动画层
    """

    animated_attrs = []

    min_framer = 0
    max_framer = 0
    animCurveNode = cmds.ls(type="animCurveTL") + cmds.ls(type="animCurveTU") + cmds.ls(type="animCurveTA") + cmds.ls(type="animCurveTT")

    for cv in animCurveNode:
        t = cmds.keyframe(cv, q=1)
        start = t[0]
        end = t[-1]
        if start < min_framer or min_framer == 0:
            min_framer = start
        if end > max_framer or max_framer == 0:
            max_framer = end
        animated_attrs += cmds.listConnections(f"{cv}.output", s=0, d=1, p=1)

    bake_and_merge_animation_layers(animated_attrs, destination_layer=None, time_range=(min_framer, max_framer))

    cmds.delete(cmds.ls(type="animLayer"))


