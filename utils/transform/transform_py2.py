import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.api.OpenMaya as om


class MIRROR_MATRIX(object):
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

    def __init__(self, axis="x"):
        if axis not in ["x", "y", "z"]:
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis="x"):
        return getattr(MIRROR_MATRIX, axis)


class UNIT_CONVERT(object):
    mm = 10.0
    cm = 1.0
    m = 0.01

    def __init__(self, unit=None):
        if unit is None:
            unit = cmds.currentUnit(q=1)
        if unit not in ["mm", "cm", "m"]:
            raise ValueError("Invalid axis. Choose from 'mm', 'cm', or 'm'.")

    def __new__(cls, unit=None):
        if unit is None:
            unit = cmds.currentUnit(q=1)
        return getattr(UNIT_CONVERT, unit)


def mirror_transform(sour_obj, target_obj, mirror_axis="x"):
    """flip source object's world space matrix  as target object's world space matrix 

    Args:
        sour_obj (str): source transform object
        target_obj (str): target transform object
        mirror_axis (str, optional): mirror axis. Defaults to "x".
    """
    sour_world_matrix = get_world_matrix(sour_obj)
    sour_parent_matrix = get_parent_matrix(sour_obj)
    sour_world_matrix_flip = flip_matrix(sour_world_matrix, mirror_axis)
    sour_parent_matrix_flip = flip_matrix(sour_parent_matrix, mirror_axis)
    target_parent_matrix = get_parent_matrix(target_obj)
    flip_offset_matrix = get_offset_matrix(sour_parent_matrix_flip, target_parent_matrix)
    set_world_matrix(target_obj, flip_offset_matrix * sour_world_matrix_flip)


def flip_matrix(world_matrix, mirror_axis="x"):
    """flip matrix by mirror matrix

    Args:
        world_matrix (om.MMatrix): input world matrix 
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix 
    """
    mirror_matrix = world_matrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offset_matrix(child_world_matrix, parent_world_matrix):
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


def get_local_matrix(obj):
    """get object's local space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: local matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return om.MFnTransform(sel_list.getDagPath(0)).transformation().asMatrix()


def get_world_matrix(obj):
    """get object's world space matrix 

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: world matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def get_parent_matrix(obj):
    """get object's parent object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: parent object's world space matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).exclusiveMatrix()


def set_local_matrix(obj, matrix):
    """set maya object's local as input matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input local matrix
    """
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr("%s.jointOrient" % obj, 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_world_matrix(obj, matrix):
    """ convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name 
        matrix (om.MMatrix): input world space matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    local_matrix = matrix * sel_list.getDagPath(0).exclusiveMatrixInverse()
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr("%s.jointOrient" % obj, 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix, rotateOrder=0):
    """ convert matrix to maya's translate, rotate and scale

    Args:
        matrix (om.MMatrix): input matrix
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        list: [tx, ty, tz, rx, ry, rz, sx, sy, sz]
    """
    om_transformation = om.MTransformationMatrix(matrix)
    translate = om_transformation.translation(1) * UNIT_CONVERT
    euler_radians = om_transformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [57.29577951308232 * radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = om_transformation.scale(1)
    outputList = [translate[0], translate[1], translate[2],
                  euler_angle[0], euler_angle[1], euler_angle[2],
                  scale[0], scale[1], scale[2], ]
    return outputList


def trs_to_matrix(trs, rotateOrder=0):
    """convert [tx,ty.tz,rx,ry,rz,sx,sy,sz] to matrix 

    Args:
        trs (list): input [tx,ty.tz,rx,ry,rz,sx,sy,sz]
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        om.MMatrix: matrix
    """
    om_transformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation([0.017453292520882225*angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    om_transformation.setTranslation(translate, 1)
    om_transformation.setRotation(euler_radians)
    om_transformation.setScale(scale, 1)
    return om_transformation.asMatrix()


def get_trs(obj):
    """get maya transform's transformation [tx,ty,tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): _description_

    Returns:
        list: [tx,ty,tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr("%s.%s" % (obj, attr)))
    return trs


def set_trs(obj, trs):
    """set maya transform [tx,ty,tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): maya transform object'name
        trs (list): [tx,ty,tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr("%s.%s" % (obj, attr), trs[i])
        except Exception, e:
            om.MGlobal.displayWarning(str(e))


def createNode_fbf(matrix=om.MMatrix(), **kwargs):
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
        cmds.setAttr("%s.%s" % (fbf_node, attr_name), num)
    return fbf_node


def matrix_constraint(source_obj, target_object, keep_offset=True):
    offset_matrix = get_offset_matrix(get_world_matrix(target_object), get_world_matrix(source_obj))
    node_multMatrix = cmds.createNode("multMatrix", name="%s_MM_matrixConstraint" % target_object)
    cmds.addAttr(node_multMatrix, ln="constraintOffsetMatrix", at="matrix")
    if keep_offset:
        cmds.setAttr("%s.constraintOffsetMatrix" % node_multMatrix, offset_matrix, type="matrix")
    cmds.connectAttr("%s.constraintOffsetMatrix" % node_multMatrix,
                     "%s.matrixIn[0]" % node_multMatrix)
    cmds.connectAttr("%s.worldMatrix[0]" % source_obj,
                     "%s.matrixIn[1]" % node_multMatrix)
    cmds.connectAttr("%s.parentInverseMatrix[0]" % target_object,
                     "%s.matrixIn[2]" % node_multMatrix)
    node_decomposeMatrix = cmds.createNode("decomposeMatrix", name="%s_DM_matrixConstraint" % target_object)
    cmds.connectAttr("%s.rotateOrder" % target_object,
                     "%s.inputRotateOrder" % node_decomposeMatrix)
    cmds.connectAttr("%s.matrixSum" % node_multMatrix,
                     "%s.inputMatrix" % node_decomposeMatrix)
    cmds.connectAttr("%s.outputTranslate" % node_decomposeMatrix,
                     "%s.translate" % target_object)
    cmds.connectAttr("%s.outputRotate" % node_decomposeMatrix,
                     "%s.rotate" % target_object)
    cmds.connectAttr("%s.outputScale" % node_decomposeMatrix,
                     "%s.scale" % target_object)
    cmds.connectAttr("%s.outputShear" % node_decomposeMatrix,
                     "%s.shear" % target_object)
    cmds.connectAttr("%s.outputQuat" % node_decomposeMatrix,
                     "%s.rotateQuaternion" % target_object)

    if cmds.objectType(target_object) == "joint":
        cmds.setAttr("%s.jointOrient" % target_object, 0, 0, 0)
    # assets box
    if not cmds.ls("RigAssets"):
        cmds.container(name="RigAssets")
        cmds.setAttr("RigAssets.blackBox", 1)
    if not cmds.ls("MatrixConstraintAssets"):
        cmds.container(name="MatrixConstraintAssets")
        cmds.container("RigAssets", e=1, addNode="MatrixConstraintAssets")
        cmds.setAttr("MatrixConstraintAssets.blackBox", 1)

    matrixConstraint_assets = cmds.container(name="%s_matrixConstraint" % target_object, addNode=[node_multMatrix, node_decomposeMatrix])
    cmds.container("MatrixConstraintAssets", e=1, addNode=matrixConstraint_assets)
    cmds.setAttr("%s.blackBox" % matrixConstraint_assets, 1)
