import maya.cmds as cmds
import maya.api.OpenMaya as om


class MIRROR_MATRIX():
    x = om.MMatrix([[-1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    y = om.MMatrix([[1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    z = om.MMatrix([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]])

    def __init__(self, axis: str = "x"):
        if axis not in ["x", "y", "z"]:
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis: str = "x"):
        return getattr(MIRROR_MATRIX, axis)


class UNIT_CONVERT():
    mm = 10.0
    cm = 1.0
    m = 0.01

    def __init__(self, unit: str = cmds.currentUnit(q=1)):
        if unit not in ["mm", "cm", "m"]:
            raise ValueError("Invalid axis. Choose from 'mm', 'cm', or 'm'.")

    def __new__(cls, unit: str = cmds.currentUnit(q=1)):
        return getattr(UNIT_CONVERT, unit)


def mirror_transform(sour_obj: str,
                     target_obj: str,
                     mirror_axis: str = "x",):
    '''set object mirror world matrix'''
    sour_world_matrix = get_world_matrix(sour_obj)
    sour_parent_matrix = get_parent_matrix(sour_obj)
    sour_world_matrix_flip = flip_matrix(sour_world_matrix, mirror_axis)
    sour_parent_matrix_flip = flip_matrix(sour_parent_matrix, mirror_axis)
    target_parent_matrix = get_parent_matrix(target_obj)
    flip_offset_matrix = get_offset_matrix(sour_parent_matrix_flip, target_parent_matrix)
    set_world_matrix(target_obj, flip_offset_matrix * sour_world_matrix_flip)


def flip_matrix(world_matrix: om.MMatrix,
                mirror_axis: str = "x") -> om.MMatrix:
    mirror_matrix = world_matrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offset_matrix(child_world_matrix: om.MMatrix,
                      parent_world_matrix: om.MMatrix) -> om.MMatrix:
    """
    get offset matrix
    get local matrix when child in parent space

    Args:
        child_world_matrix (om.MMatrix): child world matrix
        parent_world_matrix (om.MMatrix): parent world matrix

    Returns:
        om.MMatrix: local matrix when child in parent space
    """
    # child_world_matrix = child_local_matrix * parent_world_matrix
    # child_world_matrix * parent_world_matrix.inverse = child_local_matrix
    child_local_matrix = child_world_matrix * parent_world_matrix.inverse()
    return child_local_matrix


def get_local_matrix(obj: str) -> om.MMatrix:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return om.MFnTransform(sel_list.getDagPath(0)).transformation().asMatrix()


def get_world_matrix(obj: str) -> om.MMatrix:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def get_parent_matrix(obj: str) -> om.MMatrix:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).exclusiveMatrix()


def set_local_matrix(obj: str, matrix: om.MMatrix) -> None:
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_world_matrix(obj: str, matrix: om.MMatrix) -> None:
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    local_matrix = matrix * sel_list.getDagPath(0).exclusiveMatrixInverse()
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix: om.MMatrix, rotateOrder: int = 0) -> list:
    om_transformation = om.MTransformationMatrix(matrix)
    translate = om_transformation.translation(1) * UNIT_CONVERT()
    euler_radians = om_transformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [57.29577951308232*radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = om_transformation.scale(1)
    outputList = [translate[0], translate[1], translate[2],
                  euler_angle[0], euler_angle[1], euler_angle[2],
                  scale[0], scale[1], scale[2], ]
    return outputList


def trs_to_matrix(trs: list, rotateOrder: int = 0) -> om.MMatrix:
    om_transformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation(*[0.017453292520882225*angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    om_transformation.setTranslation(translate, 1)
    om_transformation.setRotation(euler_radians)
    om_transformation.setScale(scale, 1)
    return om_transformation.asMatrix()


def get_trs(obj: str) -> list:
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr(f"{obj}.{attr}"))
    return trs


def set_trs(obj: str, trs: list) -> None:
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr(f"{obj}.{attr}", trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def createNode_fbf(matrix: om.MMatrix = om.MMatrix(), **kwargs) -> str:
    '''
    Create maya node "fourByFourMatrix". And set matrix data

    Return node name
    '''
    matrix_attrs = ["in00", "in01", "in02", "in03",
                    "in10", "in11", "in12", "in13",
                    "in20", "in21", "in22", "in23",
                    "in30", "in31", "in32", "in33"]
    fbf_node = cmds.createNode("fourByFourMatrix", **kwargs)
    for iter_idx, num in enumerate(matrix):
        attr_name = matrix_attrs[iter_idx]
        cmds.setAttr(f"{fbf_node}.{attr_name}", num)
    return fbf_node
