from maya import cmds
from z_bs.utils.duplicateMesh import duplicate_mesh
from z_bs.utils.getHistory import *


def createWrap(*args, **kwargs):
    """
    Creates a standard Maya wrap deformer.

    Usage:
        To make 'pSphere1' be deformed by 'pCube1':
        createWrap("pCube1", "pSphere1")
        createWrap("pCube1", "pSphere1", falloffMode=0, maxDistance=2.0)

    Args:
        *args: A list of arguments where:
            args[0] (str): The name of the influence object (the deformer).
            args[1] (str): The name of the surface to be deformed.

        **kwargs: A dictionary of optional keyword arguments:
            weightThreshold (float): Sets the weight threshold for the wrap. Default is 0.0.
            maxDistance (float): Sets the max distance for influence. Default is 1.0.
            exclusiveBind (bool): Sets whether to use exclusive binding. Default is True.
            autoWeightThreshold (bool): Toggles auto weight threshold. Default is True.
            falloffMode (int): Sets the falloff mode (0=Volume, 1=Surface). Default is 1 (Surface).

    Returns:
        tuple[str, str]: A tuple containing:
            - The name of the created wrap deformer node.
            - The name of the created base object.
    """

    influence = args[0]
    surface = args[1]
    weightThreshold = kwargs.get('weightThreshold', 0.0)
    maxDistance = kwargs.get('maxDistance', 1.0)
    exclusiveBind = kwargs.get('exclusiveBind', True)
    autoWeightThreshold = kwargs.get('autoWeightThreshold', True)
    falloffMode = kwargs.get('falloffMode', 1)

    shapes = get_shape(influence)
    if not shapes:
        raise RuntimeError(f"Can not find {influence} shape.")
    influenceShape = shapes[0]

    wrapNode = cmds.deformer(surface, type='wrap')[0]
    cmds.setAttr(wrapNode + '.weightThreshold', weightThreshold)
    cmds.setAttr(wrapNode + '.maxDistance', maxDistance)
    cmds.setAttr(wrapNode + '.exclusiveBind', exclusiveBind)
    cmds.setAttr(wrapNode + '.autoWeightThreshold', autoWeightThreshold)
    print(wrapNode, falloffMode)
    cmds.setAttr(wrapNode + '.falloffMode', falloffMode)
    cmds.connectAttr(surface + '.worldMatrix[0]', wrapNode + '.geomMatrix')

    base = duplicate_mesh(influence, name=influence + 'Base')
    baseShape = get_shape(base)[0]
    cmds.hide(base)

    if not cmds.attributeQuery('dropoff', n=influence, exists=True):
        cmds.addAttr(influence, sn='dr', ln='dropoff', dv=4.0, min=0.0, max=20.0)
        cmds.setAttr(influence + '.dr', k=True)
    if cmds.nodeType(influenceShape) == 'mesh':
        if not cmds.attributeQuery('smoothness', n=influence, exists=True):
            cmds.addAttr(influence, sn='smt', ln='smoothness', dv=0.0, min=0.0)
            cmds.setAttr(influence + '.smt', k=True)
        if not cmds.attributeQuery('inflType', n=influence, exists=True):
            cmds.addAttr(influence, at='short', sn='ift', ln='inflType', dv=2, min=1, max=2)
        cmds.connectAttr(influenceShape + '.worldMesh', wrapNode + '.driverPoints[0]')
        cmds.connectAttr(baseShape + '.worldMesh', wrapNode + '.basePoints[0]')
        cmds.connectAttr(influence + '.inflType', wrapNode + '.inflType[0]')
        cmds.connectAttr(influence + '.smoothness', wrapNode + '.smoothness[0]')

    if cmds.nodeType(influenceShape) == 'nurbsCurve' or cmds.nodeType(influenceShape) == 'nurbsSurface':
        if not cmds.attributeQuery('wrapSamples', n=influence, exists=True):
            cmds.addAttr(influence, at='short', sn='wsm', ln='wrapSamples', dv=10, min=1)
            cmds.setAttr(influence + '.wsm', k=True)
        cmds.connectAttr(influenceShape + '.ws', wrapNode + '.driverPoints[0]')
        cmds.connectAttr(baseShape + '.ws', wrapNode + '.basePoints[0]')
        cmds.connectAttr(influence + '.wsm', wrapNode + '.nurbsSamples[0]')
    cmds.connectAttr(influence + '.dropoff', wrapNode + '.dropoff[0]')
    return wrapNode, base


def createProximityWrap(*args, **kwargs):
    """
    Creates a Proximity Wrap deformer.

    Usage:
        To make 'pSphere1' be deformed by 'pCube1':
        createProximityWrap("pCube1", "pSphere1")
        createProximityWrap("pCube1", "pSphere1", wrapMode=0, falloffScale=150)

    Args:
        *args: A list of arguments where:
            args[0] (str): The name of the influence object (the driver).
            args[1] (str): The name of the surface to be deformed.

        **kwargs: A dictionary of optional keyword arguments:
            wrapMode (int): Sets the wrap mode (0=Offset, 1=Surface). Default is 1.
            falloffScale (float): Scales the overall falloff effect. Default is 20.
            smoothInfluences (int): Default is 0.
            smoothNormals (int): Default is 0.
            dropoffRateScale (float): Default is 0.

    Returns:
        tuple[str, None]: A tuple containing:
            - The name of the created proximityWrap deformer node.
            - None (to maintain a similar return structure to createWrap).
    """
    influence = args[0]
    surface = args[1]

    shapes = get_shape(influence)[0]

    wrapNode = cmds.deformer(surface, type='proximityWrap')[0]

    wrapMode = kwargs.get('wrapMode', 1)
    smoothInfluences = kwargs.get("smoothInfluences", 0)
    smoothNormals = kwargs.get("smoothNormals", 0)
    falloffScale = kwargs.get("falloffScale", 20)
    dropoffRateScale = kwargs.get("dropoffRateScale", 0)

    cmds.setAttr(wrapNode + ".wrapMode", wrapMode)
    cmds.setAttr(wrapNode + ".falloffScale", falloffScale)
    cmds.setAttr(wrapNode + ".smoothInfluences", smoothInfluences)
    cmds.setAttr(wrapNode + ".smoothNormals", smoothNormals)
    cmds.setAttr(wrapNode + ".dropoffRateScale", dropoffRateScale)

    inf_orig = get_orig(influence)
    if not inf_orig:
        cmds.deformableShape(influence, cog=1)
        inf_orig = cmds.deformableShape(influence, cog=1)[0]
    else:
        inf_orig = inf_orig[0]

    print(inf_orig)
    print(shapes)
    cmds.connectAttr(f"{inf_orig}.outMesh", f"{wrapNode}.drivers[0].driverBindGeometry")
    cmds.connectAttr(f"{shapes}.worldMesh[0]", f"{wrapNode}.drivers[0].driverGeometry")

    return wrapNode, None
