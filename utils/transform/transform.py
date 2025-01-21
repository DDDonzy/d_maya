import maya.cmds as cmds
import maya.api.OpenMaya as om
from UTILS.generateUniqueName import generateUniqueName
from UTILS.ui.showMessage import showMessage
from UTILS.createBase import CreatorBase, CreateNode

RAD_TO_DEG = 57.29577951308232     # 180.0 / pi
DEG_TO_RAD = 0.017453292519943295  # pi / 180.0


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
        axis = axis.lower()
        if axis not in "xyz":
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


def mirror_transform(source_obj: str,
                     target_obj: str,
                     mirror_axis: str = "x",):
    """flip source object's world space matrix  as target object's world space matrix

    Args:
        sour_obj (str): source transform object
        target_obj (str): target transform object
        mirror_axis (str, optional): mirror axis. Defaults to "x".
    """
    sour_world_matrix = get_worldMatrix(source_obj)
    sour_parent_matrix = get_parentMatrix(source_obj)
    sour_world_matrix_flip = flip_matrix(sour_world_matrix, mirror_axis)
    sour_parent_matrix_flip = flip_matrix(sour_parent_matrix, mirror_axis)
    target_parent_matrix = get_parentMatrix(target_obj)
    flip_offset_matrix = get_offsetMatrix(sour_parent_matrix_flip, target_parent_matrix)
    set_worldMatrix(target_obj, flip_offset_matrix * sour_world_matrix_flip)


def flip_matrix(world_matrix: om.MMatrix,
                mirror_axis: str = "x") -> om.MMatrix:
    """flip matrix by mirror matrix

    Args:
        world_matrix (om.MMatrix): input world matrix
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix
    """
    mirror_matrix = world_matrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offsetMatrix(child_world_matrix: om.MMatrix,
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


def get_relativesMatrix(matrix: om.MMatrix,
                        referenceMatrix: om.MMatrix) -> om.MMatrix:
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
    """ convert world space matrix to local space matrix and as object's local space matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input world space matrix
    """
    mSel = om.MSelectionList()
    mSel.add(obj)
    local_matrix = matrix * mSel.getDagPath(0).exclusiveMatrixInverse()
    if cmds.objExists(f"{obj}.jointOrient"):
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix: om.MMatrix, rotateOrder: int = 0) -> list:
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
    euler_radians = om.MEulerRotation(*[DEG_TO_RAD * angle for angle in trs[3:6]], rotateOrder)
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


def create_fbfByMatrix(matrix: om.MMatrix = om.MMatrix(), **kwargs) -> str:
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
        cmds.setAttr(f"{fbf_node}.{attr_name}", num)
    return fbf_node


class decomMatrix(CreatorBase):
    isDagAsset: bool = False

    def _post_init(self, *args, **kwargs):
        self.translate = kwargs.get("translate", True) and kwargs.get("t", True)
        self.rotate = kwargs.get("rotate", True) and kwargs.get("r", True)
        self.scale = kwargs.get("scale", True) and kwargs.get("s", True)
        self.shear = kwargs.get("shear", True) and kwargs.get("sh", True)
        self.isForce = kwargs.get("force", True) and kwargs.get("f", True)

    def create(self):
        self.hasJointOrient = cmds.objExists(f"{self.name}.jointOrient")

        node_decom = CreateNode("decomposeMatrix", name=self.createName("decomposeMatrix"))
        node_mult = CreateNode("multMatrix", name=self.createName("getLocalMultMatrix"))
        node_matrixInverse = CreateNode("inverseMatrix", name=self.createName("inverseRelativesMatrix"))

        self.publishAttr(data={"inputMatrix": f"{node_mult}.matrixIn[0]",
                               "inputRotateOrder": f"{node_decom}.inputRotateOrder",
                               "inputRelativeSpaceMatrix": f"{node_matrixInverse}.inputMatrix",
                               "outputTranslate": f"{node_decom}.outputTranslate",
                               "outputRotate": f"{node_decom}.outputRotate",
                               "outputScale": f"{node_decom}.outputScale",
                               "outputShear": f"{node_decom}.outputShear"})

        # Internal connects
        cmds.connectAttr(f"{node_matrixInverse}.outputMatrix", f"{node_mult}.matrixIn[1]")
        cmds.connectAttr(f"{node_mult}.matrixSum", f"{node_decom}.inputMatrix")
        if self.hasJointOrient:
            node_euler_to_quat = CreateNode("eulerToQuat", name=self.createName("eulerToQuat"))
            node_invert_quat = CreateNode("quatInvert", name=self.createName("invertQuat"))
            node_prod_quat = CreateNode("quatProd", name=self.createName("prodQuat"))
            node_quat_to_euler = CreateNode("quatToEuler", name=self.createName("quatToEuler"))

            cmds.connectAttr(f"{node_decom}.inputRotateOrder", f"{node_euler_to_quat}.inputRotateOrder")
            cmds.connectAttr(f"{node_decom}.inputRotateOrder", f"{node_quat_to_euler}.inputRotateOrder")
            cmds.connectAttr(f"{node_decom}.outputQuat", f"{node_prod_quat}.input1Quat")
            cmds.connectAttr(f"{node_euler_to_quat}.outputQuat", f"{node_invert_quat}.inputQuat")
            cmds.connectAttr(f"{node_invert_quat}.outputQuat", f"{node_prod_quat}.input2Quat")
            cmds.connectAttr(f"{node_prod_quat}.outputQuat", f"{node_quat_to_euler}.inputQuat")

            self.publishAttr(data={"inputJointOrient": f"{node_euler_to_quat}.inputRotate",
                                   "outputRotate": f"{node_quat_to_euler}.outputRotate"})

        # External connects
        if cmds.objExists(self.name):
            if self.hasJointOrient:
                cmds.connectAttr(f"{self.name}.jointOrient", self.inputJointOrient)  # in jointOrient
            cmds.connectAttr(f"{self.name}.parentMatrix[0]", self.inputRelativeSpaceMatrix)  # input relatives space matrix
            cmds.connectAttr(f"{self.name}.rotateOrder", self.inputRotateOrder)  # in rotateOrder
            if self.translate:
                cmds.connectAttr(self.outputTranslate, f"{self.name}.translate", f=self.isForce)  # out translate
            if self.scale:
                cmds.connectAttr(self.outputScale, f"{self.name}.scale", f=self.isForce)  # out scale
            if self.shear:
                cmds.connectAttr(self.outputShear, f"{self.name}.shear", f=self.isForce)  # out shear
            if self.rotate:
                cmds.connectAttr(self.outputRotate, f"{self.name}.rotate", f=self.isForce)  # out rotate
                # cmds.connectAttr(f"{_assets}.outputQuat", f"{name}.rotateQuaternion")  # out rotate


class relativesMatrix(CreatorBase):
    isDagAsset: bool = False

    def create(self):
        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))
        node_inverseMatrix = CreateNode("inverseMatrix", name=self.createName("inverseMatrix"))
        cmds.connectAttr(f"{node_inverseMatrix}.outputMatrix", f"{node_multMatrix}.matrixIn[1]")
        self.publishAttr(data={"inputMatrix": f"{node_multMatrix}.matrixIn[0]",
                               "inputRelativeMatrix": f"{node_inverseMatrix}.inputMatrix",
                               "outputMatrix": f"{node_multMatrix}.matrixSum"})


class matrixConstraint(CreatorBase):
    isDagAsset: bool = False

    def _post_init(self, *args, **kwargs):
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

    def create(self):
        self.hasJointOrient = cmds.objExists(f"{self.target}.jointOrient")

        offset_matrix = get_offsetMatrix(child_world_matrix=get_worldMatrix(obj=self.target),
                                         parent_world_matrix=get_worldMatrix(obj=self.controller))

        node_multMatrix = CreateNode("multMatrix", name=self.createName("multMatrix"))

        node_decom = decomMatrix(name=self.name,
                                 translate=self.translate,
                                 rotate=self.rotate,
                                 scale=self.scale,
                                 shear=self.shear)

        self.publishAttr(data={"inputOffsetMatrix": f"{node_multMatrix}.matrixIn[0]",
                               "inputControllerMatrix": f"{node_multMatrix}.matrixIn[1]",
                               "inputRotateOrder": node_decom.inputRotateOrder,
                               "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                               "outputTranslate": node_decom.outputTranslate,
                               "outputRotate": node_decom.outputRotate,
                               "outputScale": node_decom.outputScale,
                               "outputShear": node_decom.outputShear})
        if self.hasJointOrient:
            self.publishAttr(data={"inputTargetJointOrient": node_decom.inputJointOrient})

        # Internal connects
        cmds.connectAttr(f"{node_multMatrix}.matrixSum", node_decom.inputMatrix)
        # External connects
        if self.keepOffset:
            cmds.setAttr(f"{node_multMatrix}.matrixIn[0]", offset_matrix, type="matrix")
        cmds.connectAttr(f"{self.controller}.worldMatrix[0]", f"{node_multMatrix}.matrixIn[1]")


class parentSpaceConstraint(CreatorBase):
    isDagAsset: bool = False
    attrName = "parentSpace"

    def _post_init(self, *args, **kwargs):

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
        if cmds.objExists(f"{self.target}.{self.attrName}"):
            if self.isForce:
                cmds.deleteAttr(f"{self.target}.{self.attrName}")
            else:
                self.isEdit = True

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
        cmds.connectAttr(f"{node_choseControllerMatrix}.controllerMatrix[0]", f"{node_choseControllerMatrix}.input[0]")
        cmds.connectAttr(f"{node_choseOffsetMatrix}.offsetMatrix[0]", f"{node_choseOffsetMatrix}.input[0]")

        # cal world matrix
        node_calWorldMatrix = CreateNode("multMatrix", name=self.createName("parentMultMatrix"))
        cmds.connectAttr(f"{node_choseOffsetMatrix}.output", f"{node_calWorldMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{node_choseControllerMatrix}.output", f"{node_calWorldMatrix}.matrixIn[1]")
        # chose to decomposeMatrix
        node_decom = decomMatrix(name=self.name,
                                 translate=self.translate,
                                 rotate=self.rotate,
                                 scale=self.scale,
                                 shear=self.shear)
        cmds.connectAttr(f"{node_calWorldMatrix}.matrixSum", node_decom.inputMatrix)
        # add parentspace switch attr
        cmds.addAttr(node_choseControllerMatrix, ln=self.attrName, at="enum", en="Parent", k=1)

        self.publishAttr(data={"inputRotateOrder": node_decom.inputRotateOrder,
                               "inputRelativeSpaceMatrix": node_decom.inputRelativeSpaceMatrix,
                               "outputTranslate": node_decom.outputTranslate,
                               "outputRotate": node_decom.outputRotate,
                               "outputScale": node_decom.outputScale,
                               "outputShear": node_decom.outputShear,
                               "parentspace": f"{node_choseControllerMatrix}.{self.attrName}",
                               "controllerMatrix": f"{node_choseControllerMatrix}.controllerMatrix",
                               "offsetMatrix": f"{node_choseOffsetMatrix}.offsetMatrix"})

        cmds.connectAttr(self.parentspace, f"{node_choseControllerMatrix}.selector")
        cmds.connectAttr(f"{node_choseControllerMatrix}.selector", f"{node_choseOffsetMatrix}.selector")

        # parent matrix * base local matrix
        cmds.connectAttr(f"{self.target}.parentMatrix[0]", f"{self.controllerMatrix}[0]")
        cmds.setAttr(f"{self.offsetMatrix}[0]", localMatrix, type="matrix")

        # add parentspace attr to obj
        if cmds.objExists(f"{self.target}.{self.attrName}"):
            cmds.deleteAttr(f"{self.target}.{self.attrName}")
        cmds.addAttr(self.target, ln=self.attrName, k=1, pxy=self.parentspace)
        # add info
        cmds.addAttr(self.target, ln="parentSpaceChoice", at="message")
        cmds.addAttr(node_choseControllerMatrix, ln="parentSpaceTarget", at="message")
        cmds.connectAttr(f"{node_choseControllerMatrix}.parentSpaceTarget", f"{self.target}.parentSpaceChoice")

    def addParentSpaceController(self,
                                 controller: str,
                                 niceName: str):

        # get index
        enum_str = cmds.addAttr(f"{self.target}.{self.attrName}", q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(niceName)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # update parentspace enum
        cmds.addAttr(f"{self.target}.{self.attrName}", e=1, en=enum_str)
        cmds.addAttr(self.parentspace, e=1, en=enum_str)

        # offset matrix to chose
        offset_matrix = get_offsetMatrix(get_worldMatrix(self.target),
                                         get_worldMatrix(controller))
        cmds.setAttr(f"{self.offsetMatrix}[{parent_indices}]", offset_matrix, type="matrix")
        # controller matrix to chose
        cmds.connectAttr(f"{controller}.worldMatrix[0]", f"{self.controllerMatrix}[{parent_indices}]")

        # update chose input data
        controller_chose = cmds.listConnections(f"{self.controllerMatrix}[0]", p=0, d=1, s=0)[0]
        offset_chose = cmds.listConnections(f"{self.offsetMatrix}[0]", p=0, d=1, s=0)[0]
        cmds.connectAttr(f"{self.controllerMatrix}[{parent_indices}]", f"{controller_chose}.input[{parent_indices}]")
        cmds.connectAttr(f"{self.offsetMatrix}[{parent_indices}]", f"{offset_chose}.input[{parent_indices}]")


class offsetFK(CreatorBase):
    def _post_init(self, *args, **kwargs):
        self.controllerList = kwargs.get("controllerList") or kwargs.get("cl") or []
        self.offsetList = kwargs.get("offsetList") or kwargs.get("ol") or []
        if not self.controllerList:
            self.controllerList = args[0] if args else []
        if not self.offsetList:
            self.offsetList = args[1] if args else []
        if not self.controllerList or not self.offsetList:
            raise RuntimeError("Input error!")

    def create(self):
        for i, control in enumerate(self.controllerList[:-1]):
            offset = self.offsetList[i]
            next_offset = self.offsetList[i + 1]
            next_control = self.controllerList[i + 1]

            node_multMatrix = CreateNode("multMatrix", name=f"{next_control}_multMatrix_{self.thisType}1")
            node_decom = decomMatrix(name=next_offset)
            # get offset matrix from 'offset_obj' with 'next offset_obj'
            cmds.connectAttr(f"{next_offset}.parentMatrix[0]",
                             f"{node_multMatrix}.matrixIn[0]")
            cmds.connectAttr(f"{offset}.parentInverseMatrix[0]",
                             f"{node_multMatrix}.matrixIn[1]")
            # controller constraint it
            cmds.connectAttr(f"{control}.worldMatrix[0]",
                             f"{node_multMatrix}.matrixIn[2]")
            # matrix to trs
            cmds.connectAttr(f"{node_multMatrix}.matrixSum",
                             f"{node_decom}.inputMatrix")


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
    msg = "Reset transform value."
    if userDefined:
        msg = "Reset value (all)."
    showMessage(msg)
