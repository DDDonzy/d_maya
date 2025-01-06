import maya.cmds as cmds
import maya.api.OpenMaya as om
from py2.utils.generate_unique_name import generate_unique_name
from py2.utils.create_assets import create_assets, bind_attr


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

    def __init__(self, axis="x"):
        if axis not in ["x", "y", "z"]:
            raise ValueError("Invalid axis. Choose from 'x', 'y', or 'z'.")

    def __new__(cls, axis="x"):
        return getattr(MIRROR_MATRIX, axis)


class UNIT_CONVERT():
    mm = 10.0
    cm = 1.0
    m = 0.01

    def __init__(self, unit=cmds.currentUnit(q=1)):
        if unit not in ["mm", "cm", "m"]:
            raise ValueError("Invalid axis. Choose from 'mm', 'cm', or 'm'.")

    def __new__(cls, unit=cmds.currentUnit(q=1)):
        return getattr(UNIT_CONVERT, unit)


def mirror_transform(sour_obj,
                     target_obj,
                     mirror_axis="x"):
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


def flip_matrix(world_matrix,
                mirror_axis="x"):
    """flip matrix by mirror matrix

    Args:
        world_matrix (om.MMatrix): input world matrix
        mirror_axis (str, optional): mirror axis x y or z. Defaults to "x".

    Returns:
        om.MMatrix: flip matrix
    """
    mirror_matrix = world_matrix * MIRROR_MATRIX(mirror_axis)
    return mirror_matrix


def get_offset_matrix(child_world_matrix,
                      parent_world_matrix):
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
            cmds.setAttr("{}.jointOrient".format(obj), 0, 0, 0)
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
            cmds.setAttr("{}.jointOrient".format(obj), 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(local_matrix))


def matrix_to_trs(matrix, rotateOrder=0):
    """ convert matrix to maya's translate,rotate and scale

    Args:
        matrix (om.MMatrix): input matrix
        rotateOrder (int, optional): rotate order. Defaults to 0.

    Returns:
        list: [tx,ty.tz,rx,ry,rz,sx,sy,sz]
    """
    om_transformation = om.MTransformationMatrix(matrix)
    translate = om_transformation.translation(1) * UNIT_CONVERT()
    euler_radians = om_transformation.rotation()
    euler_radians.reorderIt(rotateOrder)
    euler_angle = [57.29577951308232*radians for radians in [euler_radians.x, euler_radians.y, euler_radians.z]]
    scale = om_transformation.scale(1)
    outputList = [translate[0], translate[1], translate[2],
                  euler_angle[0], euler_angle[1], euler_angle[2],
                  scale[0], scale[1], scale[2]]
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


def create_fbf_node(matrix=om.MMatrix(), **kwargs):
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
        cmds.setAttr("{}.{}".format(fbf_node, attr_name), num)
    return fbf_node


def create_inverse_orient_node(name):
    node_euler_to_quat = cmds.createNode("eulerToQuat", name="{}_eulerToQuat".format(name))
    node_invert_quat = cmds.createNode("quatInvert", name="{}_invertQuat".format(name))
    node_prod_quat = cmds.createNode("quatProd", name="{}_prodQuat".format(name))
    node_quat_to_euler = cmds.createNode("quatToEuler", name="{}_quatToEuler".format(name))

    cmds.connectAttr("{}.outputQuat".format(node_euler_to_quat),
                     "{}.inputQuat".format(node_invert_quat))
    cmds.connectAttr("{}.outputQuat".format(node_invert_quat),
                     "{}.input2Quat".format(node_prod_quat))
    cmds.connectAttr("{}.outputQuat".format(node_prod_quat),
                     "{}.inputQuat".format(node_quat_to_euler))
    cmds.connectAttr("{}.inputRotateOrder".format(node_euler_to_quat),
                     "{}.inputRotateOrder".format(node_quat_to_euler))
    # assets box
    _assets = create_assets(name, add_node=[node_euler_to_quat, node_invert_quat, node_prod_quat, node_quat_to_euler])
    bind_attr_dict = {"inputOrientRotate": "{}.inputRotate".format(node_euler_to_quat),
                      "inputRotateOrder": '{}.inputRotateOrder'.format(node_euler_to_quat),
                      "inputRotateQuat": "{}.input1Quat".format(node_prod_quat),
                      "outputRotate": "{}.outputRotate".format(node_quat_to_euler),
                      "outputQuat": "{}.outputQuat".format(node_prod_quat)}
    bind_attr(_assets, bind_attr_dict)
    return _assets


def matrixConstraint(*args, **kwargs):
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

    def _create_matrix_constraint(source_obj, target_object, keep_offset=True):
        """
        Create matrix constraint between source and target

        Args:
            source_obj: Driver object
            target_object: Driven object
            keep_offset: Maintain offset transforms
        """
        offset_matrix = get_offset_matrix(get_world_matrix(target_object), get_world_matrix(source_obj))
        node_multMatrix = cmds.createNode("multMatrix", name="{0}_MM_matrixConstraint".format(target_object))
        node_decomposeMatrix = cmds.createNode("decomposeMatrix", name="{0}_DM_matrixConstraint".format(target_object))
        bind_attr_dict = {"offsetMatrix": "{0}.matrixIn[0]".format(node_multMatrix)}
        add_node_list = [node_multMatrix, node_decomposeMatrix]
        if keep_offset:
            cmds.setAttr("{0}.matrixIn[0]".format(node_multMatrix), offset_matrix, type="matrix")
        cmds.connectAttr("{0}.worldMatrix[0]".format(source_obj),
                         "{0}.matrixIn[1]".format(node_multMatrix))
        cmds.connectAttr("{0}.parentInverseMatrix[0]".format(target_object),
                         "{0}.matrixIn[2]".format(node_multMatrix))
        cmds.connectAttr("{0}.rotateOrder".format(target_object),
                         "{0}.inputRotateOrder".format(node_decomposeMatrix))  # in rotate order
        cmds.connectAttr("{0}.matrixSum".format(node_multMatrix),
                         "{0}.inputMatrix".format(node_decomposeMatrix))  # in matrix
        cmds.connectAttr("{0}.outputTranslate".format(node_decomposeMatrix),
                         "{0}.translate".format(target_object), f=1)  # out translate
        cmds.connectAttr("{0}.outputScale".format(node_decomposeMatrix),
                         "{0}.scale".format(target_object), f=1)  # out scale
        cmds.connectAttr("{0}.outputShear".format(node_decomposeMatrix),
                         "{0}.shear".format(target_object), f=1)  # out shear
        if cmds.objExists("{0}.jointOrient".format(target_object)):
            inverse_orient_node = generate_unique_name("{0}_inverseJointOrient_matrixConstraint".format(target_object))
            inverse_orient_node = create_inverse_orient_node(name=inverse_orient_node)
            add_node_list.append(inverse_orient_node)
            cmds.connectAttr("{0}.jointOrient".format(target_object),
                             "{0}.inputOrientRotate".format(inverse_orient_node))  # in orient rotate
            cmds.connectAttr("{0}.rotateOrder".format(target_object),
                             "{0}.inputRotateOrder".format(inverse_orient_node))  # in rotate order
            cmds.connectAttr("{0}.outputQuat".format(node_decomposeMatrix),
                             "{0}.inputRotateQuat".format(inverse_orient_node))  # in rotate
            cmds.connectAttr("{0}.outputRotate".format(inverse_orient_node),
                             "{0}.rotate".format(target_object), f=1)  # out rotate
            cmds.connectAttr("{0}.outputQuat".format(inverse_orient_node),
                             "{0}.rotateQuaternion".format(target_object), f=1)  # out quat
        else:
            cmds.connectAttr("{0}.outputRotate".format(node_decomposeMatrix),
                             "{0}.rotate".format(target_object), f=1)  # out rotate
            cmds.connectAttr("{0}.outputQuat".format(node_decomposeMatrix),
                             "{0}.rotateQuaternion".format(target_object), f=1)  # out quat

        # assets box
        _assets = generate_unique_name("{0}_matrixConstraint".format(target_object))
        _assets = create_assets(name=_assets, parent_assets="MatrixConstraint",
                                add_node=add_node_list)
        bind_attr(_assets, bind_attr_dict)

        # add info
        # target attr
        if cmds.objExists("{0}.{1}".format(target_object, _info_name)):
            sour_connect_attr = cmds.listConnections("{0}.{1}".format(target_object, _info_name), s=1, d=0, p=1)
            if sour_connect_attr:
                for attr in sour_connect_attr:
                    cmds.disconnectAttr(attr, "{0}.{1}".format(target_object, _info_name))
        else:
            cmds.addAttr(target_object, ln=_info_name, at="message")
        # source attr
        if not cmds.objExists("{0}.{1}".format(source_obj, _info_name)):
            cmds.addAttr(source_obj, ln=_info_name, at="message")
        # matrix constraint attr
        cmds.addAttr(_assets, ln=_info_name, at="message")
        # connect
        cmds.connectAttr("{0}.{1}".format(source_obj, _info_name),
                         "{0}.{1}".format(_assets, _info_name))
        cmds.connectAttr("{0}.{1}".format(_assets, _info_name),
                         "{0}.{1}".format(target_object, _info_name))
        return _assets

    def _query_matrix_constraint(obj, source, target):
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
        if not cmds.objExists("{0}.{1}".format(obj, _info_name)):
            return dict_info
        if source:
            _assets = cmds.listConnections("{0}.{1}".format(obj, _info_name), s=1, d=0)
            if _assets:
                _assets = _assets[0]
                source_obj = cmds.listConnections("{0}.{1}".format(_assets, _info_name), s=1, d=0)
                if source_obj:
                    source_obj = source_obj[0]
                    dict_info.update({source_obj: [obj]})
        if target:
            _assets_list = cmds.listConnections("{0}.{1}".format(obj, _info_name), s=0, d=1)
            if _assets_list:
                target_obj_list = []
                for _assets in _assets_list:
                    target_obj = cmds.listConnections("{0}.{1}".format(_assets, _info_name), s=0, d=1)
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
        return _query_matrix_constraint(source_obj, q_source, q_target)
    else:
        for target in target_object:
            matrix_constraint = _create_matrix_constraint(source_obj, target, maintainOffset)
        return matrix_constraint


def parentspaceConstraint(*args, **kwargs):
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
        # Create nodes
        node_bw = cmds.createNode("blendMatrix", name="{0}_spaceBW".format(target_obj))
        node_getLocalMatrix = cmds.createNode("multMatrix", name="{0}_getLocalMatrix".format(target_obj))
        node_decMatrix = cmds.createNode("decomposeMatrix", name="{0}_decomposeMatrix".format(target_obj))
        node_parentMult = cmds.createNode("multMatrix", name="{0}_parentMult".format(target_obj))

        # Setup attributes
        cmds.addAttr(node_bw, ln=parentspace_attrName, at="enum", en="Parent", k=0)
        bind_attr_dict = {
            parentspace_attrName: "{0}.{1}".format(node_bw, parentspace_attrName),
            "inputBlendTarget": "{0}.target".format(node_bw)
        }
        add_node_list = [node_bw, node_getLocalMatrix, node_decMatrix, node_parentMult]

        # Setup connections
        cmds.setAttr("{0}.matrixIn[0]".format(node_parentMult),
                     get_local_matrix(target_obj), type="matrix")
        cmds.connectAttr("{0}.parentMatrix[0]".format(target_obj),
                         "{0}.matrixIn[1]".format(node_parentMult))
        cmds.connectAttr("{0}.matrixSum".format(node_parentMult),
                         "{0}.inputMatrix".format(node_bw))
        cmds.connectAttr("{0}.outputMatrix".format(node_bw),
                         "{0}.matrixIn[0]".format(node_getLocalMatrix))
        cmds.connectAttr("{0}.parentInverseMatrix[0]".format(target_obj),
                         "{0}.matrixIn[1]".format(node_getLocalMatrix))
        cmds.connectAttr("{0}.matrixSum".format(node_getLocalMatrix),
                         "{0}.inputMatrix".format(node_decMatrix))

        # Connect decompose matrix outputs
        cmds.connectAttr("{0}.rotateOrder".format(target_obj),
                         "{0}.inputRotateOrder".format(node_decMatrix))
        cmds.connectAttr("{0}.outputTranslate".format(node_decMatrix),
                         "{0}.translate".format(target_obj))
        cmds.connectAttr("{0}.outputScale".format(node_decMatrix),
                         "{0}.scale".format(target_obj))
        cmds.connectAttr("{0}.outputShear".format(node_decMatrix),
                         "{0}.shear".format(target_obj))

        # Handle joint orient
        if cmds.objExists("{0}.jointOrient".format(target_obj)):
            inverse_orient_node = create_inverse_orient_node(
                name="{0}_inverseJointOrient_matrixConstraint".format(target_obj))
            add_node_list.append(inverse_orient_node)
            cmds.connectAttr("{0}.jointOrient".format(target_obj),
                             "{0}.inputOrientRotate".format(inverse_orient_node))
            cmds.connectAttr("{0}.rotateOrder".format(target_obj),
                             "{0}.inputRotateOrder".format(inverse_orient_node))
            cmds.connectAttr("{0}.outputQuat".format(node_decMatrix),
                             "{0}.inputRotateQuat".format(inverse_orient_node))
            cmds.connectAttr("{0}.outputRotate".format(inverse_orient_node),
                             "{0}.rotate".format(target_obj), f=1)
            cmds.connectAttr("{0}.outputQuat".format(inverse_orient_node),
                             "{0}.rotateQuaternion".format(target_obj), f=1)
        else:
            cmds.connectAttr("{0}.outputRotate".format(node_decMatrix),
                             "{0}.rotate".format(target_obj))
            cmds.connectAttr("{0}.outputQuat".format(node_decMatrix),
                             "{0}.rotateQuaternion".format(target_obj))

        # Create assets
        assets_name = generate_unique_name("{0}_parentspace".format(target_obj))
        _assets = create_assets(name=assets_name, parent_assets="ParentspaceAssets",
                                add_node=add_node_list)
        bind_attr(_assets, bind_attr_dict)

        # Setup attributes
        if not cmds.objExists("{0}.{1}".format(target_obj, parentspace_attrName)):
            cmds.addAttr(target_obj, ln=parentspace_attrName,
                         pxy="{0}.{1}".format(_assets, parentspace_attrName), k=1)
        else:
            cmds.addAttr("{0}.{1}".format(target_obj, parentspace_attrName), e=1, en="Parent", k=1)

        # Add message connections
        cmds.addAttr(_assets, ln=_info_name, at="message")
        if not cmds.objExists("{0}.{1}".format(target_obj, _info_name)):
            cmds.addAttr(target_obj, ln=_info_name, at="message")
        cmds.connectAttr("{0}.{1}".format(_assets, _info_name),
                         "{0}.{1}".format(target_obj, _info_name))

        return _assets

    def _add_parentspace(control_obj, target_obj, nice_name=None,
                         translate=True, rotate=True, scale=True, shear=True):
        # Get or create assets
        if not cmds.objExists("{0}.{1}".format(target_obj, _info_name)):
            _assets = _pre_parentspace(target_obj)
        else:
            _assets = cmds.listConnections("{0}.{1}".format(target_obj, _info_name), s=1, d=0)[0]

        # Get blend matrix nodes
        node_bw_target_attr = cmds.ls("{0}.inputBlendTarget".format(_assets))[0]
        node_bw = cmds.ls("{0}.inputBlendTarget".format(_assets), o=1)[0]

        # Setup enum attribute
        if not nice_name:
            nice_name = control_obj
        enum_str = cmds.addAttr("{0}.{1}".format(node_bw, parentspace_attrName), q=1, en=1)
        nice_name_list = enum_str.split(":")
        nice_name_list.append(nice_name)
        enum_str = ":".join(nice_name_list)
        parent_indices = len(nice_name_list)-1

        # Update enums
        cmds.addAttr("{0}.{1}".format(node_bw, parentspace_attrName), e=1, en=enum_str)
        cmds.addAttr("{0}.{1}".format(target_obj, parentspace_attrName), e=1, en=enum_str)

        # Create constraint connections
        offset_matrix = get_offset_matrix(get_world_matrix(target_obj),
                                          get_world_matrix(control_obj))
        node_multMatrix = cmds.createNode("multMatrix",
                                          name="{0}_{1}_multMatrix".format(control_obj, target_obj))
        cmds.setAttr("{0}.matrixIn[0]".format(node_multMatrix),
                     offset_matrix, type="matrix")
        cmds.connectAttr("{0}.worldMatrix[0]".format(control_obj),
                         "{0}.matrixIn[1]".format(node_multMatrix))

        # Connect to blend matrix
        cmds.connectAttr("{0}.matrixSum".format(node_multMatrix),
                         "{0}[{1}].targetMatrix".format(node_bw_target_attr, parent_indices))

        # Setup transform attributes
        if cmds.about(api=True) >= 20230000:
            blend_attr = ["translateWeight", "rotateWeight", "scaleWeight", "shearWeight"]
        else:
            blend_attr = ["useTranslate", "useRotate", "useScale", "useShear"]

        status = [translate, rotate, scale, shear]
        for i, attr in enumerate(blend_attr):
            cmds.container(_assets, e=1,
                           publishName="{0}_{1}".format(attr, parent_indices))
            cmds.container(_assets, e=1,
                           bindAttr=["{0}[{1}].{2}".format(node_bw_target_attr, parent_indices, attr),
                                     "{0}_{1}".format(attr, parent_indices)])
            cmds.setAttr("{0}[{1}].{2}".format(node_bw_target_attr, parent_indices, attr),
                         status[i])

        # Setup driven keys
        cmds.setDrivenKeyframe("{0}[{1}].weight".format(node_bw_target_attr, parent_indices),
                               cd="{0}.{1}".format(node_bw, parentspace_attrName),
                               dv=parent_indices - 1, v=0)
        cmds.setDrivenKeyframe("{0}[{1}].weight".format(node_bw_target_attr, parent_indices),
                               cd="{0}.{1}".format(node_bw, parentspace_attrName),
                               dv=parent_indices, v=1)
        cmds.setDrivenKeyframe("{0}[{1}].weight".format(node_bw_target_attr, parent_indices),
                               cd="{0}.{1}".format(node_bw, parentspace_attrName),
                               dv=parent_indices + 1, v=0)

        node_sdk = cmds.listConnections("{0}[{1}].weight".format(node_bw_target_attr, parent_indices),
                                        s=1, d=0)
        cmds.container(_assets, e=1, addNode=[node_multMatrix]+node_sdk)
    # Main function logic
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


def offset_fk(control_list, offset_list):
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

        node_multMatrix = cmds.createNode("multMatrix", name="{0}_multMatrix_offsetFK".format(next_control))
        node_decomposeMatrix = cmds.createNode("decomposeMatrix", name="{0}_decomposeMatrix_offsetFK".format(next_control))
        _add_node_list = [node_multMatrix, node_decomposeMatrix]
        # get offset matrix from 'offset_obj' with 'next offset_obj'
        cmds.connectAttr("{0}.parentMatrix[0]".format(next_offset),
                         "{0}.matrixIn[0]".format(node_multMatrix))
        cmds.connectAttr("{0}.parentInverseMatrix[0]".format(offset),
                         "{0}.matrixIn[1]".format(node_multMatrix))
        # control constraint it
        cmds.connectAttr("{0}.worldMatrix[0]".format(control),
                         "{0}.matrixIn[2]".format(node_multMatrix))
        # cal local matrix
        cmds.connectAttr("{0}.parentInverseMatrix[0]".format(next_offset),
                         "{0}.matrixIn[3]".format(node_multMatrix))
        # output
        cmds.connectAttr("{0}.matrixSum".format(node_multMatrix),
                         "{0}.inputMatrix".format(node_decomposeMatrix))
        cmds.connectAttr("{0}.rotateOrder".format(next_offset),
                         "{0}.inputRotateOrder".format(node_decomposeMatrix))

        cmds.connectAttr("{0}.outputTranslate".format(node_decomposeMatrix), "{0}.translate".format(next_offset), f=1)  # out translate
        cmds.connectAttr("{0}.outputScale".format(node_decomposeMatrix), "{0}.scale".format(next_offset), f=1)  # out scale
        cmds.connectAttr("{0}.outputShear".format(node_decomposeMatrix), "{0}.shear".format(next_offset), f=1)  # out shear
        if cmds.objExists("{0}.jointOrient".format(next_offset)):
            inverse_orient_node = generate_unique_name("{0}_inverseJointOrient_matrixConstraint".format(next_offset))
            inverse_orient_node = create_inverse_orient_node(name=inverse_orient_node)
            _add_node_list.append(inverse_orient_node)
            cmds.connectAttr("{0}.jointOrient".format(next_offset), "{0}.inputOrientRotate".format(inverse_orient_node))  # in orient rotate
            cmds.connectAttr("{0}.rotateOrder".format(next_offset), "{0}.inputRotateOrder".format(inverse_orient_node))  # in rotate order
            cmds.connectAttr("{0}.outputQuat".format(node_decomposeMatrix), "{0}.inputRotateQuat".format(inverse_orient_node))  # in rotate
            cmds.connectAttr("{0}.outputRotate".format(inverse_orient_node), "{0}.rotate".format(next_offset), f=1)  # out rotate
            cmds.connectAttr("{0}.outputQuat".format(inverse_orient_node), "{0}.rotateQuaternion".format(next_offset), f=1)  # out quat
        else:
            cmds.connectAttr("{0}.outputRotate".format(node_decomposeMatrix), "{0}.rotate".format(next_offset), f=1)  # out rotate
            cmds.connectAttr("{0}.outputQuat".format(node_decomposeMatrix), "{0}.rotateQuaternion".format(next_offset), f=1)  # out quat
        _assets = generate_unique_name("{0}_offsetFK".format(next_control))
        _assets = create_assets(_assets, parent_assets="OffsetFK", add_node=_add_node_list)
