import maya.cmds as cmds
import maya.api.OpenMaya as om
import functools

RAD_TO_DEG = 57.29577951308232  # 180.0 / pi
DEG_TO_RAD = 0.017453292519943295  # pi / 180.0


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
    set_trs(obj, matrix_to_trs(matrix, cmds.getAttr(f"{obj}.rotateOrder")))


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


try:
    namespace = cmds.ls(sl=1)[-1].split(":")[0]
except:
    raise RuntimeError("请选择Root控制器")
root = "FKRootControls_M"
move_controls = ["IKLeg_R", "IKLeg_L", "RootX_M", "IKArm_L", "IKArm_R", "PoleArm_R", "PoleArm_L", "PoleLeg_R", "PoleLeg_L"]

root_matrix = get_worldMatrix(f"{namespace}:{root}")
offset = []
fun_list = []
for x in move_controls:
    m = get_worldMatrix(f"{namespace}:{x}") * root_matrix
    fun_list.append(functools.partial(set_worldMatrix, f"{namespace}:{x}", m))
for x in fun_list:
    x()
