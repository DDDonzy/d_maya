import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

from face.fn.showMessage import showMessage
from face.fn.createBase import CreateBase, CreateNode
from face.fn.generateUniqueName import generateUniqueName

import numpy as np
import yaml

RAD_TO_DEG = 57.29577951308232     # 180.0 / pi
DEG_TO_RAD = 0.017453292519943295  # pi / 180.0


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
        axis = axis.lower()
        if axis not in "xyz":
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis="x"):
        return getattr(MIRROR_MATRIX, axis)


class UNIT_CONVERT(object):
    """
    unit convert class
    get current unit then return the conversion factor for the specified unit
    """
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


def mirror_transform(source_obj,
                     target_obj,
                     mirror_axis="x",):
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


def flip_transform(source_obj,
                   target_obj,
                   mirror_axis="x",):
    sour_worldMatrix = get_worldMatrix(source_obj)
    sour_worldMatrix_flip = flip_matrix(sour_worldMatrix, mirror_axis)
    set_worldMatrix(target_obj, sour_worldMatrix_flip)
    for x in "xyz":
        cmds.setAttr("{}.s{}".format(target_obj, x), abs(cmds.getAttr("{}.s{}".format(target_obj, x))))


def flip_matrix(worldMatrix,
                mirror_axis="x"):
    """flip matrix by mirror matrix

    Args:
        worldMatrix (om.MMatrix): input world matrix
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix
    """
    mirror_matrix = worldMatrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offsetMatrix(child_worldMatrix,
                     parent_worldMatrix):
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


def get_relativesMatrix(matrix,
                        referenceMatrix):
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


def get_localMatrix(obj):
    """get object's local space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: local matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return om.MFnTransform(mSel.getDagPath(0)).transformation().asMatrix()


def get_worldMatrix(obj):
    """get object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: world matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).inclusiveMatrix()


def get_parentMatrix(obj):
    """get object's parent object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: parent object's world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    return mSel.getDagPath(0).exclusiveMatrix()


def set_localMatrix(obj, matrix):
    """set maya object's local as input matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input local matrix
    """
    if cmds.objExists("{}.jointOrient".format(obj)):
        try:
            cmds.setAttr("{}.jointOrient".format(obj), 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_worldMatrix(obj, matrix):
    """ convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    localMatrix = matrix * mSel.getDagPath(0).exclusiveMatrixInverse()
    set_localMatrix(obj, localMatrix)


def matrix_to_trs(matrix, rotateOrder=0):
    """ convert matrix to maya's translate,rotate and scale

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
    mTransformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation([DEG_TO_RAD * angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    mTransformation.setTranslation(translate, 1)
    mTransformation.setRotation(euler_radians)
    mTransformation.setScale(scale, 1)
    return mTransformation.asMatrix()


def get_trs(obj):
    """get maya transform's transformation [tx,ty.tz,rx,ry,rz,sx,sy,sz]

    Args:
        obj (str): _description_

    Returns:
        list: [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    trs = []
    for attr in attrs:
        trs.append(cmds.getAttr("{}.{}".format(obj, attr)))
    return trs


def set_trs(obj, trs):
    """set maya transform [tx,ty.tz,rx,ry,rz,sx,sy,sz].
    Args:.
        obj (str): maya transform object'name.
        trs (list): [tx,ty.tz,rx,ry,rz,sx,sy,sz].
    """
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
    for i, attr in enumerate(attrs):
        try:
            cmds.setAttr("{}.{}".format(obj, attr), trs[i])
        except Exception as e:
            om.MGlobal.displayWarning(str(e))


def alignTransform(source, target):
    set_worldMatrix(target, get_worldMatrix(source))


def create_fbfByMatrix(matrix=om.MMatrix(), **kwargs):
    '''
    Create maya node "fourByFourMatrix". And set matrix data

    Return node name
    '''
    matrix_attrs = ["in00", "in01", "in02", "in03",
                    "in10", "in11", "in12", "in13",
                    "in20", "in21", "in22", "in23",
                    "in30", "in31", "in32", "in33"]
    fbf_node = CreateNode("fourByFourMatrix", **kwargs)
    for iter_idx, num in enumerate(matrix):
        attr_name = matrix_attrs[iter_idx]
        cmds.setAttr("{}.{}".format(fbf_node, attr_name), num)
    return fbf_node


class decomMatrix(CreateBase):
    """Create decompose a transformation matrix."""
    isDagAsset = False

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                name (str): is not name input, will be get name by args[-1] or  selections[-1]
                query (bool):  Default is False.
                edit (bool):  Default is False.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
                relativesMatrix (bool): Default is True.
                force (bool): Default is True.
        """

        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        self.isForce = kwargs.get("force", True) and kwargs.get("f", True)
        self.relativesMatrix = kwargs.get("relativesMatrix", True) and kwargs.get("rm", True)

        super(decomMatrix, self).__init__(*args, **kwargs)

    def create(self):
        self.hasJointOrient = cmds.objExists("{}.jointOrient".format(self.name))

        node_decom = CreateNode("decomposeMatrix", name=self.createName("decomposeMatrix"))
        node_mult = CreateNode("multMatrix", name=self.createName("getLocalMultMatrix"))
        node_matrixInverse = CreateNode("inverseMatrix", name=self.createName("inverseRelativesMatrix"))

        self.inputMatrix = None
        self.inputRotateOrder = None
        self.inputRelativeSpaceMatrix = None
        self.outputTranslate = None
        self.outputRotate = None
        self.outputScale = None
        self.outputShear = None

        self.publishAttr(data={"inputMatrix": "{}.matrixIn[0]".format(node_mult),
                               "inputRotateOrder": "{}.inputRotateOrder".format(node_decom),
                               "inputRelativeSpaceMatrix": "{}.inputMatrix".format(node_matrixInverse),
                               "outputTranslate": "{}.outputTranslate".format(node_decom),
                               "outputRotate": "{}.outputRotate".format(node_decom),
                               "outputScale": "{}.outputScale".format(node_decom),
                               "outputShear": "{}.outputShear".format(node_decom)})

        # Internal connects
        cmds.connectAttr("{}.outputMatrix".format(node_matrixInverse), "{}.matrixIn[1]".format(node_mult))
        cmds.connectAttr("{}.matrixSum".format(node_mult), "{}.inputMatrix".format(node_decom))
        if self.hasJointOrient:
            node_euler_to_quat = CreateNode("eulerToQuat", name=self.createName("eulerToQuat"))
            node_invert_quat = CreateNode("quatInvert", name=self.createName("invertQuat"))
            node_prod_quat = CreateNode("quatProd", name=self.createName("prodQuat"))
            node_quat_to_euler = CreateNode("quatToEuler", name=self.createName("quatToEuler"))

            cmds.connectAttr("{}.inputRotateOrder".format(node_decom), "{}.inputRotateOrder".format(node_euler_to_quat))
            cmds.connectAttr("{}.inputRotateOrder".format(node_decom), "{}.inputRotateOrder".format(node_quat_to_euler))
            cmds.connectAttr("{}.outputQuat".format(node_decom), "{}.input1Quat".format(node_prod_quat))
            cmds.connectAttr("{}.outputQuat".format(node_euler_to_quat), "{}.inputQuat".format(node_invert_quat))
            cmds.connectAttr("{}.outputQuat".format(node_invert_quat), "{}.input2Quat".format(node_prod_quat))
            cmds.connectAttr("{}.outputQuat".format(node_prod_quat), "{}.inputQuat".format(node_quat_to_euler))

            self.inputJointOrient = None
            self.outputRotate = None
            self.publishAttr(data={"inputJointOrient": "{}.inputRotate".format(node_euler_to_quat),
                                   "outputRotate": "{}.outputRotate".format(node_quat_to_euler)})

        # External connects
        if cmds.objExists(self.name):
            if self.hasJointOrient:
                cmds.connectAttr("{}.jointOrient".format(self.name), self.inputJointOrient)  # in jointOrient
            if self.relativesMatrix:
                cmds.connectAttr("{}.parentMatrix[0]".format(self.name), self.inputRelativeSpaceMatrix)  # input relatives space matrix
            cmds.connectAttr("{}.rotateOrder".format(self.name), self.inputRotateOrder)  # in rotateOrder
            if self.translate:
                cmds.connectAttr(self.outputTranslate, "{}.translate".format(self.name), f=self.isForce)  # out translate
            if self.scale:
                cmds.connectAttr(self.outputScale, "{}.scale".format(self.name), f=self.isForce)  # out scale
            if self.shear:
                cmds.connectAttr(self.outputShear, "{}.shear".format(self.name), f=self.isForce)  # out shear
            if self.rotate:
                cmds.connectAttr(self.outputRotate, "{}.rotate".format(self.name), f=self.isForce)  # out rotate
                # cmds.connectAttr(f"{_assets}.outputQuat", f"{name}.rotateQuaternion")  # out rotate


class relativesMatrix(CreateBase):
    """Create relatives matrix node"""
    isDagAsset = False

    def create(self):
        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))
        node_inverseMatrix = CreateNode("inverseMatrix", name=self.createName("inverseMatrix"))
        cmds.connectAttr("{}.outputMatrix".format(node_inverseMatrix), "{}.matrixIn[1]".format(node_multMatrix))

        self.inputMatrix = None
        self.inputRelativeMatrix = None
        self.outputMatrix = None
        self.publishAttr(data={"inputMatrix": "{}.matrixIn[0]".format(node_multMatrix),
                               "inputRelativeMatrix": "{}.inputMatrix".format(node_inverseMatrix),
                               "outputMatrix": "{}.matrixSum".format(node_multMatrix)})


class matrixConstraint(CreateBase):
    """Create matrix constraint node"""
    isDagAsset = False

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
                controller: args[0], If not args, will be get it from selection list[0]
                target: args[1], If not args, will be get it from selection list[1]
            **kwargs: Arbitrary keyword arguments.
                query (bool): Default is False.
                edit (bool): Default is False.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
        """
        self.keepOffset = kwargs.get("maintainOffset", True) and kwargs.get("mo", True)
        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        if len(args) == 2:
            self.controller, self.target = args
        else:
            sel = cmds.ls(sl=1)
            if len(sel) == 2:
                self.controller, self.target = sel
            else:
                raise RuntimeError("Please input or select two objects.")
        self.name = self.target

        super(matrixConstraint, self).__init__(*args, **kwargs)

    def create(self):
        self.hasJointOrient = cmds.objExists("{}.jointOrient".format(self.target))

        offsetMatrix = get_offsetMatrix(child_worldMatrix=get_worldMatrix(obj=self.target),
                                        parent_worldMatrix=get_worldMatrix(obj=self.controller))

        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))

        node_decom = decomMatrix(name=self.name,
                                 translate=self.translate,
                                 rotate=self.rotate,
                                 scale=self.scale,
                                 shear=self.shear)

        self.publishAttr(data={"inputOffsetMatrix": "{}.matrixIn[0]".format(node_multMatrix),
                               "inputControllerMatrix": "{}.matrixIn[1]".format(node_multMatrix),
                               "inputRotateOrder": node_decom.inputRotateOrder,
                               "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                               "outputTranslate": node_decom.outputTranslate,
                               "outputRotate": node_decom.outputRotate,
                               "outputScale": node_decom.outputScale,
                               "outputShear": node_decom.outputShear})
        if self.hasJointOrient:
            self.publishAttr(data={"inputTargetJointOrient": node_decom.inputJointOrient})

        # Internal connects
        cmds.connectAttr("{}.matrixSum".format(node_multMatrix), node_decom.inputMatrix)
        # External connects
        if self.keepOffset:
            cmds.setAttr("{}.matrixIn[0]".format(node_multMatrix), offsetMatrix, type="matrix")
        cmds.connectAttr("{}.worldMatrix[0]".format(self.controller), "{}.matrixIn[1]".format(node_multMatrix))


class parentSpaceConstraint(CreateBase):
    """Create parentspace constraint"""

    isDagAsset = False
    attrName = "parentSpace"

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                translate (bool): Default is True.
                rotate (bool): Default is True.
                scale (bool): Default is True.
                shear (bool): Default is True.
                niceName (str or list): A nice name for the controller(s). Default is an empty list.
                force (bool): Default is False.
        """
        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)

        # get controller and target
        if len(args) < 2:
            sel = cmds.ls(sl=1)
            if len(sel) < 2:
                raise RuntimeError("Please select at least 2 objects.")
            self.target = sel.pop()
            self.controller = sel
        else:
            self.target = args.pop()
            self.controller = args
        # get nice name
        self.niceName = kwargs.get("niceName") or kwargs.get("nn") or []
        if not isinstance(self.niceName, list):
            self.niceName = [self.niceName]
        if len(self.niceName) != len(self.controller):
            self.niceName = self.controller

        # create \ edit \ query
        self.isForce = kwargs.get("force") or kwargs.get("f") or False
        if cmds.objExists("{}.{}".format(self.target, self.attrName)):
            if self.isForce:
                cmds.deleteAttr("{}.{}".format(self.target, self.attrName))
            else:
                self.isEdit = True

        super(parentSpaceConstraint, self).__init__(*args, **kwargs)

    def create(self):
        self.createParentSpaceLogic()
        for i, controller in enumerate(self.controller):
            self.addParentSpaceController(controller=controller,
                                          niceName=self.niceName[i])

    def createParentSpaceLogic(self):
        localMatrix = get_localMatrix(self.target)
        # connect to chose
        node_choseControllerMatrix = CreateNode("choice", name=self.createName("choice"))
        node_choseOffsetMatrix = CreateNode("choice", name=self.createName(keyword="offsetChoice"))
        # add matrix
        cmds.addAttr(node_choseControllerMatrix, ln="controllerMatrix", at="matrix", m=1)
        cmds.addAttr(node_choseOffsetMatrix, ln="offsetMatrix", at="matrix", m=1)
        cmds.connectAttr("{}.controllerMatrix[0]".format(node_choseControllerMatrix), "{}.input[0]".format(node_choseControllerMatrix))
        cmds.connectAttr("{}.offsetMatrix[0]".format(node_choseOffsetMatrix), "{}.input[0]".format(node_choseOffsetMatrix))

        # cal world matrix
        node_calWorldMatrix = CreateNode("multMatrix", name=self.createName("parentMultMatrix"))
        cmds.connectAttr("{}.output".format(node_choseOffsetMatrix), "{}.matrixIn[0]".format(node_calWorldMatrix))
        cmds.connectAttr("{}.output".format(node_choseControllerMatrix), "{}.matrixIn[1]".format(node_calWorldMatrix))
        # chose to decomposeMatrix
        node_decom = decomMatrix(name=self.name,
                                 translate=self.translate,
                                 rotate=self.rotate,
                                 scale=self.scale,
                                 shear=self.shear)
        cmds.connectAttr("{}.matrixSum".format(node_calWorldMatrix), node_decom.inputMatrix)
        # add parentspace switch attr
        cmds.addAttr(node_choseControllerMatrix, ln=self.attrName, at="enum", en="Parent", k=1)

        self.publishAttr(data={"inputRotateOrder": node_decom.inputRotateOrder,
                               "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                               "outputTranslate": node_decom.outputTranslate,
                               "outputRotate": node_decom.outputRotate,
                               "outputScale": node_decom.outputScale,
                               "outputShear": node_decom.outputShear,
                               "parentspace": "{}.{}".format(node_choseControllerMatrix, self.attrName),
                               "controllerMatrix": "{}.controllerMatrix".format(node_choseControllerMatrix),
                               "offsetMatrix": "{}.offsetMatrix".format(node_choseOffsetMatrix)})

        cmds.connectAttr(self.parentspace, "{}.selector".format(node_choseControllerMatrix))
        cmds.connectAttr("{}.selector".format(node_choseControllerMatrix), "{}.selector".format(node_choseOffsetMatrix))

        # parent matrix * base local matrix
        cmds.connectAttr("{}.parentMatrix[0]".format(self.target), "{}[0]".format(self.controllerMatrix))
        cmds.setAttr("{}[0]".format(self.offsetMatrix), localMatrix, type="matrix")

        # add parentspace attr to obj
        if cmds.objExists("{}.{}".format(self.target, self.attrName)):
            cmds.deleteAttr("{}.{}".format(self.target, self.attrName))
        cmds.addAttr(self.target, ln=self.attrName, k=1, pxy=self.parentspace)
        # add info
        cmds.addAttr(self.target, ln="parentSpaceChoice", at="message")
        cmds.addAttr(node_choseControllerMatrix, ln="parentSpaceTarget", at="message")
        cmds.connectAttr("{}.parentSpaceTarget".format(node_choseControllerMatrix), "{}.parentSpaceChoice".format(self.target))

    def addParentSpaceController(self,
                                 controller,
                                 niceName):

        # get index
        enum_str = cmds.addAttr("{}.{}".format(self.target, self.attrName), q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(niceName)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # update parentspace enum
        cmds.addAttr("{}.{}".format(self.target, self.attrName), e=1, en=enum_str)
        cmds.addAttr(self.parentspace, e=1, en=enum_str)

        # offset matrix to chose
        offsetMatrix = get_offsetMatrix(get_worldMatrix(self.target),
                                        get_worldMatrix(controller))
        cmds.setAttr("{}[{}]".format(self.offsetMatrix, parent_indices), offsetMatrix, type="matrix")
        # controller matrix to chose
        cmds.connectAttr("{}.worldMatrix[0]".format(controller), "{}[{}]".format(self.controllerMatrix, parent_indices))

        # update chose input data
        controller_chose = cmds.listConnections("{}[0]".format(self.controllerMatrix), p=0, d=1, s=0)[0]
        offset_chose = cmds.listConnections("{}[0]".format(self.offsetMatrix), p=0, d=1, s=0)[0]
        cmds.connectAttr("{}[{}]".format(self.controllerMatrix, parent_indices), "{}.input[{}]".format(controller_chose, parent_indices))
        cmds.connectAttr("{}[{}]".format(self.offsetMatrix, parent_indices), "{}.input[{}]".format(offset_chose, parent_indices))


class offsetFK(CreateBase):
    """Create offset fk system"""

    def __init__(self, *args, **kwargs):
        """
            Args:
            *args: Variable length argument list.
                args[0] (list): List of controllers if not provided in kwargs.
                args[1] (list): List of offsets if not provided in kwargs.
            **kwargs: Arbitrary keyword arguments.
                controllerList (list): List of controllers. Default is an empty list.
                offsetList (list): List of offsets. Default is an empty list.
        """
        # get parameter
        self.controllerList = kwargs.get("controllerList") or kwargs.get("cl") or []
        self.offsetList = kwargs.get("offsetList") or kwargs.get("ol") or []
        #
        if not self.controllerList:
            self.controllerList = args[0] if args else []
        if not self.offsetList:
            self.offsetList = args[1] if args else []
        if not self.controllerList or not self.offsetList:
            raise RuntimeError("Input error!")

        super(offsetFK, self).__init__(*args, **kwargs)

    def create(self):
        for i, control in enumerate(self.controllerList[:-1]):
            offset = self.offsetList[i]
            next_offset = self.offsetList[i + 1]
            next_control = self.controllerList[i + 1]

            node_multMatrix = CreateNode("multMatrix", name="{}_multMatrix_{}1".format(next_control, self.thisType))
            node_decom = decomMatrix(name=next_offset)
            # get offset matrix from 'offset_obj' with 'next offset_obj'
            cmds.connectAttr("{}.parentMatrix[0]".format(next_offset),
                             "{}.matrixIn[0]".format(node_multMatrix))
            cmds.connectAttr("{}.parentInverseMatrix[0]".format(offset),
                             "{}.matrixIn[1]".format(node_multMatrix))
            # controller constraint it
            cmds.connectAttr("{}.worldMatrix[0]".format(control),
                             "{}.matrixIn[2]".format(node_multMatrix))
            # matrix to trs
            cmds.connectAttr("{}.matrixSum".format(node_multMatrix),
                             node_decom.inputMatrix)


class _uvPin(CreateBase):
    """Create uvPin constraint"""
    isBlackBox = False

    def __init__(self, *args, **kwargs):
        """
            Args:
            *args: Variable length argument list.
                args[0] (list): List of target objects if not provided in kwargs.
            **kwargs: Arbitrary keyword arguments.
                targetList (list): List of target objects. Default is the current selection.
                size (float): Size of the UV pin. Default is 0.1.
                name (str): Name of the UV pin. Default is 'uvPin'.
        """

        self.targetList = kwargs.get("targetList") or kwargs.get("tl") or args[0] if args else cmds.ls(sl=1)
        self.size = kwargs.get("size") or kwargs.get("s") or 0.1
        self.name = kwargs.get("name") or kwargs.get("n") or 'uvPin'

        if not isinstance(self.targetList, list):
            self.targetList = [self.targetList]
        if not self.targetList:
            raise ValueError("No object need to create uvPin, please input object list. or select some object.")

        super(_uvPin, self).__init__(*args, **kwargs)

    def create(self):
        # create mesh
        self.mesh, self.meshShape = uvPin.create_planeByObjectList(targetList=self.targetList,
                                                                   size=self.size,
                                                                   name="{}_uvPinMesh".format(self.name))
        # create uvPin node
        self.uvPinNode = CreateNode("uvPin", name="{}_uvPin".format(self.name))
        orig_outMesh = cmds.deformableShape(self.mesh, cog=1)[0]
        cmds.setAttr("{}.normalAxis".format(self.uvPinNode), 0)
        cmds.setAttr("{}.tangentAxis".format(self.uvPinNode), 5)
        cmds.setAttr("{}.uvSetName".format(self.uvPinNode),
                     uvPin.get_currentUVSetName(self.mesh),
                     type="string")
        cmds.connectAttr(orig_outMesh,
                         "{}.originalGeometry".format(self.uvPinNode))
        cmds.connectAttr("{}.worldMesh[0]".format(self.mesh),
                         "{}.deformedGeometry".format(self.uvPinNode))
        for i, obj in enumerate(self.targetList):
            # set uvPin.uv value
            cmds.setAttr("{}.coordinate[{}].coordinateU".format(self.uvPinNode, i), i + 0.5)
            cmds.setAttr("{}.coordinate[{}].coordinateV".format(self.uvPinNode, i), 0.5)
            node_decom = decomMatrix(name=obj, scale=False, shear=False)
            cmds.connectAttr("{}.outputMatrix[{}]".format(self.uvPinNode, i), node_decom.inputMatrix)

    @staticmethod
    def create_planeByObjectList(targetList, size=0.1, name="uvPinPlane", buildInMaya=True):
        if not targetList:
            raise ValueError("No object need to create plane, please input object list first.")
        num = len(targetList)

        base_vtx_pos_ary = [[0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
        base_poly_count = [3, 3, 3, 3]
        base_poly_connect = [1, 4, 0, 4, 3, 0, 3, 2, 0, 2, 1, 0]
        base_uvCounts = [3, 3, 3, 3]
        base_uvIds = [0, 1, 2, 1, 3, 2, 3, 4, 2, 4, 0, 2]
        base_u = [1, 0.5, 0.5, 0, 0.5]
        base_v = [0.5, 1, 0.5, 0.5, 0]

        base_vtx_num = len(base_vtx_pos_ary)
        pos_ary = []
        face_connect_ary = []
        face_count_ary = base_poly_count * num

        uvCounts = base_uvCounts * num
        u = []
        v = base_v * num
        uvIds = []

        info = []
        # num
        for i in range(num):
            info.append({"driven": targetList[i], "meshComponent": list(range(5*i, 5*i+5))})
            # pos_ary
            mult_matrix = get_worldMatrix(targetList[i])
            for pos in base_vtx_pos_ary:
                pos_ary.append(om.MPoint(pos) * size * mult_matrix)
            # face_connect_ary
            for vtx in base_poly_connect:
                face_connect_ary.append(vtx + (i * base_vtx_num))
            # u
            for u_value in base_u:
                u.append(u_value+i)
            # uvIds
            for id in base_uvIds:
                uvIds.append(id + (i * base_vtx_num))

        if not buildInMaya:
            data = om.MFnMeshData()
            mObject = data.create()
            fnMesh = om.MFnMesh()
            fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
            fnMesh.setUVs(u, v)
            fnMesh.assignUVs(uvCounts, uvIds)
            return fnMesh, data

        fnMesh = om.MFnMesh()
        transform = CreateNode("transform", name=name)
        mObject = om.MSelectionList().add(transform).getDependNode(0)
        mObj = fnMesh.create(pos_ary, face_count_ary, face_connect_ary, parent=mObject)
        fnMesh.setUVs(u, v)
        fnMesh.assignUVs(uvCounts, uvIds)
        fnDep = om.MFnDependencyNode(mObj)
        fnDep.setName("{}Shape".format(transform))

        try:
            cmds.addAttr(transform, ln="notes", dt="string")
        except:
            pass

        infoStr = yaml.dump(info, indent=4)
        cmds.setAttr("{}.notes".format(transform), infoStr, type="string")

        return str(transform), str(fnDep.name())

    @staticmethod
    def get_UVByClosestPoint(point, shape):
        p = om.MPoint(point)
        sel = om.MGlobal.getSelectionListByName(shape)
        dag = sel.getDagPath(0)
        fn_mesh = om.MFnMesh(dag)
        set_name = fn_mesh.currentUVSetName()
        return fn_mesh.getUVAtPoint(p, space=om.MSpace.kWorld, uvSet=set_name)[0:2]

    @staticmethod
    def get_currentUVSetName(shape):
        sel = om.MGlobal.getSelectionListByName(shape)
        dag = sel.getDagPath(0)
        fn_mesh = om.MFnMesh(dag)
        return fn_mesh.currentUVSetName()

    @staticmethod
    def normalizedWeights(uvPinMesh, skinCluster):
        mSel = om.MSelectionList()
        mSel.add(uvPinMesh)
        mSel.add(skinCluster)
        uvPinMesh_mDag = mSel.getDagPath(0)
        skin_mObj = mSel.getDependNode(1)
        fnSkin = oma.MFnSkinCluster(skin_mObj)
        singleIdComp = om.MFnSingleIndexedComponent()
        vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
        weight, infCount = fnSkin.getWeights(uvPinMesh_mDag, vertexComp)
        weightAry = np.array(weight)
        weightAry = weightAry.reshape(int(len(weightAry)/infCount), infCount)
        for i in range(0, len(weightAry) - 4, 4 + 1):
            weightAry[i + 1:i + 1 + 4] = weightAry[i]
        weightAry = weightAry.reshape(1, len(weight))[0]
        fnSkin.setWeights(uvPinMesh_mDag, vertexComp, om.MIntArray(list(range(infCount))), om.MDoubleArray(weightAry))


class _follicle(_uvPin):
    """Create follicle constraint """

    def __init__(self, *args, **kwargs):
        super(_follicle, self).__init__(*args, **kwargs)

    def create(self):
        self.mesh, self.meshShape = _uvPin.create_planeByObjectList(targetList=self.targetList,
                                                                   size=self.size,
                                                                   name="{}_uvPinMesh".format(self.name))
        self.uvPinNode = []
        for i, obj in enumerate(self.targetList):
            node_follicle = generateUniqueName("{}_follicle".format(obj))
            node_follicle = CreateNode("transform", name=node_follicle)
            cmds.setAttr("{}.v".format(node_follicle), 0)
            cmds.setAttr("{}.inheritsTransform".format(node_follicle), 0)
            follicle_shape = CreateNode("follicle", name="{}Shape".format(node_follicle), parent=node_follicle)
            cmds.connectAttr("{}.outMesh".format(self.mesh), "{}.inputMesh".format(follicle_shape))
            cmds.connectAttr("{}.worldMatrix[0]".format(self.mesh), "{}.inputWorldMatrix".format(follicle_shape))
            cmds.setAttr("{}.parameterU".format(follicle_shape), i + 0.5)
            cmds.setAttr("{}.parameterV".format(follicle_shape), 0.5)
            cmds.connectAttr("{}.outTranslate".format(follicle_shape), "{}.translate".format(node_follicle))
            cmds.connectAttr("{}.outRotate".format(follicle_shape), "{}.rotate".format(node_follicle))
            matrixConstraint(node_follicle, obj, scale=False, shear=False)
            self.uvPinNode.append(follicle_shape)

def reset_transformObjectValue(obj, transform=True, userDefined=True):
    def _set_trsv(obj, trs):
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
        for i, attr in enumerate(attrs):
            try:
                cmds.setAttr("{}.{}".format(obj, attr), trs[i])
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
                v = cmds.addAttr("{}.{}".format(obj, x), q=1, dv=1)
                cmds.setAttr("{}.{}".format(obj, x), v)
            except Exception as e:
                om.MGlobal.displayInfo(str(e))


def reset_transformObjectValue_cmd(transform=True, userDefined=False):
    for obj in cmds.ls(sl=1):
        reset_transformObjectValue(obj, transform, userDefined)
    msg = "Reset value."
    if userDefined:
        msg = "Reset value (all)."
    showMessage(msg)


if cmds.about(api=1) >= 20230000:
    uvPin = _uvPin
else:
    uvPin = _follicle
