import maya.cmds as cmds
import maya.api.OpenMaya as om
from utils.generate_unique_name import generate_unique_name
from utils.create_assets import create_assets, bind_attr


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
    """get object's local space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: local matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return om.MFnTransform(sel_list.getDagPath(0)).transformation().asMatrix()


def get_world_matrix(obj: str) -> om.MMatrix:
    """get object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: world matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).inclusiveMatrix()


def get_parent_matrix(obj: str) -> om.MMatrix:
    """get object's parent object's world space matrix

    Args:
        obj (str): maya transform name

    Returns:
        om.MMatrix: parent object's world space matrix
    """
    sel_list = om.MSelectionList()
    sel_list.add(obj)
    return sel_list.getDagPath(0).exclusiveMatrix()


def set_local_matrix(obj: str, matrix: om.MMatrix) -> None:
    """set maya object's local as input matrix

    Args:
        obj (str): maya transform name
        matrix (om.MMatrix): input local matrix
    """
    if cmds.objectType(obj) == "joint":
        try:
            cmds.setAttr(f"{obj}.jointOrient", 0, 0, 0)
        except Exception as e:
            om.MGlobal.displayWarning(str(e))
    set_trs(obj, matrix_to_trs(matrix))


def set_world_matrix(obj: str, matrix: om.MMatrix) -> None:
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
    om_transformation = om.MTransformationMatrix()
    translate = om.MVector(trs[0], trs[1], trs[2]) / UNIT_CONVERT()
    euler_radians = om.MEulerRotation(*[0.017453292520882225*angle for angle in trs[3:6]], rotateOrder)
    scale = om.MVector(trs[6], trs[7], trs[8])
    om_transformation.setTranslation(translate, 1)
    om_transformation.setRotation(euler_radians)
    om_transformation.setScale(scale, 1)
    return om_transformation.asMatrix()


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


def create_fbf_node(matrix: om.MMatrix = om.MMatrix(), **kwargs) -> str:
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


def create_inverse_orient_node(name: str):
    node_euler_to_quat = cmds.createNode("eulerToQuat", name=f"{name}_eulerToQuat")
    node_invert_quat = cmds.createNode("quatInvert", name=f"{name}_invertQuat")
    node_prod_quat = cmds.createNode("quatProd", name=f"{name}_prodQuat")
    node_quat_to_euler = cmds.createNode("quatToEuler", name=f"{name}_quatToEuler")

    cmds.connectAttr(f"{node_euler_to_quat}.outputQuat",
                     f"{node_invert_quat}.inputQuat")
    cmds.connectAttr(f"{node_invert_quat}.outputQuat",
                     f"{node_prod_quat}.input2Quat")
    cmds.connectAttr(f"{node_prod_quat}.outputQuat",
                     f"{node_quat_to_euler}.inputQuat")
    cmds.connectAttr(f"{node_euler_to_quat}.inputRotateOrder",
                     f"{node_quat_to_euler}.inputRotateOrder")
    # assets box
    assets = create_assets(name, add_node=[node_euler_to_quat, node_invert_quat, node_prod_quat, node_quat_to_euler])
    bind_attr_dict = {"inputOrientRotate": f"{node_euler_to_quat}.inputRotate",
                      "inputRotateOrder": f'{node_euler_to_quat}.inputRotateOrder',
                      "inputRotateQuat": f"{node_prod_quat}.input1Quat",
                      "outputRotate": f"{node_quat_to_euler}.outputRotate",
                      "outputQuat": f"{node_prod_quat}.outputQuat"}
    bind_attr(assets, bind_attr_dict)
    return assets


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

    def _create_matrix_constraint(source_obj: str,
                                  target_object: str,
                                  keep_offset: bool = True):
        """
        Create matrix constraint between source and target

        Args:
            source_obj: Driver object
            target_object: Driven object
            keep_offset: Maintain offset transforms
        """
        offset_matrix = get_offset_matrix(get_world_matrix(target_object), get_world_matrix(source_obj))
        node_multMatrix = cmds.createNode("multMatrix", name=f"{target_object}_MM_matrixConstraint")
        node_decomposeMatrix = cmds.createNode("decomposeMatrix", name=f"{target_object}_DM_matrixConstraint")
        bind_attr_dict = {"offsetMatrix": f"{node_multMatrix}.matrixIn[0]"}
        add_node_list = [node_multMatrix, node_decomposeMatrix]
        if keep_offset:
            cmds.setAttr(f"{node_multMatrix}.matrixIn[0]", offset_matrix, type="matrix")
        cmds.connectAttr(f"{source_obj}.worldMatrix[0]",
                         f"{node_multMatrix}.matrixIn[1]")
        cmds.connectAttr(f"{target_object}.parentInverseMatrix[0]",
                         f"{node_multMatrix}.matrixIn[2]")
        cmds.connectAttr(f"{target_object}.rotateOrder", f"{node_decomposeMatrix}.inputRotateOrder")  # in  rotate order
        cmds.connectAttr(f"{node_multMatrix}.matrixSum", f"{node_decomposeMatrix}.inputMatrix")  # in matrix
        cmds.connectAttr(f"{node_decomposeMatrix}.outputTranslate", f"{target_object}.translate", f=1)  # out translate
        cmds.connectAttr(f"{node_decomposeMatrix}.outputScale", f"{target_object}.scale", f=1)  # out scale
        cmds.connectAttr(f"{node_decomposeMatrix}.outputShear", f"{target_object}.shear", f=1)  # out shear
        if cmds.objExists(f"{target_object}.jointOrient"):
            inverse_orient_node = generate_unique_name(f"{target_object}_inverseJointOrient_matrixConstraint")
            inverse_orient_node = create_inverse_orient_node(name=inverse_orient_node)
            add_node_list.append(inverse_orient_node)
            cmds.connectAttr(f"{target_object}.jointOrient", f"{inverse_orient_node}.inputOrientRotate")  # in orient rotate
            cmds.connectAttr(f"{target_object}.rotateOrder", f"{inverse_orient_node}.inputRotateOrder")  # in rotate order
            cmds.connectAttr(f"{node_decomposeMatrix}.outputQuat", f"{inverse_orient_node}.inputRotateQuat")  # in rotate
            cmds.connectAttr(f"{inverse_orient_node}.outputRotate", f"{target_object}.rotate", f=1)  # out rotate
            cmds.connectAttr(f"{inverse_orient_node}.outputQuat", f"{target_object}.rotateQuaternion", f=1)  # out quat
        else:
            cmds.connectAttr(f"{node_decomposeMatrix}.outputRotate", f"{target_object}.rotate", f=1)  # out rotate
            cmds.connectAttr(f"{node_decomposeMatrix}.outputQuat", f"{target_object}.rotateQuaternion", f=1)  # out quat

        # assets box
        matrix_assets = generate_unique_name(f"{target_object}_matrixConstraint")
        matrix_assets = create_assets(name=matrix_assets, parent_assets="MatrixConstraint",
                                      add_node=add_node_list)
        bind_attr(matrix_assets, bind_attr_dict)

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
        cmds.addAttr(matrix_assets, ln=_info_name, at="message")
        # connect
        cmds.connectAttr(f"{source_obj}.{_info_name}",
                         f"{matrix_assets}.{_info_name}")
        cmds.connectAttr(f"{matrix_assets}.{_info_name}",
                         f"{target_object}.{_info_name}")
        return matrix_assets

    def _query_matrix_constraint(obj: str,
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
        if source:
            matrix_constraint = cmds.listConnections(f"{obj}.{_info_name}", s=1, d=0)
            if matrix_constraint:
                matrix_constraint = matrix_constraint[0]
                source_obj = cmds.listConnections(f"{matrix_constraint}.{_info_name}", s=1, d=0)
                if source_obj:
                    source_obj = source_obj[0]
                    dict_info.update({source_obj: [obj]})
        if target:
            matrix_constraint_list = cmds.listConnections(f"{obj}.{_info_name}", s=0, d=1)
            if matrix_constraint_list:
                target_obj_list = []
                for matrix_constraint in matrix_constraint_list:
                    target_obj = cmds.listConnections(f"{matrix_constraint}.{_info_name}", s=0, d=1)
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
        node_getLocalMatrix = cmds.createNode("multMatrix", name=f"{target_obj}_getLocalMatrix")
        node_decMatrix = cmds.createNode("decomposeMatrix", name=f"{target_obj}_decomposeMatrix")
        node_parentMult = cmds.createNode("multMatrix", name=f"{target_obj}_parentMult")
        cmds.addAttr(node_bw, ln=parentspace_attrName, at="enum", en="Parent", k=0)
        bind_attr_dict = {parentspace_attrName: f"{node_bw}.{parentspace_attrName}",
                          "inputBlendTarget": f"{node_bw}.target"}
        add_node_list = [node_bw, node_getLocalMatrix, node_decMatrix, node_parentMult]
        # parent connect
        cmds.setAttr(f"{node_parentMult}.matrixIn[0]",
                     get_local_matrix(target_obj),
                     type="matrix")
        cmds.connectAttr(f"{target_obj}.parentMatrix[0]",
                         f"{node_parentMult}.matrixIn[1]")
        cmds.connectAttr(f"{node_parentMult}.matrixSum",
                         f"{node_bw}.inputMatrix")
        # blend world matrix to local matrix
        cmds.connectAttr(f"{node_bw}.outputMatrix",
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
            inverse_orient_node = create_inverse_orient_node(name=f"{target_obj}_inverseJointOrient_matrixConstraint")
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
        assets_name = generate_unique_name(f"{target_obj}_parentspace")
        parentspace_assets = create_assets(name=assets_name, parent_assets="ParentspaceAssets",
                                           add_node=add_node_list)
        bind_attr(parentspace_assets, bind_attr_dict)
        # add parentspace attr to obj
        if not cmds.objExists(f"{target_obj}.{parentspace_attrName}"):
            cmds.addAttr(target_obj, ln=parentspace_attrName, pxy=f"{parentspace_assets}.{parentspace_attrName}", k=1)
        else:
            cmds.addAttr(f"{target_obj}.{parentspace_attrName}", e=1, en="Parent", k=1)
        # add message info to obj
        cmds.addAttr(parentspace_assets, ln=_info_name, at="message")
        if not cmds.objExists(f"{target_obj}.{_info_name}"):
            cmds.addAttr(target_obj, ln=_info_name, at="message")
        cmds.connectAttr(f"{parentspace_assets}.{_info_name}",
                         f"{target_obj}.{_info_name}")

        return parentspace_assets

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
            parentspace_assets = _pre_parentspace(target_obj)
        else:
            parentspace_assets = cmds.listConnections(f"{target_obj}.{_info_name}", s=1, d=0)[0]

        # get node blendMatrix
        node_bw_target_attr = cmds.ls(f"{parentspace_assets}.inputBlendTarget")[0]
        node_bw = cmds.ls(f"{parentspace_assets}.inputBlendTarget", o=1)[0]

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
        offset_matrix = get_offset_matrix(get_world_matrix(target_obj),
                                          get_world_matrix(control_obj))
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
            cmds.container(parentspace_assets, e=1, publishName=f'{attr}_{parent_indices}')
            cmds.container(parentspace_assets, e=1, bindAttr=[f"{node_bw_target_attr}[{parent_indices}].{attr}", f'{attr}_{parent_indices}'])
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
        cmds.container(parentspace_assets, e=1, addNode=[node_multMatrix]+node_sdk)
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


def reset_transform_value(obj, transform=True, userDefined=True):
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


def reset_transform_value_cmd(transform=True, userDefined=False):
    def _show_message(msg):
        message = f"<hl> {msg} </hl>"
        cmds.inViewMessage(amg=message, pos='botRight', fade=True, fadeInTime=100, fadeStayTime=1000, fadeOutTime=100)
    for obj in cmds.ls(sl=1):
        reset_transform_value(obj, transform, userDefined)
    msg = "Reset transform value."
    if userDefined:
        msg = "Reset value (all)."
    _show_message(msg)
