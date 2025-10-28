from maya import cmds
import maya.api.OpenMaya as om

"""
Maya Asset Container Management with Context Manager
==================================================

This module provides a context manager for creating and managing Maya asset containers.
It supports both regular containers and DAG containers with automatic node organization.

Features:
- Context manager for automatic container creation and cleanup
- Support for nested containers with stack management
- Automatic parenting of DAG nodes to container
- Configurable container properties (blackBox, icon, etc.)
- Asset data publishing capabilities


Usage:
    with AssetCallback(name="myAsset", isDagAsset=True) as asset:
        cmds.polyCube(name="cube1")
        cmds.polySphere(name="sphere1")
    # All created nodes are automatically added to the container
"""


class AssetCallback:
    """
    Context manager for Maya asset container creation and management.

    This class provides automatic container creation, node management, and cleanup
    through Python's context manager protocol (__enter__ and __exit__).

    """

    asset_stack = []

    def __init__(self, name: str = "asset", parent: str = None, isDagAsset: bool = True, isBlackBox: bool = False, icon: str = None, force: bool = True):
        """
        Initialize the AssetCallback context manager.

        Args:
            name (str): Name for the container asset
            parent (str): Parent container to nest this asset under
            isDagAsset (bool): Create DAG container if True, regular container if False
            isBlackBox (bool): Set container as black box (hide internal connections)
            icon (str): Icon name for the container display
            force (bool): Force creation even if container with same name exists
        """
        self.parent = parent
        self.currentContainer = None
        self.lastContainer = None
        self.name = name
        self.force = force
        self.icon = icon
        self.blackBox = isBlackBox
        self.isDagAsset = isDagAsset

    def __enter__(self):
        """
        Enter the context manager - create container and set as current.

        Returns:
            AssetCallback: Self instance for use in 'with' statement
        """
        # Store reference to previous container in stack
        self.lastContainer = AssetCallback.asset_stack[-1] if AssetCallback.asset_stack else None

        # Create new container with specified parameters
        self.currentContainer = AssetCallback.createContainer(name=self.name, isDagAsset=self.isDagAsset, isBlackBox=self.blackBox, icon=self.icon, force=self.force)
        self.name = self.currentContainer

        # Set container as current (nodes created will be added to it)
        cmds.container(self.currentContainer, e=1, c=True)

        # Add to stack for nested container support
        AssetCallback.asset_stack.append(self)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Restore previous container as current or disable current container
        if self.lastContainer:
            cmds.container(self.lastContainer, e=1, c=True)
        else:
            cmds.container(self.currentContainer, e=1, c=False)
            # Add to parent container if specified
            if self.parent:
                cmds.container(self.parent, e=1, an=[self])

        # For DAG containers, organize hierarchy by parenting orphaned nodes
        if self.isDagAsset:
            nodeList = cmds.container(self.currentContainer, q=1, nodeList=1) or []
            for x in nodeList:
                if cmds.objectType(x, isAType="transform"):
                    # Check if node's parent is outside the container
                    if (cmds.listRelatives(x, p=1) or ["world"])[0] not in nodeList + [self.currentContainer]:
                        # Parent the node to the container
                        cmds.parent(x, self.currentContainer)

        # Remove from stack
        AssetCallback.asset_stack.pop()

    def __repr__(self):
        """String representation of the container."""
        return str(self.currentContainer)

    def __str__(self):
        """String conversion of the container."""
        return str(self.currentContainer)

    @staticmethod
    def createContainer(name: str, isDagAsset: bool = True, isBlackBox: bool = False, icon: str = None, force: bool = True):
        """
        Create a Maya container with specified properties.

        Args:
            name (str): Container name
            isDagAsset (bool): Create DAG container if True
            isBlackBox (bool): Set as black box container
            icon (str): Icon name for display
            force (bool): Force creation if name exists

        Returns:
            str: Name of created container
        """
        # Return existing container if force is False and it exists
        if not force and cmds.objExists(name):
            return name

        assetType = ("container", "dagContainer")[isDagAsset]
        container = cmds.createNode(assetType, name=name, skipSelect=True)

        cmds.container(container, e=1, addNode=[])
        cmds.setAttr(f"{container}.blackBox", isBlackBox) if isBlackBox else None
        cmds.setAttr(f"{container}.iconName", icon, type="string") if icon else None
        cmds.setAttr(f"{container}.viewMode", 0)

        return container

    @staticmethod
    def publishAssetData(name: str, isPublishAssetAttr: bool = False, publishAttrData: dict = None, isPublishNode: bool = False, publishNodeList: list = []):
        """
        Publish asset data for external access.

        Args:
            name (str): Container name to publish data for
            isPublishAssetAttr (bool): Enable attribute publishing
            publishAttrData (dict): Dictionary of attributes to publish
            isPublishNode (bool): Enable node publishing
            publishNodeList (list): List of nodes to publish
        """
        # Publish attributes if requested
        if publishAttrData and isPublishAssetAttr:
            if publishAttrData and isinstance(publishAttrData, dict):
                for k, v in publishAttrData.items():
                    cmds.container(name, e=1, publishAndBind=[v, k])

        # Publish nodes if requested
        if publishNodeList and isPublishNode:
            if publishNodeList and isinstance(publishNodeList, list):
                for x in publishNodeList:
                    cmds.containerPublish(name, publishNode=[x, ""])
                    cmds.containerPublish(name, bindNode=[x, x])


#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################


MUTE_MESSAGE = False


def showMessage(msg):
    if MUTE_MESSAGE:
        return
    message = f"<hl> {msg} </hl>"
    cmds.inViewMessage(amg=message, pos="botRight", fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)


def muteMessage(mute: bool):
    global MUTE_MESSAGE
    MUTE_MESSAGE = mute
    return MUTE_MESSAGE


#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
RAD_TO_DEG = 57.29577951308232  # 180.0 / pi
DEG_TO_RAD = 0.017453292519943295  # pi / 180.0


class MIRROR_MATRIX:
    x = om.MMatrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    y = om.MMatrix([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    z = om.MMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    def __init__(self, axis: str = "x"):
        axis = axis.lower()
        if axis not in "xyz":
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis: str = "x"):
        return getattr(MIRROR_MATRIX, axis)


def UNIT_CONVERT(unit: str = None) -> float:
    """
    Convert the current unit to the specified unit and return the conversion factor.

    Args:
        unit (str, optional): The unit to convert to. Defaults to None.

    Returns:
        float: The conversion factor for the specified unit.
    """
    if unit is None:
        unit = cmds.currentUnit(q=1)
    conversion_factors = {"mm": 10.0, "cm": 1.0, "m": 0.01}
    if unit not in conversion_factors:
        raise ValueError("Invalid unit. Choose from 'mm', 'cm', or 'm'.")
    return conversion_factors[unit]


def mirror_transform(
    source_obj: str,
    target_obj: str,
    mirror_axis: str = "x",
):
    """flip source object's world space matrix  as target object's world space matrix

    Args:
        sour_obj (str): source transform object
        target_obj (str): target transform object
        mirror_axis (str, optional): mirror axis. Defaults to "x".
    """
    sour_worldMatrix = get_worldMatrix(source_obj)
    sour_parent_matrix = get_parentMatrix(source_obj)
    sour_worldMatrix_flip = flip_matrix(sour_worldMatrix, mirror_axis)
    sour_parent_matrix_flip = flip_matrix(sour_parent_matrix, mirror_axis)
    target_parent_matrix = get_parentMatrix(target_obj)
    flip_offsetMatrix = get_offsetMatrix(sour_parent_matrix_flip, target_parent_matrix)
    set_worldMatrix(target_obj, flip_offsetMatrix * sour_worldMatrix_flip)


def flip_transform(
    source_obj: str,
    target_obj: str,
    mirror_axis: str = "x",
):
    sour_worldMatrix = get_worldMatrix(source_obj)
    sour_worldMatrix_flip = flip_matrix(sour_worldMatrix, mirror_axis)
    set_worldMatrix(target_obj, sour_worldMatrix_flip)
    for x in "xyz":
        cmds.setAttr(f"{target_obj}.s{x}", abs(cmds.getAttr(f"{target_obj}.s{x}")))


def flip_matrix(worldMatrix: om.MMatrix, mirror_axis: str = "x") -> om.MMatrix:
    """flip matrix by mirror matrix

    Args:
        worldMatrix (om.MMatrix): input world matrix
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix
    """
    mirror_matrix = worldMatrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offsetMatrix(child_worldMatrix: om.MMatrix, parent_worldMatrix: om.MMatrix) -> om.MMatrix:
    """
    get offset matrix
    get local matrix when child in parent space

    Args:
        child_worldMatrix (om.MMatrix): child world matrix
        parent_worldMatrix (om.MMatrix): parent world matrix

    Returns:
        om.MMatrix: local matrix when child in parent space
    """
    # child_worldMatrix = child_localMatrix * parent_worldMatrix
    # child_worldMatrix * parent_worldMatrix.inverse = child_localMatrix
    child_localMatrix = child_worldMatrix * parent_worldMatrix.inverse()
    return child_localMatrix


def get_relativesMatrix(matrix: om.MMatrix, referenceMatrix: om.MMatrix) -> om.MMatrix:
    """
    Calculate the relative matrix

    This function calculates the relative matrix of a given matrix with respect to a reference matrix.

    Args:
        matrix (om.MMatrix): The input matrix
        referenceMatrix (om.MMatrix): The reference matrix

    Returns:
        om.MMatrix: The relative matrix
    """
    relativesMatrix = matrix * referenceMatrix.inverse()
    return relativesMatrix


def get_localMatrix(obj: str) -> om.MMatrix:
    """get object's local space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: local matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return om.MFnTransform(mSel.getDagPath(0)).transformation().asMatrix()


def get_worldMatrix(obj: str) -> om.MMatrix:
    """get object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: world matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).inclusiveMatrix()


def get_parentMatrix(obj: str) -> om.MMatrix:
    """get object's parent object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: parent object's world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).exclusiveMatrix()


def set_localMatrix(obj: str, matrix: om.MMatrix) -> None:
    """set maya object's local as input matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input local matrix
    """
    if cmds.objExists(f"{obj}.jointOrient"):
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_worldMatrix(obj: str, matrix: om.MMatrix) -> None:
    """convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    localMatrix = matrix * mSel.getDagPath(0).exclusiveMatrixInverse()
    set_localMatrix(obj, localMatrix)


def matrix_to_trs(matrix: om.MMatrix, rotateOrder: int = 0) -> list:
    """convert matrix to maya's translate,rotate and scale

    Args:
        matrix (om.MMatrix): input matrix
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        list: [tx,ty,tz,rx,ry,rz,sx,sy,sz]
    """
    mTransformation = om.MTransformationMatrix(matrix)
    translate = mTransformation.translation(1) * UNIT_CONVERT()
    euler_radians = mTransformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [RAD_TO_DEG * radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = mTransformation.scale(1)
    outputList = [
        translate[0],
        translate[1],
        translate[2],
        euler_angle[0],
        euler_angle[1],
        euler_angle[2],
        scale[0],
        scale[1],
        scale[2],
    ]
    return outputList


def trs_to_matrix(trs: list, rotateOrder: int = 0) -> om.MMatrix:
    """convert [tx,ty.tz,rx,ry,rz,sx,sy,sz] to matrix

    Args:
        trs (list): input [tx,ty.tz,rx,ry,rz,sx,sy,sz]
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        om.MMatrix: matrix
    """
    mTransformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation([DEG_TO_RAD * angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    mTransformation.setTranslation(translate, 1)
    mTransformation.setRotation(euler_radians)
    mTransformation.setScale(scale, 1)
    return mTransformation.asMatrix()


def get_trs(obj: str) -> list:
    """get maya transform's transformation [tx,ty.tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): _description_

    Returns:
        list: [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr(f"{obj}.{attr}"))
    return trs


def set_trs(obj: str, trs: list) -> None:
    """set maya transform [tx,ty.tz,rx,ry,rz,sx,sy,sz].
    Args:.
        obj (str): maya transform object'name.
        trs (list): [tx,ty.tz,rx,ry,rz,sx,sy,sz].
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr(f"{obj}.{attr}", trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def alignTransform(source: str, target: str):
    """Align target object to source object

    Args:
        source (str): align source object
        target (str): align target object
    """
    set_worldMatrix(target, get_worldMatrix(source))


def alignTransform_cmd():
    """Align selected objects to the first selected object"""
    selected_objects = cmds.ls(sl=True)
    if len(selected_objects) < 2:
        om.MGlobal.displayError("Please select at least two objects.")
        return
    source = selected_objects[0]
    for target in selected_objects[1:]:
        alignTransform(source, target)
    showMessage("Align Complete.")


def reset_transformObjectValue(obj, transform=True, userDefined=True):
    def _set_trsv(obj, trs):
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        for i, attr in enumerate(attrs):
            try:
                cmds.setAttr(f"{obj}.{attr}", trs[i])
            except Exception as e:
                om.MGlobal.displayInfo(str(e))

    if transform:
        _set_trsv(obj, [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
    if userDefined:
        user_defined = cmds.listAttr(obj, ud=1, u=1)
        if not user_defined:
            return
        for x in user_defined:
            try:
                v = cmds.addAttr(f"{obj}.{x}", q=1, dv=1)
                cmds.setAttr(f"{obj}.{x}", v)
            except Exception as e:
                om.MGlobal.displayInfo(str(e))


def reset_transformObjectValue_cmd(transform=True, userDefined=False):
    for obj in cmds.ls(sl=1):
        reset_transformObjectValue(obj, transform, userDefined)
    msg = "Reset value."
    if userDefined:
        msg = "Reset value (all)."
    showMessage(msg)


#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################\
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################


PELVIS = "RootX_M"
IK = ["IKLeg_L", "IKLeg_R", "IKArm_L", "IKArm_R", "PoleLeg_L", "PoleLeg_R", "PoleArm_L", "PoleArm_R"]


def build():
    if cmds.objExists("*MOVE_POSE*"):
        bake()
        return

    try:
        cmds.undoInfo(openChunk=1)
        with AssetCallback(name="MOVE_POSE", isDagAsset=True) as asset:
            sel = cmds.ls(sl=1)
            if not sel:
                raise RuntimeError("Please Select Controls!")

            namespace = ""
            if ":" in sel[0]:
                namespace = sel[0].split(":")[0]
            has_namespace = namespace in cmds.namespaceInfo(lon=1)

            controls = [f"{namespace}:{x}" if has_namespace else x for x in [PELVIS] + IK]

            # pos = cmds.xform(controls[0], q=1, ws=1, t=1)
            # pos[1] = 0
            pos = [0, 0, 0]

            move_handle = cmds.spaceLocator(name="MOVE_HANDLE")[0]
            cmds.setAttr(f"{move_handle}.localScale", 100, 100, 100)
            cmds.setAttr(f"{move_handle}.overrideEnabled", True)
            cmds.setAttr(f"{move_handle}.overrideColor", 14)
            cmds.xform(move_handle, t=pos, ws=1)

            # select time
            cmds.addAttr(asset, ln="moveBlend", min=0, max=1, dv=0, k=1)
            sel_end_time = cmds.currentTime(q=1)
            sel_start_time = sel_end_time - 1

            cmds.setKeyframe(f"{asset}.moveBlend", t=sel_start_time, v=0, inTangentType="linear", outTangentType="linear")
            cmds.setKeyframe(f"{asset}.moveBlend", t=sel_end_time, v=1, inTangentType="linear", outTangentType="linear")

            for x in controls:
                con = cmds.parentConstraint(move_handle, x, mo=1)
                blend_list = set()
                for node in cmds.listConnections(f"{con[0]}", d=1, s=0):
                    if cmds.objectType(node, isAType="pairBlend"):
                        blend_list.add(node)
                if blend_list:
                    for node in blend_list:
                        controls_blend_attr = cmds.listConnections(f"{node}.weight", s=1, d=0, p=1) or []
                        if controls_blend_attr:
                            attr = controls_blend_attr[0]
                            cmds.connectAttr(f"{asset}.moveBlend", attr, f=1)
                cmds.parent(con, move_handle)
            cmds.select(move_handle)

        for x in cmds.listAttr(asset, k=1):
            if x == "moveBlend":
                cmds.setAttr(f"{asset}.{x}", lock=0, k=0)
                continue
            cmds.setAttr(f"{asset}.{x}", lock=1, k=0)

    except Exception as e:
        cmds.undoInfo(closeChunk=1)
        cmds.undo()
        raise RuntimeError(e)
    finally:
        cmds.undoInfo(closeChunk=1)


def bake():
    asset = cmds.ls("*MOVE_POSE*")[0]
    node_list = cmds.container(asset, q=1, nodeList=1)

    controls_list = []

    for node in node_list:
        if cmds.objectType(node, isAType="constraint"):
            control = cmds.listConnections(f"{node}.constraintParentInverseMatrix", s=1, d=0)
            controls_list.extend(control)

    delete_attr = []
    for attr in cmds.listConnections("MOVE_POSE.moveBlend", d=1, s=0, p=1):
        delete_attr.append(attr)

    t = cmds.keyframe("MOVE_POSE.moveBlend", query=True, timeChange=True)[-1]
    cmds.currentTime(t)
    cmds.select(controls_list)
    cmds.setKeyframe()
    cmds.deleteAttr(delete_attr)
    print(delete_attr)
    cmds.delete(asset)


build()
