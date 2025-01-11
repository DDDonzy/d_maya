import maya.cmds as cmds
import maya.api.OpenMaya as om
from utils.generateUniqueName import generateUniqueName
from utils.createAssets import createAssets, assetBindAttr, get_bindAttrs
from utils.showMessage import showMessage

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
    fbf_node = cmds.createNode("fourByFourMatrix", **kwargs)
    for iter_idx, num in enumerate(matrix):
        attr_name = matrix_attrs[iter_idx]
        cmds.setAttr(f"{fbf_node}.{attr_name}", num)
    return fbf_node


def create_decomposeMatrix(name: str, translate=True, rotate=True, scale=True, shear=True):
    """ create decomposeMatrix for input object

    Args:
        name (str): _description_
        translate (bool, optional): _description_. Defaults to True.
        rotate (bool, optional): _description_. Defaults to True.
        scale (bool, optional): _description_. Defaults to True.
        shear (bool, optional): _description_. Defaults to True.

    PublishAttr:
        inputMatrix: -
        inputRotateOrder: -
        inputRelativeSpaceMatrix: -
        outputTranslate: -
        outputRotate: -
        outputScale: -
        outputShear: -
    """
    hasJointOrient = cmds.objExists(f"{name}.jointOrient")

    node_decom = cmds.createNode("decomposeMatrix", name=f"{name}_decomposeMatrix")
    node_mult = cmds.createNode("multMatrix", name=f"{name}_getLocalMatrix_multMatrix")
    node_matrixInverse = cmds.createNode("inverseMatrix", name=f"{name}_inverseRelativesSpaceMatrix_multMatrix")
    _assets_nodeList = [node_decom, node_mult, node_matrixInverse]
    _bindAttr = {"inputMatrix": f"{node_mult}.matrixIn[0]",
                 "inputRotateOrder": f"{node_decom}.inputRotateOrder",
                 "inputRelativeSpaceMatrix": f"{node_matrixInverse}.inputMatrix",
                 "outputTranslate": f"{node_decom}.outputTranslate",
                 "outputRotate": f"{node_decom}.outputRotate",
                 # "outputQuat": f"{node_decom}.outputQuat",
                 "outputScale": f"{node_decom}.outputScale",
                 "outputShear": f"{node_decom}.outputShear"}
    # Internal connects
    cmds.connectAttr(f"{node_matrixInverse}.outputMatrix", f"{node_mult}.matrixIn[1]")
    cmds.connectAttr(f"{node_mult}.matrixSum", f"{node_decom}.inputMatrix")
    if hasJointOrient:
        node_euler_to_quat = cmds.createNode("eulerToQuat", name=f"{name}_eulerToQuat")
        node_invert_quat = cmds.createNode("quatInvert", name=f"{name}_invertQuat")
        node_prod_quat = cmds.createNode("quatProd", name=f"{name}_prodQuat")
        node_quat_to_euler = cmds.createNode("quatToEuler", name=f"{name}_quatToEuler")

        cmds.connectAttr(f"{node_decom}.inputRotateOrder", f"{node_euler_to_quat}.inputRotateOrder")
        cmds.connectAttr(f"{node_decom}.inputRotateOrder", f"{node_quat_to_euler}.inputRotateOrder")
        cmds.connectAttr(f"{node_decom}.outputQuat", f"{node_prod_quat}.input1Quat")
        cmds.connectAttr(f"{node_euler_to_quat}.outputQuat", f"{node_invert_quat}.inputQuat")
        cmds.connectAttr(f"{node_invert_quat}.outputQuat", f"{node_prod_quat}.input2Quat")
        cmds.connectAttr(f"{node_prod_quat}.outputQuat", f"{node_quat_to_euler}.inputQuat")
        _assets_nodeList.extend([node_euler_to_quat,
                                 node_invert_quat,
                                 node_prod_quat,
                                 node_quat_to_euler])
        _bindAttr.update({"inputJointOrient": f"{node_euler_to_quat}.inputRotate",
                          # "outputQuat": f"{node_prod_quat}.outputQuat"
                          "outputRotate": f"{node_quat_to_euler}.outputRotate"})
    # assets
    _assets = createAssets(name=f"{name}_decomMatrix", assetsType="DecomposeMatrix", addNode=_assets_nodeList)
    assetBindAttr(_assets, _bindAttr)

    # External connects
    if cmds.objExists(name):
        if cmds.objExists(f"{name}.jointOrient"):
            cmds.connectAttr(f"{name}.jointOrient", f"{_assets}.inputJointOrient")  # in jointOrient
        cmds.connectAttr(f"{name}.parentMatrix[0]", f"{_assets}.inputRelativeSpaceMatrix")  # input relatives space matrix
        cmds.connectAttr(f"{name}.rotateOrder", f"{_assets}.inputRotateOrder")  # in rotateOrder
        if translate:
            cmds.connectAttr(f"{_assets}.outputTranslate", f"{name}.translate")  # out translate
        if scale:
            cmds.connectAttr(f"{_assets}.outputScale", f"{name}.scale")  # out scale
        if shear:
            cmds.connectAttr(f"{_assets}.outputShear", f"{name}.shear")  # out shear
        if rotate:
            cmds.connectAttr(f"{_assets}.outputRotate", f"{name}.rotate")  # out rotate
            # cmds.connectAttr(f"{_assets}.outputQuat", f"{name}.rotateQuaternion")  # out rotate
    return _assets


def create_relativesMatrix(name: str = ""):
    node_multMatrix = cmds.createNode("multMatrix", name=f"{name}_getRelativesMatrix_multMatrix")
    node_inverseMatrix = cmds.createNode("inverseMatrix", name=f"{name}_getRelativesMatrix_inverseMatrix")
    cmds.connectAttr(f"{node_inverseMatrix}.outputMatrix", f"{node_multMatrix}.matrixIn[1]")
    _assets_nodeList = [node_multMatrix, node_inverseMatrix]
    _bindAttr = {"inputMatrix": f"{node_multMatrix}.matrixIn[0]",
                 "inputRelativeMatrix": f"{node_inverseMatrix}.inputMatrix",
                 "outputMatrix": f"{node_multMatrix}.matrixSum"}
    _assets = createAssets(f"{name}_getRelativesMatrix", addNode=_assets_nodeList)
    assetBindAttr(_assets, _bindAttr)


def matrixConstraint(*args,
                     translate: bool = True,
                     rotate: bool = True,
                     scale: bool = True,
                     shear: bool = True,
                     **kwargs) -> str:
    """
    Create a matrix-based constraint node

    Args:
            translate (bool): Enable translation constraint
            rotate (bool): Enable rotation constraint
            scale (bool): Enable scale constraint
            shear (bool): Enable shear constraint
        *arg: Variable length arguments.
            No args: Use current selection, first as source, rest as targets.
            Single arg: Specify source object.
            Multiple args: First as source, rest as targets.
        **kwargs: Keyword arguments.
            mo/maintainOffset (bool): Keep offset transforms, default True.
            q/query (bool): Query mode, default False.
            s/source (bool): Query source object, default True.
            t/target (bool): Query target objects, default False.

    Returns:
        str: Name of constraint node or query result dictionary
    """

    _info_name = "matrixConstraintInfo"

    def _create_matrixConstraint(source_obj: str,
                                 target_object: str,
                                 keep_offset: bool = True):
        """
        Create matrix constraint between source and target

        Args:
            source_obj: Driver object
            target_object: Driven object
            keep_offset: Maintain offset transforms
        """
        hasJointOrient = cmds.objExists(f"{target_object}.jointOrient")
        offset_matrix = get_offsetMatrix(get_worldMatrix(target_object), get_worldMatrix(source_obj))
        node_multMatrix = cmds.createNode("multMatrix", name=f"{target_object}_MM_matrixConstraint")
        node_decom = create_decomposeMatrix(name=target_object, translate=translate, rotate=rotate, scale=scale, shear=shear)
        _add_nodeList = [node_multMatrix, node_decom]
        _bindAttr = {"inputOffsetMatrix": f"{node_multMatrix}.matrixIn[0]",
                     "inputControllerMatrix": f"{node_multMatrix}.matrixIn[1]",
                     "inputRotateOrder": f"{node_decom}.inputRotateOrder",
                     "inputRelativeSpaceMatrix": f"{node_decom}.inputRelativeSpaceMatrix",
                     "outputTranslate": f"{node_decom}.outputTranslate",
                     "outputRotate": f"{node_decom}.outputRotate",
                     # "outputQuat": f"{node_decom}.outputQuat",
                     "outputScale": f"{node_decom}.outputScale",
                     "outputShear": f"{node_decom}.outputShear"}
        if hasJointOrient:
            _bindAttr.update({"inputTargetJointOrient": f"{node_decom}.inputJointOrient"})
        _assets = generateUniqueName(f"{target_object}_matrixConstraint")
        _assets = createAssets(name=_assets, assetsType="MatrixConstraint", addNode=_add_nodeList)
        assetBindAttr(_assets, _bindAttr)
        # Internal connects
        cmds.connectAttr(f"{node_multMatrix}.matrixSum", f"{node_decom}.inputMatrix")
        # External connects
        if keep_offset:
            cmds.setAttr(f"{_assets}.inputOffsetMatrix", offset_matrix, type="matrix")
        cmds.connectAttr(f"{source_obj}.worldMatrix[0]", f"{_assets}.inputControllerMatrix")
        # cmds.connectAttr(f"{target_object}.parentMatrix[0]", f"{_assets}.inputTargetRelativeSpaceMatrix")

        # add info
        if cmds.objExists(f"{target_object}.{_info_name}"):
            cmds.deleteAttr(f"{target_object}.{_info_name}")

        # matrix constraint attr
        cmds.addAttr(_assets, ln=_info_name, at="message")
        cmds.addAttr(target_object, ln=_info_name, at="message", pxy=f"{_assets}.{_info_name}")
        return _assets

    def _query_matrixConstraint(obj: str):
        """
        Query constraint relationships

        Args:
            object: object to query
        Returns:
            dict: Constraint relationship dictionary
        """
        dict_info = {}
        _assets = None
        target_obj = None
        if not cmds.objExists(f"{obj}.{_info_name}"):
            return dict_info
        if cmds.objectType(obj) == "container":
            _assets = obj
            target_obj_list = cmds.listConnections(f"{_assets}.{_info_name}", s=0, d=1)
            if target_obj_list:
                target_obj = target_obj_list[0]
        else:
            target_obj = obj
            _assets_list = cmds.listConnections(f"{target_obj}.{_info_name}", s=1, d=0)
            if _assets_list:
                _assets = _assets_list[0]
        controller_obj = cmds.listConnections(f"{_assets}.inputControllerMatrix", s=1, d=0)[0]
        dict_info.update({controller_obj: target_obj})
        return dict_info

    maintainOffset = kwargs.get("mo", True) and kwargs.get("maintainOffset", True)
    query = kwargs.get("q", False) or kwargs.get("query", False)
    q_source = kwargs.get("s", True)
    if not q_source:
        q_source = kwargs.get("source", False)
    q_target = kwargs.get("t", True)
    if not q_target:
        q_target = kwargs.get("target", False)

    # do functions
    if query:
        if args:
            obj = args[0]
        else:
            obj = cmds.ls(sl=1)
            obj = obj[0]
        return _query_matrixConstraint(obj)
    if not query:
        if not args:
            args = cmds.ls(sl=1)
        source_obj = args[0]
        target_object = args[1:]
        _assets_list = []
        for target in target_object:
            _assets = _create_matrixConstraint(source_obj, target, maintainOffset)
            _assets_list.append(_assets)
        return _assets_list


def parentspaceConstraint(*args,
                          translate: bool = True,
                          rotate: bool = True,
                          scale: bool = True,
                          shear: bool = True,
                          ** kwargs):
    """
    Create parent space constraint networks for target object with multiple control objects.

    Usage:
        1. Select multiple controls + one target (last selected)
        2. Or provide objects as arguments (last arg = target)

    Args:
            translate (bool): Enable translation constraint
            rotate (bool): Enable rotation constraint
            scale (bool): Enable scale constraint
            shear (bool): Enable shear constraint
        *arg: Variable length argument list
            If empty: Uses selected objects (last = target)
            If provided: Last arg = target, others = controls
        **kwargs: Optional arguments
            niceName (str): Custom name for space switch enum
    """

    parentspace_attrName = "parentSpace"
    _info_name = "parentspaceConstraint"

    def _pre_parentspace(target_obj):
        """
        Setup initial constraint network and container structure

        Args:
            target_obj (str): Target object to setup constraint for

        Returns:
            str: Created parentspace assets container name
        """
        localMatrix = get_localMatrix(target_obj)
        # connect to chose
        node_choseControllerMatrix = cmds.createNode("choice", name=f"{target_obj}_controller_choice")
        node_choseOffsetMatrix = cmds.createNode("choice", name=f"{target_obj}_offset_choice")
        # cal world matrix
        node_calWorldMatrix = cmds.createNode("multMatrix", name=f"{target_obj}_parentSpace_multMatrix")
        cmds.connectAttr(f"{node_choseOffsetMatrix}.output", f"{node_calWorldMatrix}.matrixIn[0]")
        cmds.connectAttr(f"{node_choseControllerMatrix}.output", f"{node_calWorldMatrix}.matrixIn[1]")
        # chose to decomposeMatrix
        node_decom = create_decomposeMatrix(f"{target_obj}", translate=translate, rotate=rotate, scale=scale, shear=shear)
        cmds.connectAttr(f"{node_calWorldMatrix}.matrixSum", f"{node_decom}.inputMatrix")

        _add_nodeList = [node_decom, node_choseOffsetMatrix, node_choseControllerMatrix, node_calWorldMatrix]
        _bindAttr = {"inputRotateOrder": f"{node_decom}.inputRotateOrder",
                     "inputRelativeSpaceMatrix": f"{node_decom}.inputRelativeSpaceMatrix",
                     "outputTranslate": f"{node_decom}.outputTranslate",
                     "outputRotate": f"{node_decom}.outputRotate",
                     "outputScale": f"{node_decom}.outputScale",
                     "outputShear": f"{node_decom}.outputShear", }

        # assets
        _assets = createAssets(name=generateUniqueName(f"{target_obj}_parentspace"),
                               assetsType="ParentspaceAssets",
                               addNode=_add_nodeList)
        assetBindAttr(_assets, _bindAttr)

        # add parentspace switch attr
        cmds.addAttr(_assets, ln=parentspace_attrName, at="enum", en="Parent", k=1)
        cmds.connectAttr(f"{_assets}.{parentspace_attrName}", f"{node_choseControllerMatrix}.selector")
        cmds.connectAttr(f"{_assets}.{parentspace_attrName}", f"{node_choseOffsetMatrix}.selector")
        # add matrix
        cmds.addAttr(_assets, ln="controllerMatrix", at="matrix", m=1)
        cmds.addAttr(_assets, ln="offsetMatrix", at="matrix", m=1)
        cmds.connectAttr(f"{_assets}.controllerMatrix[0]", f"{node_choseControllerMatrix}.input[0]")
        cmds.connectAttr(f"{_assets}.offsetMatrix[0]", f"{node_choseOffsetMatrix}.input[0]")
        # parent matrix * base local matrix
        cmds.setAttr(f"{_assets}.offsetMatrix[0]", localMatrix, type="matrix")
        cmds.connectAttr(f"{target_obj}.parentMatrix[0]", f"{_assets}.controllerMatrix[0]")

        # add parentspace attr to obj
        if cmds.objExists(f"{target_obj}.{parentspace_attrName}"):
            cmds.deleteAttr(f"{target_obj}.{parentspace_attrName}")
        cmds.addAttr(target_obj, ln=parentspace_attrName, k=1, pxy=f"{_assets}.{parentspace_attrName}")

        # add message info to obj
        cmds.addAttr(_assets, ln=_info_name, at="message")
        if cmds.objExists(f"{target_obj}.{_info_name}"):
            cmds.deleteAttr(f"{target_obj}.{_info_name}")
        cmds.addAttr(target_obj, ln=_info_name, at="message", pxy=f"{_assets}.{_info_name}")

        return _assets

    def _add_parentspace(controllerObj: str,
                         targetObj: str,
                         niceName: str = None):
        """
        Add a new parent space option to the target object

        Args:
            control_obj (str): Control object to add as parent space
            target_obj (str): Target object to be constrained
            niceName (str, optional): Custom name for space enum
        """

        # get parentspace assets
        if not cmds.objExists(f"{targetObj}.{_info_name}"):
            _assets = _pre_parentspace(targetObj)

        _assets = cmds.listConnections(f"{targetObj}.{_info_name}", s=1, d=0)[0]
        if not _assets:
            raise RuntimeError("Can not find parentspace constraint node!")

        # nice name enum
        if not niceName:
            niceName = controllerObj
        enum_str = cmds.addAttr(f"{targetObj}.{parentspace_attrName}", q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(niceName)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # update parentspace enum
        cmds.addAttr(f"{targetObj}.{parentspace_attrName}", e=1, en=enum_str)
        cmds.addAttr(f"{_assets}.{parentspace_attrName}", e=1, en=enum_str)

        # offset matrix to chose
        offset_matrix = get_offsetMatrix(get_worldMatrix(targetObj), get_worldMatrix(controllerObj))
        cmds.setAttr(f"{_assets}.offsetMatrix[{parent_indices}]", offset_matrix, type="matrix")
        # controller matrix to chose
        cmds.connectAttr(f"{controllerObj}.worldMatrix[0]", f"{_assets}.controllerMatrix[{parent_indices}]")
        # update chose input data
        controller_chose = cmds.listConnections(f"{_assets}.controllerMatrix[0]", p=0, d=1, s=0)[0]
        offset_chose = cmds.listConnections(f"{_assets}.offsetMatrix[0]", p=0, d=1, s=0)[0]
        cmds.connectAttr(f"{_assets}.controllerMatrix[{parent_indices}]", f"{controller_chose}.input[{parent_indices}]")
        cmds.connectAttr(f"{_assets}.offsetMatrix[{parent_indices}]", f"{offset_chose}.input[{parent_indices}]")

    if len(args) == 0:
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            om.MGlobal.displayError("Please select at least two objects.")
            return
        control_obj_list = cmds.ls(sl=1)[:-1]
        target_obj = cmds.ls(sl=1)[-1]
    else:
        control_obj_list = []
        control_obj_list.extend(args[:-1])
        target_obj = args[-1]

    for control_obj in control_obj_list:
        _add_parentspace(control_obj, target_obj, **kwargs)


def create_OffsetFK(control_list: list, offset_list: list):
    """
    Create an offset system for FK chains
    For example, the hierarchy at the top of each FK chain is constrained,
    causing us to lose control over the levels below the FK chain.
    This function can achieve this by preserving control over the levels below the FK chain,
    even when they are constrained.

    Args:
        control_list (list): Control the list of objects, paying attention to the order, from top to bottom.
        offset_list (list): Control's offset transform objects, paying attention to the order, from top to bottom.
    Example:
        hierarchy ------GRP------Offset------CTL

        control_list = ['Test_CTL', 'Test1_CTL', 'Test2_CTL', 'Test3_CTL']

        offset_list = ['Test_Offset', 'Test1_Offset', 'Test2_Offset', 'Test3_Offset']

        offset_fk(control_list, offset_list)

    """
    for i, control in enumerate(control_list[:-1]):
        offset = offset_list[i]
        next_offset = offset_list[i + 1]
        next_control = control_list[i + 1]

        node_multMatrix = cmds.createNode("multMatrix", name=f"{next_control}_multMatrix_offsetFK")
        node_decom = create_decomposeMatrix(name=next_offset)
        _add_nodeList = [node_multMatrix, node_decom]

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
        _assets = generateUniqueName(f"{next_control}_offsetFK")
        _assets = createAssets(name=_assets, assetsType="OffsetFK", addNode=_add_nodeList)


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
