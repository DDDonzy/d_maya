import maya.cmds as cmds
import maya.api.OpenMaya as om
from UTILS.ui.showMessage import showMessage

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


def set_localMatrix(obj: str, matrix: om.MMatrix, rotateOrder: int = 0) -> None:
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
    set_trs(obj, matrix_to_trs(matrix, rotateOrder))


def set_worldMatrix(obj: str, matrix: om.MMatrix, rotateOrder: int = 0) -> None:
    """convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    localMatrix = matrix * mSel.getDagPath(0).exclusiveMatrixInverse()
    set_localMatrix(obj, localMatrix, rotateOrder)


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
