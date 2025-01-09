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


def create_decomposeMatrix(name: str, translate=True, rotate=True, scale=True, shear=True, quat=True):
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


def matrixConstraint(*args,
                     **kwargs) -> str:
    """
    Create a matrix-based constraint node

    Args:
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
        node_decom = create_decomposeMatrix(name=target_object)
        _add_nodeList = [node_multMatrix, node_decom]
        _bindAttr = {"inputOffsetMatrix": f"{node_multMatrix}.matrixIn[0]",
                     "inputControllerMatrix": f"{node_multMatrix}.matrixIn[1]",
                     "inputTargetRotateOrder": f"{node_decom}.inputRotateOrder",
                     "inputTargetRelativeSpaceMatrix": f"{node_decom}.inputRelativeSpaceMatrix",
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
        # target attr
        if cmds.objExists(f"{target_object}.{_info_name}"):
            sour_connect_attr = cmds.listConnections(f"{target_object}.{_info_name}", s=1, d=0, p=1)
            if sour_connect_attr:
                for attr in sour_connect_attr:
                    cmds.disconnectAttr(attr, f"{target_object}.{_info_name}")
        else:
            cmds.addAttr(target_object, ln=_info_name, at="message")
        # source attr
        if not cmds.objExists(f"{source_obj}.{_info_name}"):
            cmds.addAttr(source_obj, ln=_info_name, at="message")
        # matrix constraint attr
        cmds.addAttr(_assets, ln=_info_name, at="message")
        # connect
        cmds.connectAttr(f"{source_obj}.{_info_name}",
                         f"{_assets}.{_info_name}")
        cmds.connectAttr(f"{_assets}.{_info_name}",
                         f"{target_object}.{_info_name}")
        return _assets

    def _query_matrixConstraint(obj: str,
                                source: bool,
                                target: bool):
        """
        Query constraint relationships

        Args:
            obj: Object to query
            source: Query source object
            target: Query target objects

        Returns:
            dict: Constraint relationship dictionary
        """
        dict_info = {}
        if not cmds.objExists(f"{obj}.{_info_name}"):
            return dict_info
        if source:
            _assets = cmds.listConnections(f"{obj}.{_info_name}", s=1, d=0)
            if _assets:
                _assets = _assets[0]
                source_obj = cmds.listConnections(f"{_assets}.{_info_name}", s=1, d=0)
                if source_obj:
                    source_obj = source_obj[0]
                    dict_info.update({source_obj: [obj]})
        if target:
            _assets_list = cmds.listConnections(f"{obj}.{_info_name}", s=0, d=1)
            if _assets_list:
                target_obj_list = []
                for _assets in _assets_list:
                    target_obj = cmds.listConnections(f"{_assets}.{_info_name}", s=0, d=1)
                    if target_obj:
                        target_obj_list.extend(target_obj)
                dict_info.update({obj: target_obj_list})
        return dict_info

    if len(args) == 0:
        sel = cmds.ls(sl=1)
        if len(sel) < 2:
            om.MGlobal.displayError("Please select at least two objects.")
            return
        source_obj = cmds.ls(sl=1)[0]
        target_object = cmds.ls(sl=1)[1:]
    elif len(args) == 1:
        source_obj = args[0]
    else:
        source_obj = args[0]
        target_object = []
        target_object.extend(args[1:])
    maintainOffset = kwargs.get("mo", True) and kwargs.get("maintainOffset", True)
    query = kwargs.get("q", False) or kwargs.get("query", False)
    q_source = kwargs.get("s", True)
    if not q_source:
        q_source = kwargs.get("source", False)
    q_target = kwargs.get("t", True)
    if not q_target:
        q_target = kwargs.get("target", False)

    if query:
        return _query_matrixConstraint(source_obj, q_source, q_target)
    else:
        for target in target_object:
            _assets = _create_matrixConstraint(source_obj, target, maintainOffset)
        return _assets


def parentspaceConstraint(*args,
                          **kwargs):
    """
    Create parent space constraint networks for target object with multiple control objects.

    Usage:
        1. Select multiple controls + one target (last selected)
        2. Or provide objects as arguments (last arg = target)

    Args:
        *arg: Variable length argument list
            If empty: Uses selected objects (last = target)
            If provided: Last arg = target, others = controls
        **kwargs: Optional arguments
            nice_name (str): Custom name for space switch enum
            translate (bool): Enable translation constraint
            rotate (bool): Enable rotation constraint
            scale (bool): Enable scale constraint
            shear (bool): Enable shear constraint
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

        # constraint logic
        # pro create node
        node_bw = cmds.createNode("blendMatrix", name=f"{target_obj}_spaceBW")
        #
        bode_chose = cmds.createNode("choice", name=f"{target_obj}_spaceChoice")
        node_getLocalMatrix = cmds.createNode("multMatrix", name=f"{target_obj}_getLocalMatrix")
        node_decMatrix = cmds.createNode("decomposeMatrix", name=f"{target_obj}_decomposeMatrix")
        node_parentMult = cmds.createNode("multMatrix", name=f"{target_obj}_parentMult")
        cmds.addAttr(node_bw, ln=parentspace_attrName, at="enum", en="Parent", k=0)
        bind_attr_dict = {parentspace_attrName: f"{node_bw}.{parentspace_attrName}",
                          "inputBlendTarget": f"{node_bw}.target"}
        add_node_list = [node_bw, node_getLocalMatrix, node_decMatrix, node_parentMult]
        # parent connect
        cmds.setAttr(f"{node_parentMult}.matrixIn[0]",
                     get_localMatrix(target_obj),
                     type="matrix")
        cmds.connectAttr(f"{target_obj}.parentMatrix[0]",
                         f"{node_parentMult}.matrixIn[1]")
        cmds.connectAttr(f"{node_parentMult}.matrixSum",
                         f"{node_bw}.inputMatrix")
        #
        cmds.connectAttr(f"{node_parentMult}.matrixSum",
                         f"{bode_chose}.input[0]")
        # blend world matrix to local matrix
        cmds.connectAttr(f"{node_bw}.outputMatrix",
                         f"{node_getLocalMatrix}.matrixIn[0]")
        #
        cmds.connectAttr(f"{bode_chose}.output",
                         f"{node_getLocalMatrix}.matrixIn[0]")

        cmds.connectAttr(f"{target_obj}.parentInverseMatrix[0]",
                         f"{node_getLocalMatrix}.matrixIn[1]")
        cmds.connectAttr(f"{node_getLocalMatrix}.matrixSum",
                         f"{node_decMatrix}.inputMatrix")
        # decomposeMatrix
        cmds.connectAttr(f"{target_obj}.rotateOrder", f"{node_decMatrix}.inputRotateOrder")  # in rotate order
        cmds.connectAttr(f"{node_decMatrix}.outputTranslate", f"{target_obj}.translate")  # out translate
        cmds.connectAttr(f"{node_decMatrix}.outputScale", f"{target_obj}.scale")  # out scale
        cmds.connectAttr(f"{node_decMatrix}.outputShear", f"{target_obj}.shear")  # out shear

        if cmds.objExists(f"{target_obj}.jointOrient"):
            inverse_orient_node = create_inverseOrient(name=f"{target_obj}_inverseJointOrient_matrixConstraint")
            add_node_list.append(inverse_orient_node)
            cmds.connectAttr(f"{target_obj}.jointOrient", f"{inverse_orient_node}.inputOrientRotate")  # in orient rotate
            cmds.connectAttr(f"{target_obj}.rotateOrder", f"{inverse_orient_node}.inputRotateOrder")  # in rotate order
            cmds.connectAttr(f"{node_decMatrix}.outputQuat", f"{inverse_orient_node}.inputRotateQuat")  # in rotate
            cmds.connectAttr(f"{inverse_orient_node}.outputRotate", f"{target_obj}.rotate", f=1)  # out rotate
            cmds.connectAttr(f"{inverse_orient_node}.outputQuat", f"{target_obj}.rotateQuaternion", f=1)  # out quat
        else:
            cmds.connectAttr(f"{node_decMatrix}.outputRotate", f"{target_obj}.rotate")  # out rotate
            cmds.connectAttr(f"{node_decMatrix}.outputQuat", f"{target_obj}.rotateQuaternion")  # out quat

        # assets
        _assets = generateUniqueName(f"{target_obj}_parentspace")
        _assets = createAssets(name=_assets, assetsType="ParentspaceAssets", addNode=add_node_list)
        assetBindAttr(_assets, bind_attr_dict)
        # add parentspace attr to obj
        if not cmds.objExists(f"{target_obj}.{parentspace_attrName}"):
            cmds.addAttr(target_obj, ln=parentspace_attrName, pxy=f"{_assets}.{parentspace_attrName}", k=1)
        else:
            cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en="Parent", k=1)
        # add message info to obj
        cmds.addAttr(_assets, ln=_info_name, at="message")
        if not cmds.objExists(f"{target_obj}.{_info_name}"):
            cmds.addAttr(target_obj, ln=_info_name, at="message")
        cmds.connectAttr(f"{_assets}.{_info_name}",
                         f"{target_obj}.{_info_name}")

        return _assets

    def _add_parentspace(control_obj: str,
                         target_obj: str,
                         nice_name: str = None,
                         translate=True,
                         rotate=True,
                         scale=True,
                         shear=True):
        """
        Add a new parent space option to the target object

        Args:
            control_obj (str): Control object to add as parent space
            target_obj (str): Target object to be constrained
            nice_name (str, optional): Custom name for space enum
            translate (bool): Enable translation
            rotate (bool): Enable rotation
            scale (bool): Enable scale
            shear (bool): Enable shear
        """

        # get parentspace assets
        if not cmds.objExists(f"{target_obj}.{_info_name}"):
            _assets = _pre_parentspace(target_obj)
        else:
            _assets = cmds.listConnections(f"{target_obj}.{_info_name}", s=1, d=0)[0]

        # get node blendMatrix
        node_bw_target_attr = cmds.ls(f"{_assets}.inputBlendTarget")[0]
        node_bw = cmds.ls(f"{_assets}.inputBlendTarget", o=1)[0]

        # nice name enum
        if not nice_name:
            nice_name = control_obj
        enum_str = cmds.addAttr(f"{node_bw}.{parentspace_attrName}", q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(nice_name)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # update parentspace enum
        cmds.addAttr(f"{node_bw}.{parentspace_attrName}", e=1, en=enum_str)
        cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en=enum_str)

        # control_obj constraint target_obj
        offset_matrix = get_offsetMatrix(get_worldMatrix(target_obj),
                                         get_worldMatrix(control_obj))
        node_multMatrix = cmds.createNode("multMatrix", name=f"{control_obj}_{target_obj}_multMatrix")
        cmds.setAttr(f"{node_multMatrix}.matrixIn[0]",
                     offset_matrix,
                     type="matrix")
        cmds.connectAttr(f"{control_obj}.worldMatrix[0]",
                         f"{node_multMatrix}.matrixIn[1]")

        # connect to blendMatrix
        cmds.connectAttr(f'{node_multMatrix}.matrixSum',
                         f"{node_bw_target_attr}[{parent_indices}].targetMatrix")

        # version switch
        if cmds.about(api=True) >= 20230000:
            blend_attr = ["translateWeight", "rotateWeight", "scaleWeight", "shearWeight"]
        else:
            blend_attr = ["useTranslate", "useRotate", "useScale", "useShear"]
        # publish trs attr
        status = [translate, rotate, scale, shear]
        for i, attr in enumerate(blend_attr):
            cmds.container(_assets, e=1, publishName=f'{attr}_{parent_indices}')
            cmds.container(_assets, e=1, bindAttr=[f"{node_bw_target_attr}[{parent_indices}].{attr}", f'{attr}_{parent_indices}'])
            cmds.setAttr(f"{node_bw_target_attr}[{parent_indices}].{attr}", status[i])

        # sdk
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{node_bw}.{parentspace_attrName}",
                               dv=parent_indices - 1, v=0)
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{node_bw}.{parentspace_attrName}",
                               dv=parent_indices, v=1)
        cmds.setDrivenKeyframe(f"{node_bw_target_attr}[{parent_indices}].weight",
                               cd=f"{node_bw}.{parentspace_attrName}",
                               dv=parent_indices + 1, v=0)
        node_sdk = cmds.listConnections(f"{node_bw_target_attr}[{parent_indices}].weight", s=1, d=0)
        cmds.container(_assets, e=1, addNode=[node_multMatrix]+node_sdk)
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


def create_fkOffset(control_list: list, offset_list: list):
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
        # cal local matrix
        cmds.connectAttr(f"{next_offset}.parentInverseMatrix[0]",
                         f"{node_multMatrix}.matrixIn[3]")
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
